# Voice Mode Core ML Integration Specification

## Overview
Enhance voice mode to automatically download and use **pre-built** Core ML models from Hugging Face on Apple Silicon Macs for 2-3x faster whisper transcription performance. No Python dependencies or Xcode required!

## Key Design Principles
1. **Seamless by default**: Core ML acceleration should work without user intervention on supported hardware
2. **CLI/MCP parity**: Command-line tools and MCP tools should have identical behavior and flags
3. **Graceful fallback**: If Core ML isn't available, fall back to standard models transparently
4. **User control**: Provide flags to override default behavior when needed

## Proposed Changes

### 1. Whisper Installation Enhancement

#### Current Behavior
- `voicemode whisper install` installs whisper.cpp but no models
- User must manually run model install command

#### Proposed Behavior
```bash
# Install whisper with default base model
voicemode whisper install

# Install with specific model
voicemode whisper install --model large-v3

# Install without any model
voicemode whisper install --no-model
```

**Implementation**:
- Default model: `base` (good balance of speed/quality/size)
- Automatically detect Apple Silicon and download Core ML version
- Fall back to regular model if Core ML unavailable

### 2. Model Installation Enhancement

#### Current Behavior
- Downloads only regular ggml models
- No Core ML support

#### Proposed Behavior
```bash
# Auto-detect and download Core ML on Apple Silicon
voicemode whisper model install base

# Skip Core ML even on Apple Silicon
voicemode whisper model install base --skip-coreml

# Force Core ML download (fail if not supported)
voicemode whisper model install base --require-coreml
```

**Implementation**:
- Check platform with `platform.machine() == "arm64"` and `platform.system() == "Darwin"`
- Download from Hugging Face: `https://huggingface.co/ggerganov/whisper.cpp/resolve/main/ggml-{model}-encoder.mlmodelc.zip`
- Extract to `models/ggml-{model}-encoder.mlmodelc/`
- Verify whisper.cpp was built with `-DWHISPER_COREML=1`
- **NO Python dependencies required** - models are pre-built and ready to use
- **NO Xcode required** - models are pre-compiled to .mlmodelc format

### 3. Core ML Model Sources

**Trusted Provider**: ggerganov/whisper.cpp on Hugging Face
- Official whisper.cpp author
- Pre-built models work across all Apple Silicon (M1/M2/M3/M4)
- Models are pre-compiled to .mlmodelc format (no build step required!)
- Apple Neural Engine optimizes on first run for specific device

**Available Pre-Built Core ML Models**:
- `ggml-tiny-encoder.mlmodelc.zip` (15MB)
- `ggml-tiny.en-encoder.mlmodelc.zip` (15MB)
- `ggml-base-encoder.mlmodelc.zip` (38MB)
- `ggml-base.en-encoder.mlmodelc.zip` (38MB)
- `ggml-small-encoder.mlmodelc.zip` (163MB)
- `ggml-small.en-encoder.mlmodelc.zip` (163MB)
- `ggml-medium-encoder.mlmodelc.zip` (568MB)
- `ggml-medium.en-encoder.mlmodelc.zip` (567MB)
- `ggml-large-v1-encoder.mlmodelc.zip` (1.2GB)
- `ggml-large-v2-encoder.mlmodelc.zip` (1.2GB)
- `ggml-large-v3-encoder.mlmodelc.zip` (1.2GB)
- `ggml-large-v3-turbo-encoder.mlmodelc.zip` (1.2GB)

### 4. Configuration Updates

**Environment Variables**:
```bash
# New optional variables
VOICEMODE_WHISPER_DEFAULT_MODEL=base  # Model to install with whisper
VOICEMODE_WHISPER_USE_COREML=auto     # auto|always|never
```

**Status Display**:
```bash
voicemode whisper status
# Should show:
#   Core ML: ✓ Enabled & Active (using ggml-large-v3-encoder.mlmodelc)
```

### 5. Error Handling

- If Core ML model download fails, fall back to regular model
- If Core ML model exists but regular model missing, download regular model
- Clear error messages explaining what happened and how to fix

### 6. Detailed Implementation Plan

