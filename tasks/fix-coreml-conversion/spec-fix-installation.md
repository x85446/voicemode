# Specification: Fix Core ML Installation

## Objective
Implement automatic dependency installation and improve the Core ML conversion process to ensure models are successfully converted when possible.

## Requirements

### 1. Automatic Dependency Detection
- Check for required Python packages before attempting conversion
- Detect UV availability and project configuration
- Verify Xcode Command Line Tools installation

### 2. Smart Dependency Installation
- Attempt automatic installation of missing packages
- Use UV when available for project-aware installation
- Fall back to pip if UV is not available
- Handle user consent for large downloads

### 3. Robust Conversion Process
- Pre-flight checks before attempting conversion
- Better handling of different Whisper installation paths
- Timeout handling for long conversions
- Cleanup of partial/failed conversions

## Implementation

### Phase 1: Dependency Detection and Installation

#### Step 1: Create Dependency Checker

Location: `/voice_mode/utils/services/whisper_coreml.py` (new file)

```python
import subprocess
import shutil
from pathlib import Path
from typing import Dict, List, Optional

class CoreMLDependencyManager:
    """Manages Core ML dependencies for Whisper model conversion."""
    
    REQUIRED_PACKAGES = [
        "torch",
        "coremltools", 
        "openai-whisper",
        "ane_transformers"
    ]
    
    def check_dependencies(self) -> Dict[str, bool]:
        """
        Check which dependencies are installed.
        
        Returns:
            Dict mapping package name to installation status
        """
        status = {}
        for package in self.REQUIRED_PACKAGES:
            status[package] = self._is_package_installed(package)
        return status
    
    def _is_package_installed(self, package: str) -> bool:
        """Check if a Python package is installed."""
        try:
            # Try UV first if available
            if shutil.which("uv"):
                result = subprocess.run(
                    ["uv", "run", "python", "-c", f"import {package}"],
                    capture_output=True,
                    timeout=5
                )
                return result.returncode == 0
            else:
                # Fall back to standard python
                result = subprocess.run(
                    ["python", "-c", f"import {package}"],
                    capture_output=True,
                    timeout=5
                )
                return result.returncode == 0
        except (subprocess.TimeoutExpired, FileNotFoundError):
            return False
    
    async def install_dependencies(
        self,
        missing_packages: List[str],
        models_dir: Path,
        auto_install: bool = True
    ) -> Dict[str, Union[bool, str]]:
        """
        Install missing dependencies.
        
        Args:
            missing_packages: List of packages to install
            models_dir: Whisper models directory (contains requirements.txt)
            auto_install: Whether to install without prompting
            
        Returns:
            Installation result with success status and any errors
        """
        if not missing_packages:
            return {"success": True, "message": "All dependencies installed"}
        
        # Check for requirements file
        requirements_file = models_dir / "requirements-coreml.txt"
        if not requirements_file.exists():
            return {
                "success": False,
                "error": "requirements-coreml.txt not found",
                "manual_install": f"pip install {' '.join(missing_packages)}"
            }
        
        # Estimate download size
        package_sizes = {
            "torch": "2.5GB",
            "coremltools": "50MB",
            "openai-whisper": "100MB",
            "ane_transformers": "10MB"
        }
        
        total_size = sum([
            float(package_sizes.get(p, "10MB").rstrip("GBMB"))
            for p in missing_packages
        ])
        
        if total_size > 500 and not auto_install:  # MB
            return {
                "success": False,
                "error": f"Large download required (~{total_size}MB)",
                "packages": missing_packages,
                "install_command": f"uv pip install -r {requirements_file}",
                "retry_with": "force_install=True to install automatically"
            }
        
        # Attempt installation
        try:
            if shutil.which("uv"):
                result = subprocess.run(
                    ["uv", "pip", "install", "-r", str(requirements_file)],
                    capture_output=True,
                    text=True,
                    timeout=300  # 5 minutes
                )
            else:
                result = subprocess.run(
                    ["pip", "install", "-r", str(requirements_file)],
                    capture_output=True,
                    text=True,
                    timeout=300
                )
            
            if result.returncode == 0:
                return {
                    "success": True,
                    "message": "Dependencies installed successfully",
                    "packages_installed": missing_packages
                }
            else:
                return {
                    "success": False,
                    "error": "Installation failed",
                    "stderr": result.stderr,
                    "manual_install": f"pip install -r {requirements_file}"
                }
                
        except subprocess.TimeoutExpired:
            return {
                "success": False,
                "error": "Installation timed out after 5 minutes",
                "manual_install": f"pip install -r {requirements_file}"
            }
```

