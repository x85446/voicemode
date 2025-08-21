# Fix Core ML Conversion Task

## Problem Definition

The Core ML conversion for Whisper models is failing silently without proper error reporting back to the user or LLM. This prevents users from understanding why Core ML models aren't being created and how to fix the issue.

### Current Issues

#### 1. Silent Failures
- Core ML conversion fails due to missing dependencies but only logs warnings
- The LLM tool response shows `"core_ml_enabled": true` even when conversion fails
- No actionable error messages are returned to the user

#### 2. Missing Dependencies
The Core ML conversion requires Python packages that are not installed by default:
- `torch` (PyTorch) - Neural network operations
- `coremltools` - Apple's Core ML conversion tools  
- `openai-whisper` - Official OpenAI Whisper implementation
- `ane_transformers` - Apple Neural Engine optimizations

These are listed in `~/.voicemode/services/whisper/models/requirements-coreml.txt` but not automatically installed.

#### 3. Poor Error Propagation
- The `convert_to_coreml()` function catches exceptions but doesn't return detailed error info
- The `download_whisper_model()` function treats Core ML failure as non-critical
- The `whisper_model_install` tool doesn't include Core ML status in its response

#### 4. Complex Execution Path
The conversion attempts multiple approaches which makes debugging difficult:
1. UV-based Python execution with project dependencies
2. Fallback to standard bash script execution  
3. Different script locations (new vs legacy paths)

### Impact

Users experience:
- Core ML models not being created despite "successful" installation
- Degraded performance (Metal-only instead of Core ML acceleration)
- No clear guidance on how to enable Core ML support
- Need to manually check logs and file system to understand failures

### Files Affected

- `/voice_mode/utils/services/whisper_helpers.py` - Core conversion logic
  - `download_whisper_model()` function (lines 62-200)
  - `convert_to_coreml()` function (lines 260-318)
- `/voice_mode/tools/services/whisper/model_install.py` - LLM tool interface
  - `whisper_model_install()` function

## Task Breakdown

### Phase 1: Proper Error Reporting
Implement comprehensive error reporting so users and LLMs understand exactly why Core ML conversion fails and how to fix it.

See: [spec-error-reporting.md](spec-error-reporting.md)

### Phase 2: Fix Core ML Installation
Implement automatic dependency installation and improve the Core ML conversion process.

See: [spec-fix-installation.md](spec-fix-installation.md)

## Success Criteria

1. **Clear Error Messages**: When Core ML conversion fails, the user receives:
   - Specific reason for failure (e.g., "PyTorch not installed")
   - Exact command to fix the issue
   - Log file location for detailed debugging

2. **Accurate Status Reporting**: The tool response accurately reflects:
   - Whether Core ML conversion was attempted
   - Whether it succeeded or failed
   - What type of acceleration is available (Core ML vs Metal-only)

3. **Automatic Recovery**: Where possible, the system should:
   - Automatically install missing dependencies
   - Retry conversion after dependency installation
   - Provide fallback options when automatic fixes aren't possible

## Testing

1. Test with missing dependencies (fresh environment)
2. Test with partial dependencies (e.g., torch but no coremltools)
3. Test with all dependencies installed
4. Test error recovery and retry logic
5. Verify error messages are actionable and accurate