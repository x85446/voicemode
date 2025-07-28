# Fix /tmp Multi-User Permission Issues

## Problem Statement

Voice Mode writes files to `/tmp` which causes permission errors when multiple users run voice-mode on the same system. When user "cora" creates a file in `/tmp`, user "m" cannot write to or modify it.

### Reported Errors

1. **voicemode_silence_debug.txt**
   - Error: `[Errno 13] Permission denied: '/tmp/voicemode_silence_debug.txt'`
   - Created by silence detection debugging code

2. **voicemode_vad_import.txt** 
   - Error: `PermissionError: [Errno 13] Permission denied: '/tmp/voicemode_vad_import.txt'`
   - Referenced in error log but not found in current codebase

## Analysis of /tmp Usage

### Direct /tmp References Found

1. **README.md** - Docker example only (not an issue)
   ```bash
   -v /tmp/.X11-unix:/tmp/.X11-unix
   ```

2. **Test files** - Use tempfile module correctly
   - `test_conversation_browser_playback.py`: `tempfile.mkdtemp(prefix="voicemode_test_")`
   - Multiple test files use `tempfile.NamedTemporaryFile()`

3. **Core functionality** - Use tempfile module correctly
   - `core.py`: `tempfile.NamedTemporaryFile(suffix=f'.{validated_format}', delete=False)`
   - `streaming.py`: `tempfile.NamedTemporaryFile(suffix='.wav', delete=False)`
   - `converse.py`: Multiple uses of `tempfile.NamedTemporaryFile()`

### Missing/Hidden /tmp Usage

The following files are creating hardcoded `/tmp` paths but weren't found in the current search:
- `/tmp/voicemode_silence_debug.txt` - Silence detection debug
- `/tmp/voicemode_vad_import.txt` - VAD import tracking

These may be:
1. In an older version of the code
2. Created by a dependency
3. In a file that's generated at runtime

## Recommendations

### 1. User-Specific Directory Structure

Create a proper directory structure under the user's home:

```
~/.voicemode/
├── temp/           # Temporary files (cleaned periodically)
├── debug/          # Debug output files
├── recordings/     # Audio recordings (already exists)
├── logs/           # Log files (already exists)
└── cache/          # Cached data
```

### 2. Implementation Plan

1. **Create utility function for temp files**
   ```python
   def get_user_temp_dir():
       """Get user-specific temp directory, creating if needed."""
       temp_dir = Path.home() / '.voicemode' / 'temp'
       temp_dir.mkdir(parents=True, exist_ok=True)
       return temp_dir
   
   def get_debug_file_path(filename):
       """Get path for debug file in user directory."""
       debug_dir = Path.home() / '.voicemode' / 'debug'
       debug_dir.mkdir(parents=True, exist_ok=True)
       return debug_dir / filename
   ```

2. **Update all hardcoded /tmp paths**
   - Find and replace any hardcoded `/tmp/voicemode_*` paths
   - Use the utility functions instead

3. **Configure tempfile to use user directory**
   ```python
   # Set tempfile to use our directory
   import tempfile
   tempfile.tempdir = str(get_user_temp_dir())
   ```

4. **Add cleanup mechanism**
   - Clean temp files older than 24 hours on startup
   - Provide `voice-mode --clean-temp` command

### 3. Benefits

- **Multi-user safe**: Each user has their own directory
- **Better organization**: Debug, temp, and recordings separated
- **Easier debugging**: User can find their files easily
- **Follows conventions**: Uses standard ~/.voicemode location
- **Backwards compatible**: tempfile module still works

### 4. Migration Steps

1. Search entire codebase for hardcoded /tmp paths
2. Create utility module for temp file management
3. Update all file creation to use new paths
4. Add startup check to create directories
5. Add cleanup functionality
6. Test with multiple users

## Action Items

- [ ] Find source of `/tmp/voicemode_silence_debug.txt` creation
- [ ] Find source of `/tmp/voicemode_vad_import.txt` creation  
- [ ] Create `voice_mode/utils/paths.py` module
- [ ] Update all temp file creation
- [ ] Add tests for multi-user scenarios
- [ ] Update documentation