#### Step 2: Integrate Dependency Management

Location: `/voice_mode/utils/services/whisper_helpers.py`

Add before `convert_to_coreml()`:

```python
from .whisper_coreml import CoreMLDependencyManager

async def ensure_coreml_dependencies(
    models_dir: Path,
    auto_install: bool = False
) -> Dict[str, Union[bool, str]]:
    """
    Ensure Core ML dependencies are available.
    
    Returns:
        Dict with 'ready' bool and optional 'error' or 'missing_packages'
    """
    manager = CoreMLDependencyManager()
    
    # Check dependencies
    dep_status = manager.check_dependencies()
    missing = [pkg for pkg, installed in dep_status.items() if not installed]
    
    if not missing:
        return {"ready": True}
    
    # Try to install if requested
    if auto_install:
        install_result = await manager.install_dependencies(
            missing, 
            models_dir,
            auto_install=True
        )
        
        if install_result["success"]:
            return {"ready": True, "installed": missing}
        else:
            return {
                "ready": False,
                "error": install_result.get("error"),
                "missing_packages": missing,
                "install_command": install_result.get("manual_install")
            }
    else:
        return {
            "ready": False,
            "missing_packages": missing,
            "install_command": f"uv pip install {' '.join(missing)}"
        }
```

### Phase 2: Improved Conversion Process

#### Step 1: Add Pre-flight Checks

Modify `convert_to_coreml()`:

```python
async def convert_to_coreml(
    model: str,
    models_dir: Union[str, Path],
    auto_install_deps: bool = False
) -> Dict[str, Union[bool, str, Dict]]:
    """Enhanced Core ML conversion with pre-flight checks."""
    
    models_dir = Path(models_dir)
    
    # Pre-flight check 1: Verify model file exists
    model_path = models_dir / f"ggml-{model}.bin"
    if not model_path.exists():
        return {
            "success": False,
            "error": f"Model file not found: {model_path}",
            "error_category": "missing_model"
        }
    
    # Pre-flight check 2: Check dependencies
    dep_check = await ensure_coreml_dependencies(models_dir, auto_install_deps)
    if not dep_check.get("ready"):
        return {
            "success": False,
            "error": "Missing Core ML dependencies",
            "error_category": "missing_dependencies",
            "missing_packages": dep_check.get("missing_packages"),
            "install_command": dep_check.get("install_command"),
            "installed_packages": dep_check.get("installed", [])
        }
    
    # Pre-flight check 3: Verify conversion script exists
    convert_script = models_dir / "convert-whisper-to-coreml.py"
    if not convert_script.exists():
        # Try to find it in whisper installation
        whisper_dirs = [
            Path.home() / ".voicemode" / "services" / "whisper",
            Path.home() / ".voicemode" / "whisper.cpp"
        ]
        
        for whisper_dir in whisper_dirs:
            script_path = whisper_dir / "models" / "convert-whisper-to-coreml.py"
            if script_path.exists():
                shutil.copy2(script_path, convert_script)
                break
        
        if not convert_script.exists():
            return {
                "success": False,
                "error": "Core ML conversion script not found",
                "error_category": "missing_script"
            }
    
    # Pre-flight check 4: Check for existing Core ML model
    coreml_path = models_dir / f"ggml-{model}-encoder.mlmodelc"
    if coreml_path.exists():
        return {
            "success": True,
            "path": str(coreml_path),
            "message": "Core ML model already exists",
            "cached": True
        }
    
    # Proceed with conversion...
    # [Rest of existing conversion code with enhanced error handling]
```

