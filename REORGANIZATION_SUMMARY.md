# Voice-MCP Reorganization Summary

## Overview

This document summarizes the reorganization of voice-mcp to follow the patterns observed in metool-mcp, using FastMCP's decorator-based registration system.

## Key Patterns from metool-mcp

1. **Directory Structure**: Separate directories for `tools/`, `prompts/`, and `resources/`
2. **Auto-registration**: Using FastMCP decorators (`@mcp.tool()`, `@mcp.prompt()`, `@mcp.resource()`)
3. **Feature-based Files**: Grouping related functionality (e.g., all repo-related tools in `repos.py`)
4. **Central Server File**: Simple `server.py` that creates MCP instance and imports all components
5. **Clean Separation**: Each directory has an `__init__.py` that imports all modules

## New Structure Created

```
voice_mcp/
├── server_new.py          # New FastMCP-based server entry point
├── shared.py              # Shared configuration and utilities
├── tools/                 # Tool implementations
│   ├── __init__.py
│   ├── voice_capture.py   # converse(), listen_for_speech()
│   ├── transcription.py   # STT tools (placeholder)
│   ├── synthesis.py       # TTS tools (placeholder)
│   ├── livekit.py         # LiveKit integration
│   ├── services.py        # Service management (kokoro_start/stop/status)
│   └── devices.py         # Audio devices & voice_status, list_tts_voices
├── prompts/               # Prompt definitions
│   ├── __init__.py
│   └── voice_commands.py  # voice_setup, emotional_speech_guide
└── resources/             # Resource providers
    ├── __init__.py
    └── audio_files.py     # Access to saved/debug audio files
```

## Migration Status

### Completed
- Created new directory structure
- Created `server_new.py` following metool pattern
- Created `shared.py` for common configuration
- Partially migrated tools:
  - `voice_capture.py`: Contains `converse()` and `listen_for_speech()` (needs helper functions)
  - `services.py`: Contains kokoro management tools
  - `devices.py`: Contains device listing and status tools
  - `livekit.py`: Placeholder with basic structure
- Created example prompts in `voice_commands.py`
- Created example resources in `audio_files.py`

### Still Needed
1. **Complete Tool Migration**: 
   - Move remaining helper functions from `server.py` to appropriate modules
   - Implement placeholders in `transcription.py` and `synthesis.py`
   - Complete LiveKit tools in `livekit.py`

2. **Update Imports**: 
   - The new tools reference functions from the old `server.py` that need to be properly relocated
   - Update import paths throughout the codebase

3. **Testing**: 
   - Test the new structure to ensure all tools work correctly
   - Verify decorator registration is working

4. **Cleanup**:
   - Remove old `server.py` once migration is complete
   - Update `__main__.py` to use new server
   - Update any documentation

## Benefits of New Structure

1. **Better Organization**: Tools are grouped by functionality rather than in one large file
2. **Easier Maintenance**: Each file has a clear purpose and scope
3. **Scalability**: Easy to add new tools/prompts/resources in appropriate files
4. **Cleaner Code**: Follows established MCP patterns from metool
5. **Auto-registration**: No need to manually register tools, just use decorators

## Next Steps

To complete the migration:
1. Move helper functions to appropriate shared modules
2. Update all import statements
3. Test the new server with `python -m voice_mcp.server_new`
4. Once verified, replace the old server.py
5. Update documentation to reflect new structure