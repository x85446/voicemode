"""Download Whisper models with Core ML support."""

import os
import sys
import json
import logging
import platform
import subprocess
from pathlib import Path
from typing import Union, List, Dict, Any

from voice_mode.server import mcp
from voice_mode.config import logger, MODELS_DIR
from voice_mode.utils.services.whisper_helpers import download_whisper_model, get_available_models

logger = logging.getLogger("voice-mode")


@mcp.tool()
async def whisper_model_install(
    model: Union[str, List[str]] = "large-v2",
    force_download: Union[bool, str] = False,
    skip_core_ml: Union[bool, str] = False,
    install_torch: Union[bool, str] = False,
    auto_confirm: Union[bool, str] = False
) -> str:
    """Download Whisper model(s) with optional Core ML conversion.
    
    Downloads whisper.cpp models to the configured directory. On Apple Silicon,
    automatically converts models to Core ML format for better performance.
    
    Args:
        model: Model name(s) to download. Can be:
               - Single model: "large-v2"
               - List of models: ["base", "small"]
               - "all" to download all available models
        force_download: Re-download even if model exists (default: False)
        skip_core_ml: Skip Core ML conversion on Apple Silicon (default: False)
        install_torch: Install PyTorch for CoreML (adds ~2.5GB) (default: False)
        auto_confirm: Skip all confirmation prompts (default: False)
        
    Available models:
        - tiny, tiny.en
        - base, base.en
        - small, small.en
        - medium, medium.en
        - large-v1, large-v2, large-v3
        - large-v3-turbo
        
    Returns:
        Status message with download results
        
    Examples:
        # Download default model
        download_model()
        
        # Download specific model
        download_model("small.en")
        
        # Download multiple models
        download_model(["base", "small", "medium"])
        
        # Download all models
        download_model("all")
        
        # Force re-download
        download_model("large-v3", force_download=True)
    """
    try:
        # Get model directory from configuration
        models_dir = MODELS_DIR / "whisper"
        
        # Check both possible whisper installation locations
        whisper_install_dir = Path.home() / ".voicemode" / "services" / "whisper"
        legacy_install_dir = Path.home() / ".voicemode" / "whisper.cpp"
        
        if whisper_install_dir.exists():
            actual_models_dir = whisper_install_dir / "models"
        elif legacy_install_dir.exists():
            actual_models_dir = legacy_install_dir / "models"
        else:
            return json.dumps({
                "success": False,
                "error": "Whisper.cpp not installed. Please run whisper_install first."
            }, indent=2)
        
        # Handle CoreML dependencies if needed
        coreml_status = await _handle_coreml_dependencies(
            install_torch=install_torch,
            auto_confirm=auto_confirm,
            skip_core_ml=skip_core_ml
        )
        
        if not coreml_status["continue"]:
            return json.dumps(coreml_status, indent=2)
        
        # If CoreML deps were installed, skip_core_ml may have been updated
        if coreml_status.get("coreml_deps_failed"):
            skip_core_ml = True
        
        # Parse model input
        available_models = get_available_models()
        
        if isinstance(model, str):
            if model.lower() == "all":
                models_to_download = available_models
            else:
                models_to_download = [model]
        else:
            models_to_download = model
        
        # Validate models
        invalid_models = [m for m in models_to_download if m not in available_models]
        if invalid_models:
            return json.dumps({
                "success": False,
                "error": f"Invalid models: {', '.join(invalid_models)}",
                "available_models": available_models
            }, indent=2)
        
        # Download models
        results = []
        success_count = 0
        
        for model_name in models_to_download:
            logger.info(f"Processing model: {model_name}")
            result = await download_whisper_model(
                model_name,
                actual_models_dir,
                force_download=force_download
            )
            
            # Build comprehensive result entry
            model_result = {
                "model": model_name,
                "download_success": result["success"],
                "message": result.get("message", result.get("error", "Unknown error")),
                "acceleration": result.get("acceleration", "unknown")
            }
            
            # Include Core ML status if available
            if "core_ml_status" in result and not skip_core_ml:
                core_ml = result["core_ml_status"]
                model_result["core_ml"] = {
                    "attempted": True,
                    "success": core_ml.get("success", False),
                    "error_category": core_ml.get("error_category") if not core_ml.get("success") else None,
                    "error": core_ml.get("error") if not core_ml.get("success") else None,
                    "fix_command": core_ml.get("install_command") if not core_ml.get("success") else None,
                    "package_size": core_ml.get("package_size") if not core_ml.get("success") else None
                }
            elif skip_core_ml:
                model_result["core_ml"] = {
                    "attempted": False,
                    "reason": "Skipped by user request"
                }
            
            results.append(model_result)
            
            if result["success"]:
                success_count += 1
        
        # Summary
        total_models = len(models_to_download)
        
        # Collect warnings and recommendations
        warnings = []
        recommendations = []
        
        # Check for Core ML issues
        core_ml_failures = [r for r in results if r.get("core_ml", {}).get("attempted") and not r.get("core_ml", {}).get("success")]
        if core_ml_failures:
            # Group by error category
            error_categories = {}
            for failure in core_ml_failures:
                category = failure["core_ml"].get("error_category", "unknown")
                if category not in error_categories:
                    error_categories[category] = failure["core_ml"]
            
            # Add warnings for each category
            if "missing_pytorch" in error_categories:
                warnings.append("PyTorch not installed - Core ML acceleration unavailable")
                recommendations.append(f"Install PyTorch for Core ML: {error_categories['missing_pytorch'].get('fix_command', 'uv pip install torch')}")
            elif "missing_coremltools" in error_categories:
                warnings.append("CoreMLTools not installed - Core ML acceleration unavailable")
                recommendations.append(f"Install CoreMLTools: {error_categories['missing_coremltools'].get('fix_command', 'uv pip install coremltools')}")
            
            # General Core ML recommendation
            if len(core_ml_failures) == len(results):
                recommendations.append("Models will use Metal acceleration. Core ML provides better performance on Apple Silicon.")
        
        summary = {
            "success": success_count > 0,
            "models_directory": str(actual_models_dir),
            "total_requested": total_models,
            "successful_downloads": success_count,
            "failed_downloads": total_models - success_count,
            "results": results,
            "core_ml_available": not skip_core_ml and os.uname().machine == "arm64",
        }
        
        # Add warnings and recommendations if present
        if warnings:
            summary["warnings"] = warnings
        if recommendations:
            summary["recommendations"] = recommendations
        
        # Add overall status message
        if success_count == total_models:
            if core_ml_failures:
                summary["status"] = "Models downloaded successfully but Core ML conversion failed. Using Metal acceleration."
            else:
                summary["status"] = "Models downloaded and converted successfully. Ready to use with whisper_start."
        else:
            summary["status"] = "Some models failed to download. Check the results for details."
        
        return json.dumps(summary, indent=2)
        
    except Exception as e:
        logger.error(f"Error in download_model: {e}")
        return json.dumps({
            "success": False,
            "error": str(e)
        }, indent=2)