#### Step 2: Add Conversion Progress Tracking

```python
async def convert_to_coreml_with_progress(
    model: str,
    models_dir: Path,
    progress_callback: Optional[Callable] = None
) -> Dict:
    """Convert with progress tracking."""
    
    import asyncio
    
    # Start conversion in subprocess
    process = await asyncio.create_subprocess_exec(
        "uv", "run", "python", 
        str(models_dir / "convert-whisper-to-coreml.py"),
        model,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
        cwd=str(models_dir)
    )
    
    # Monitor progress
    start_time = time.time()
    timeout = 600  # 10 minutes
    
    while True:
        try:
            await asyncio.wait_for(
                asyncio.shield(process.wait()),
                timeout=1.0
            )
            break  # Process completed
        except asyncio.TimeoutError:
            elapsed = time.time() - start_time
            
            if elapsed > timeout:
                process.kill()
                return {
                    "success": False,
                    "error": "Conversion timed out after 10 minutes",
                    "error_category": "timeout"
                }
            
            if progress_callback:
                progress_callback(elapsed, timeout)
            
            # Check for partial model (indicates progress)
            mlpackage = models_dir / f"coreml-encoder-{model}.mlpackage"
            if mlpackage.exists():
                size = sum(f.stat().st_size for f in mlpackage.rglob("*"))
                logger.info(f"Core ML conversion in progress: {size / 1024 / 1024:.1f}MB")
    
    # Get results
    stdout, stderr = await process.communicate()
    
    if process.returncode == 0:
        # Verify compilation completed
        mlmodelc = models_dir / f"ggml-{model}-encoder.mlmodelc"
        if mlmodelc.exists():
            return {
                "success": True,
                "path": str(mlmodelc),
                "duration": time.time() - start_time,
                "message": f"Core ML model created in {time.time() - start_time:.1f}s"
            }
    
    # Handle failure
    return {
        "success": False,
        "error": stderr.decode() if stderr else "Unknown error",
        "error_category": "conversion_failed",
        "duration": time.time() - start_time
    }
```

### Phase 3: Tool Integration

#### Update `whisper_model_install()`:

```python
@mcp.tool()
async def whisper_model_install(
    model: Union[str, List[str]] = "large-v2",
    force_download: Union[bool, str] = False,
    skip_core_ml: Union[bool, str] = False,
    auto_install_deps: Union[bool, str] = False  # New parameter
) -> str:
    """
    Download Whisper model(s) with automatic Core ML conversion.
    
    Args:
        model: Model name(s) to download
        force_download: Re-download even if model exists
        skip_core_ml: Skip Core ML conversion
        auto_install_deps: Automatically install Core ML dependencies
                          (may download large files like PyTorch ~2.5GB)
    """
    # Implementation with dependency installation support
```

## Testing Plan

1. **Fresh Environment Test**
   - Start with no Core ML dependencies
   - Run model install with `auto_install_deps=False`
   - Verify clear error about missing dependencies
   - Run with `auto_install_deps=True`
   - Verify dependencies install and conversion succeeds

2. **Partial Dependencies Test**
   - Install only torch, missing coremltools
   - Verify specific error about missing coremltools
   - Auto-install remaining dependencies
   - Verify conversion succeeds

3. **Network Issues Test**
   - Simulate slow/interrupted downloads
   - Verify timeout handling
   - Verify partial download cleanup

4. **Large Model Test**
   - Test with large-v3 model
   - Verify progress tracking works
   - Verify timeout is sufficient

## Success Metrics

1. **Dependency Installation**: 90% success rate for automatic installation
2. **Conversion Success**: 95% success rate when dependencies are met
3. **Error Recovery**: 100% of failures provide actionable next steps
4. **Performance**: Conversion completes within 5 minutes for large models