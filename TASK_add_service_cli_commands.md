# Task: Add Service Management CLI Commands to Voice Mode

## Objective
Extend the voice-mode CLI to include service management commands that currently exist as MCP tools but would be useful as standalone CLI commands. These commands don't require the MCP server to be running, making them more accessible for system administration tasks.

## Background
The voice-mode package currently has two service subcommands (`kokoro` and `whisper`) with basic operations (start, stop, status, etc.). There are many additional MCP tools in the `voice_mode/tools/` directory that would be valuable as CLI commands for managing voice-mode services without needing to run the MCP server.

## Key Implementation Details

### 1. Add Short Option Support
Currently, CLI commands only support long options (e.g., `--help`). Add short options for better usability:
- `-h` for `--help`
- `-n` for `--lines` (in logs command)
- `-f` for `--force` (in install commands)
- etc.

### 2. New Commands to Add

#### Install/Uninstall Commands
Location: Under `kokoro` and `whisper` groups
- `kokoro install` - Install kokoro-fastapi service
- `kokoro uninstall` - Uninstall kokoro-fastapi service  
- `whisper install` - Install whisper.cpp service
- `whisper uninstall` - Uninstall whisper.cpp service

#### Model Management (Whisper only)
- `whisper download-model` - Download whisper models with Core ML support
- `whisper list-models` - List available models

#### Configuration Commands
New top-level group: `config`
- `config list` - List all configuration keys with descriptions
- `config get <key>` - Get a configuration value
- `config set <key> <value>` - Update a configuration value

#### Diagnostics Commands  
New top-level group: `diag` (or `diagnostics`)
- `diag info` - Show voice-mode installation info
- `diag devices` - List audio devices
- `diag registry` - Show provider registry
- `diag dependencies` - Check system dependencies

#### Version Management
Add to service groups:
- `kokoro version` - Show installed/available versions
- `whisper version` - Show installed/available versions
- `kokoro update` - Update to latest version
- `whisper update` - Update to latest version

### 3. Architecture Pattern

The existing pattern in `cli.py` is:
1. Import the async function from the tools module
2. Create a Click command that wraps it with `asyncio.run()`
3. Handle any command-line specific formatting

Example from existing code:
```python
@kokoro.command()
def status():
    """Show Kokoro service status."""
    result = asyncio.run(status_service("kokoro"))
    click.echo(result)
```

### 4. Important Considerations

#### Parameter Type Conversion
Many MCP tools accept `Union[bool, str]` parameters to handle both programmatic and string inputs. CLI commands should:
- Accept proper boolean flags for CLI (e.g., `--force/--no-force`)
- Convert to appropriate types before calling the underlying functions

#### Error Handling
- MCP tools often return Dict[str, Any] or structured responses
- CLI commands should format these nicely for terminal output
- Use click.echo() for consistent output
- Consider using click.style() for colored output on errors/success

#### Progress Feedback
Install commands can take time. Consider:
- Using click.progressbar() for long operations
- Providing verbose output options
- Showing real-time output from subprocess commands

#### Help Text Quality
- Keep help text concise but informative
- Include examples in docstrings where helpful
- Ensure consistency with existing commands

### 5. File Structure

Current structure:
```
voice_mode/
├── cli.py                    # Main CLI entry point
├── cli_commands/            
│   └── exchanges.py         # Legacy exchanges commands
└── tools/
    ├── services/
    │   ├── kokoro/
    │   │   ├── install.py
    │   │   └── uninstall.py
    │   └── whisper/
    │       ├── install.py
    │       ├── uninstall.py
    │       └── download_model.py
    ├── configuration_management.py
    ├── diagnostics.py
    └── devices.py
```

Recommended approach:
- Keep all CLI logic in `cli.py` for now (can refactor later if it gets too large)
- Import functions directly from tools modules
- Maintain existing naming conventions

### 6. Testing Considerations

- Test commands both with and without services installed
- Verify error messages are helpful
- Ensure commands work across platforms (Linux, macOS)
- Test parameter validation and edge cases

### 7. Priority Order

1. **High Priority** (most useful for users):
   - Install/uninstall commands
   - Model download for whisper
   - Configuration management

2. **Medium Priority**:
   - Diagnostics commands
   - Version management

3. **Low Priority** (nice to have):
   - Additional convenience commands

## Success Criteria

- [ ] All new CLI commands work without MCP server running
- [ ] Commands have both short and long options where appropriate  
- [ ] Error messages are clear and actionable
- [ ] Help text is comprehensive and consistent
- [ ] Commands follow existing patterns and conventions
- [ ] No breaking changes to existing commands

## Implementation Notes

- The existing service management functions in `tools/service.py` already handle the async/sync conversion well
- Many MCP tools can be reused directly with minimal wrapping
- Focus on user experience - make commands intuitive and helpful
- Consider adding a `--dry-run` option for destructive operations

## Code Locations for Reference

- CLI entry point: `voice_mode/cli.py`
- Service tools: `voice_mode/tools/services/`
- Config tools: `voice_mode/tools/configuration_management.py`
- Diagnostic tools: `voice_mode/tools/diagnostics.py`, `devices.py`
- Version helpers: `voice_mode/utils/version_helpers.py`