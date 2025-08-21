# Specification: Core ML Error Reporting

## Objective
Implement comprehensive error reporting for Core ML conversion failures so users and LLMs receive actionable information about what went wrong and how to fix it.

## Requirements

### 1. Enhanced Error Detection
- Detect specific failure types (missing dependencies, compilation errors, etc.)
- Categorize errors for appropriate handling
- Capture full subprocess output (stdout and stderr)

### 2. Detailed Error Information
Each error should include:
- Error category (e.g., `missing_pytorch`, `missing_coremltools`, `conversion_failure`)
- Human-readable error message
- Exact installation command to fix the issue
- Log file location for debugging
- Command that failed (for debugging)

### 3. Error Propagation Chain
Errors must propagate correctly through the call stack:
1. `convert_to_coreml()` → Returns detailed error dictionary
2. `download_whisper_model()` → Includes Core ML status in result
3. `whisper_model_install()` → Reports Core ML status to user/LLM

## Implementation

### Step 1: Modify `convert_to_coreml()` Function

Location: `/voice_mode/utils/services/whisper_helpers.py`

```python
async def convert_to_coreml(
    model: str,
    models_dir: Union[str, Path]
) -> Dict[str, Union[bool, str, Dict]]:
    """
    Convert Whisper model to Core ML format with detailed error reporting.
    
    Returns:
        Dict with:
        - success: bool
        - path: str (if successful)
        - error: str (if failed)
        - error_category: str (type of error)
        - error_details: dict (full error information)
        - install_command: str (how to fix)
        - log_location: str (where to find logs)
    """
```

Key changes:
- Return comprehensive error dictionary instead of simple success/error
- Detect specific error patterns in subprocess output
- Include remediation instructions

### Step 2: Update `download_whisper_model()` Function

Location: `/voice_mode/utils/services/whisper_helpers.py`

```python
async def download_whisper_model(
    model: str,
    models_dir: Union[str, Path],
    force_download: bool = False
) -> Dict[str, Union[bool, str, Dict]]:
    """
    Download model with Core ML status reporting.
    
    Returns:
        Dict with:
        - success: bool
        - path: str
        - message: str
        - core_ml_status: dict (detailed Core ML conversion result)
    """
```

Key changes:
- Always include `core_ml_status` in response
- Don't hide Core ML failures
- Log Core ML errors at appropriate level (ERROR not just WARNING)

### Step 3: Enhance `whisper_model_install()` Tool Response

Location: `/voice_mode/tools/services/whisper/model_install.py`

```python
@mcp.tool()
async def whisper_model_install(...) -> str:
    """
    Returns JSON with:
    {
        "success": bool,
        "models_directory": str,
        "results": [
            {
                "model": str,
                "download_success": bool,
                "core_ml_attempted": bool,
                "core_ml_success": bool,
                "core_ml_error": str,  # If failed
                "core_ml_fix": str,     # Installation command
                "acceleration": str,    # "coreml" or "metal"
            }
        ],
        "warnings": [str],  # List of warnings
        "recommendations": [str]  # Next steps for user
    }
    """
```

Key changes:
- Separate download success from Core ML success
- Include specific fix commands
- Add warnings section for important issues
- Provide clear recommendations

## Error Categories and Messages

### Missing Dependencies

#### `missing_pytorch`
```json
{
    "error_category": "missing_pytorch",
    "error": "PyTorch not installed - required for Core ML conversion",
    "install_command": "uv pip install torch",
    "recommendation": "Install PyTorch to enable Core ML acceleration"
}
```

#### `missing_coremltools`
```json
{
    "error_category": "missing_coremltools",
    "error": "Core ML Tools not installed",
    "install_command": "uv pip install coremltools",
    "recommendation": "Install Core ML Tools for model conversion"
}
```

#### `missing_whisper`
```json
{
    "error_category": "missing_whisper",
    "error": "OpenAI Whisper package not installed",
    "install_command": "uv pip install openai-whisper",
    "recommendation": "Install OpenAI Whisper for Core ML conversion"
}
```

#### `missing_ane_transformers`
```json
{
    "error_category": "missing_ane_transformers",
    "error": "ANE Transformers not installed",
    "install_command": "uv pip install ane_transformers",
    "recommendation": "Install ANE Transformers for Apple Neural Engine optimization"
}
```

### System Issues

#### `missing_xcode_tools`
```json
{
    "error_category": "missing_xcode_tools",
    "error": "Xcode Command Line Tools not installed",
    "install_command": "xcode-select --install",
    "recommendation": "Install Xcode Command Line Tools for Core ML compilation"
}
```

### Conversion Failures

#### `conversion_timeout`
```json
{
    "error_category": "conversion_timeout",
    "error": "Core ML conversion timed out after 10 minutes",
    "recommendation": "Try again or use smaller model"
}
```

#### `conversion_error`
```json
{
    "error_category": "conversion_error",
    "error": "Core ML conversion failed: <specific error>",
    "log_location": "~/.voicemode/logs/coreml_conversion.log",
    "recommendation": "Check logs for details. Model will use Metal acceleration."
}
```

## Testing Plan

1. **Test missing dependencies**
   - Remove torch, verify error message
   - Remove coremltools, verify error message
   - Remove all dependencies, verify combined fix command

2. **Test error propagation**
   - Verify errors appear in tool response
   - Verify LLM receives actionable information
   - Check log files contain full error details

3. **Test recovery suggestions**
   - Verify installation commands are correct
   - Verify recommendations are appropriate
   - Test that following recommendations fixes issues

## Success Metrics

1. **Error Clarity**: 100% of Core ML failures include specific error category
2. **Actionability**: 100% of dependency errors include exact fix command
3. **Visibility**: Core ML status always included in tool response
4. **Logging**: All errors logged with full context for debugging