#### Phase 1: Core ML Download Implementation
```python
# In whisper_helpers.py - replace convert_to_coreml with:
async def download_coreml_model(model: str, models_dir: Path) -> Dict:
    """Download pre-built Core ML model from Hugging Face."""
    coreml_url = f"https://huggingface.co/ggerganov/whisper.cpp/resolve/main/ggml-{model}-encoder.mlmodelc.zip"
    coreml_zip = models_dir / f"ggml-{model}-encoder.mlmodelc.zip"
    coreml_dir = models_dir / f"ggml-{model}-encoder.mlmodelc"

    # Check if already exists
    if coreml_dir.exists():
        return {"success": True, "path": str(coreml_dir), "message": "Core ML model already exists"}

    # Download with progress
    async with aiohttp.ClientSession() as session:
        async with session.get(coreml_url) as response:
            if response.status != 200:
                return {"success": False, "error": f"HTTP {response.status}"}

            total_size = int(response.headers.get('content-length', 0))
            with open(coreml_zip, 'wb') as f:
                downloaded = 0
                async for chunk in response.content.iter_chunked(8192):
                    f.write(chunk)
                    downloaded += len(chunk)
                    if total_size:
                        progress = (downloaded / total_size) * 100
                        logger.info(f"Downloading Core ML model: {progress:.1f}%")

    # Extract
    shutil.unpack_archive(coreml_zip, models_dir)
    coreml_zip.unlink()  # Clean up zip

    return {"success": True, "path": str(coreml_dir)}
```

#### Phase 2: Update download_whisper_model
```python
# In download_whisper_model function:
if platform.system() == "Darwin" and platform.machine() == "arm64" and not skip_core_ml:
    # Download pre-built Core ML model instead of converting
    core_ml_result = await download_coreml_model(model, models_dir)
    if core_ml_result["success"]:
        logger.info(f"Core ML model downloaded for {model}")
```

#### Phase 3: Remove Core ML Conversion Code
- Delete `coreml_setup.py` entirely
- Remove `convert_to_coreml` function from `whisper_helpers.py`
- Remove all PyTorch/coremltools installation code
- Clean up venv-coreml creation logic

#### Phase 4: Whisper Install Updates
```python
# In whisper_install tool:
@mcp.tool()
async def whisper_install(
    model: str = "base",  # New default
    no_model: bool = False,
    skip_coreml: bool = False
) -> str:
    # Install whisper.cpp
    # ... existing installation code ...

    # Install default model unless --no-model
    if not no_model:
        await whisper_model_install(model, skip_core_ml=skip_coreml)
```

### 7. Implementation Priority

1. **Phase 1** (Immediate): Add Core ML download to `whisper_model_install`
   - Update `download_whisper_model` to download pre-built models
   - Remove Core ML conversion attempt
   - Test on Apple Silicon

2. **Phase 2** (Next Sprint): Update `whisper_install`
   - Add `--model` and `--no-model` flags
   - Install base model by default
   - Update documentation

3. **Phase 3** (Cleanup): Remove legacy code
   - Remove `coreml_setup.py`
   - Remove conversion functions
   - Clean up dependencies

## Benefits

1. **Performance**: 2-3x faster transcription on Apple Silicon
2. **Simplicity**: Works out of the box, no Python deps or Xcode required
3. **Compatibility**: Pre-built models work on all Apple Silicon Macs (M1/M2/M3/M4)
4. **Reliability**: No conversion failures, guaranteed to work
5. **Size Efficiency**: Only download what you need (no 2.5GB PyTorch!)
6. **Speed**: Instant setup (download vs compile)

## Testing Plan

1. Test on Apple Silicon Mac (M1/M2/M3/M4)
2. Test on Intel Mac (should skip Core ML)
3. Test on Linux (should skip Core ML)
4. Test with various model sizes
5. Test failure scenarios (network issues, disk space, etc.)

## Migration Path

For existing users:
- Detect if whisper installed without Core ML models
- Prompt to download Core ML versions of existing models
- Provide `voicemode whisper upgrade-coreml` command

## Documentation Updates

- Update README with Core ML information
- Add Core ML section to installation guide
- Document performance improvements
- Explain manual Core ML model installation for advanced users