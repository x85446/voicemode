# Implementation Plan: Fix /tmp Multi-User Issues

## Summary of Findings

### Current /tmp Usage

1. **Proper tempfile usage** (No changes needed):
   - `core.py`: Uses `tempfile.NamedTemporaryFile()` for TTS audio processing
   - `streaming.py`: Uses `tempfile.NamedTemporaryFile()` for audio streaming
   - `converse.py`: Uses `tempfile.NamedTemporaryFile()` for STT processing
   - All test files: Use `tempfile` module correctly

2. **Problematic hardcoded paths** (Need fixing):
   - `/tmp/voicemode_silence_debug.txt` - Not found in current code
   - `/tmp/voicemode_vad_import.txt` - Not found in current code

These files appear to be created by:
- An older version of the code
- Runtime-generated code
- A dependency that's creating debug files

## Implementation Steps

### Step 1: Create Path Utilities Module

Create `voice_mode/utils/paths.py`:

```python
"""User-specific path utilities for Voice Mode."""
import os
from pathlib import Path
import tempfile
from typing import Optional

def get_voicemode_dir() -> Path:
    """Get the main voicemode directory."""
    base_dir = Path.home() / '.voicemode'
    base_dir.mkdir(exist_ok=True)
    return base_dir

def get_user_temp_dir() -> Path:
    """Get user-specific temp directory."""
    temp_dir = get_voicemode_dir() / 'temp'
    temp_dir.mkdir(exist_ok=True)
    return temp_dir

def get_debug_dir() -> Path:
    """Get user-specific debug directory."""
    debug_dir = get_voicemode_dir() / 'debug'
    debug_dir.mkdir(exist_ok=True)
    return debug_dir

def get_cache_dir() -> Path:
    """Get user-specific cache directory."""
    cache_dir = get_voicemode_dir() / 'cache'
    cache_dir.mkdir(exist_ok=True)
    return cache_dir

def configure_tempfile():
    """Configure tempfile to use user-specific directory."""
    # Only set if not already configured
    if tempfile.gettempdir() == '/tmp':
        tempfile.tempdir = str(get_user_temp_dir())

def cleanup_old_files(max_age_hours: int = 24):
    """Clean up old temporary files."""
    import time
    temp_dir = get_user_temp_dir()
    cutoff_time = time.time() - (max_age_hours * 3600)
    
    for file_path in temp_dir.iterdir():
        if file_path.is_file():
            if file_path.stat().st_mtime < cutoff_time:
                try:
                    file_path.unlink()
                except OSError:
                    pass  # File in use, skip
```

### Step 2: Update Core Initialization

Add to `voice_mode/__init__.py` or early initialization:

```python
from .utils.paths import configure_tempfile, cleanup_old_files

# Configure on import
configure_tempfile()

# Optional: cleanup old files on startup
try:
    cleanup_old_files()
except Exception:
    pass  # Don't fail on cleanup errors
```

### Step 3: Find and Fix Hardcoded Paths

Since the problematic files aren't in the current codebase, we need to:

1. **Add defensive code** to handle the case where these files exist:
   ```python
   # Check if running as different user
   import os
   import pwd
   
   def check_tmp_permissions():
       """Check for permission issues with /tmp files."""
       problem_files = [
           '/tmp/voicemode_silence_debug.txt',
           '/tmp/voicemode_vad_import.txt'
       ]
       
       current_user = pwd.getpwuid(os.getuid()).pw_name
       
       for filepath in problem_files:
           if os.path.exists(filepath):
               stat = os.stat(filepath)
               owner = pwd.getpwuid(stat.st_uid).pw_name
               if owner != current_user:
                   # Try to remove or rename
                   try:
                       os.unlink(filepath)
                   except PermissionError:
                       print(f"Warning: {filepath} owned by {owner}, may cause issues")
   ```

2. **Search for runtime file creation**:
   - Check if any dependencies are creating these files
   - Add logging to track file creation

3. **Potential sources to investigate**:
   - VAD (Voice Activity Detection) imports
   - Silence detection code
   - Debug mode initialization

### Step 4: Update Debug File Creation

Ensure all debug files use the new paths:

```python
# Instead of hardcoded /tmp paths
debug_file = '/tmp/voicemode_debug.txt'

# Use
from voice_mode.utils.paths import get_debug_dir
debug_file = get_debug_dir() / 'voicemode_debug.txt'
```

### Step 5: Add Environment Variable Support

Allow users to override the base directory:

```python
def get_voicemode_dir() -> Path:
    """Get the main voicemode directory."""
    # Allow override via environment variable
    base_dir = os.environ.get('VOICEMODE_HOME')
    if base_dir:
        base_dir = Path(base_dir)
    else:
        base_dir = Path.home() / '.voicemode'
    
    base_dir.mkdir(exist_ok=True)
    return base_dir
```

### Step 6: Testing

1. **Multi-user test**:
   ```bash
   # As user1
   uvx voice-mode
   
   # As user2
   uvx voice-mode
   
   # Verify no permission errors
   ```

2. **Temp file cleanup test**:
   ```python
   # Create old files
   # Run cleanup
   # Verify removal
   ```

3. **Permission test**:
   ```python
   # Create files with different permissions
   # Verify handling
   ```

## Migration Guide

For users upgrading:

1. Old temp files in `/tmp` can be manually removed
2. New files will be created in `~/.voicemode/temp/`
3. Debug files will be in `~/.voicemode/debug/`
4. No action required for most users

## Benefits

1. **Multi-user safe**: Each user has isolated directories
2. **Better organization**: Clear separation of file types
3. **Easier debugging**: Users know where to find their files
4. **Standard location**: Follows Unix conventions
5. **Configurable**: Can override with environment variables