async def _handle_coreml_dependencies(
    install_torch: bool = False,
    auto_confirm: bool = False,
    skip_core_ml: bool = False
) -> Dict[str, Any]:
    """Handle CoreML dependency installation for Apple Silicon Macs.
    
    Returns:
        Dict with 'continue' key indicating whether to proceed with model download
    """
    # Check if we're on Apple Silicon Mac
    if platform.system() != "Darwin" or platform.machine() != "arm64":
        return {"continue": True}
    
    # If skipping CoreML, no need to check dependencies
    if skip_core_ml:
        return {"continue": True}
    
    # Check if torch is already installed
    try:
        import torch
        logger.info("PyTorch already installed for CoreML support")
        return {"continue": True}
    except ImportError:
        pass
    
    # Check if user wants to install torch
    if not install_torch and not auto_confirm:
        return {
            "continue": False,
            "success": False,
            "requires_confirmation": True,
            "message": "CoreML requires PyTorch (~2.5GB). Rerun with install_torch=True to confirm.",
            "recommendation": "Set install_torch=True for CoreML acceleration (2-3x faster)"
        }
    
    # Install CoreML dependencies
    logger.info("Installing CoreML dependencies...")
    
    try:
        # Detect environment and install appropriately
        packages = ["torch>=2.0.0", "coremltools>=7.0", "transformers", "ane-transformers"]
        
        # Try UV first (most common)
        if subprocess.run(["which", "uv"], capture_output=True).returncode == 0:
            cmd = ["uv", "pip", "install"] + packages
            logger.info("Installing via UV...")
        else:
            # Fallback to pip
            cmd = [sys.executable, "-m", "pip", "install"] + packages
            logger.info("Installing via pip...")
        
        # Run installation
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            logger.info("CoreML dependencies installed successfully")
            return {"continue": True, "coreml_deps_installed": True}
        else:
            logger.warning(f"Failed to install CoreML dependencies: {result.stderr}")
            return {
                "continue": True,
                "coreml_deps_failed": True,
                "warning": "CoreML dependencies installation failed. Models will use Metal acceleration."
            }
            
    except Exception as e:
        logger.warning(f"Error installing CoreML dependencies: {e}")
        return {
            "continue": True,
            "coreml_deps_failed": True,
            "warning": f"CoreML setup error: {str(e)}. Models will use Metal acceleration."
        }