# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

VoiceMode is a Python package that provides voice interaction capabilities for AI assistants through the Model Context Protocol (MCP). It enables natural voice conversations with Claude Code and other AI coding assistants by integrating speech-to-text (STT) and text-to-speech (TTS) services.

## Key Commands

### Development & Testing
```bash
# Install in development mode with dependencies
make dev-install

# Run all unit tests
make test
# Or directly: uv run pytest tests/ -v --tb=short

# Run specific test
uv run pytest tests/test_voice_mode.py -v

# Run tests by type
make test-unit        # Unit tests only
make test-integration # Integration tests only
make test-all        # All tests including slow/manual
make test-parallel   # Run tests in parallel with pytest-xdist

# Coverage reports
make coverage        # Run tests with coverage, opens HTML report
make coverage-html   # Open HTML coverage report
make coverage-xml    # Generate XML coverage for CI

# Clean build artifacts
make clean
```

### Configuration Management
```bash
# Edit configuration file in default editor
voicemode config edit

# Or specify a different editor
voicemode config edit --editor vim
voicemode config edit --editor "code --wait"

# List available configuration keys
voicemode config list

# Get a specific configuration value
voicemode config get VOICEMODE_TTS_VOICE

# Set a configuration value
voicemode config set VOICEMODE_TTS_VOICE nova
```

### Building & Publishing
```bash
# Build Python package
make build-package

# Build development version (auto-versioned with .devYYYYMMDDHHMMSS suffix)
make build-dev

# Test package installation
make test-package

# Release workflow - comprehensive automation:
# 1. Prompts for new version
# 2. Updates voice_mode/__version__.py, server.json, CHANGELOG.md
# 3. Creates git commit and tag
# 4. Pushes to GitHub triggering CI/CD
make release
```

### Documentation
```bash
# Serve docs locally at http://localhost:8000
make docs-serve

# Build documentation site
make docs-build

# Check docs for errors (strict mode)
make docs-check
```

### Development Environment
```bash
# Generate CLAUDE.md from template with consolidated context
make CLAUDE.md

# Prepare environment and start Claude Code interactive session
make claude
```

## Architecture Overview

### Core Components

1. **MCP Server (`voice_mode/server.py`)**
   - FastMCP-based server providing voice tools via stdio transport
   - Auto-imports all tools, prompts, and resources
   - Handles FFmpeg availability checks and logging setup

2. **Tool System (`voice_mode/tools/`)**
   - **converse.py**: Primary voice conversation tool with TTS/STT integration
   - **service.py**: Unified service management for Whisper/Kokoro/LiveKit
   - **providers.py**: Provider discovery and registry management
   - **devices.py**: Audio device detection and management
   - Services subdirectory contains install/uninstall tools for Whisper, Kokoro, and LiveKit
   - **Tool Loading Modes**: Control which tools are loaded via environment variables:
     - `VOICEMODE_TOOLS_ENABLED`: Whitelist mode - only load specified tools
     - `VOICEMODE_TOOLS_DISABLED`: Blacklist mode - load all except specified tools
     - Tools auto-imported from directory structure at runtime

3. **Provider System (`voice_mode/providers.py`)**
   - Dynamic discovery of OpenAI-compatible TTS/STT endpoints
   - Health checking and failover support
   - Maintains registry of available voice services

4. **Configuration (`voice_mode/config.py`)**
   - Environment-based configuration with sensible defaults
   - Support for voice preference files (project/user level)
   - Audio format configuration (PCM, MP3, WAV, FLAC, AAC, Opus)

5. **Resources (`voice_mode/resources/`)**
   - MCP resources exposed for client access
   - Statistics, configuration, changelog, and version information
   - Whisper model management

6. **Frontend (`voice_mode/frontend/`)**
   - Next.js-based web interface for LiveKit integration
   - Real-time voice conversation UI
   - Built and bundled with the Python package
   - **Build Hook System**: Automatic frontend compilation during package build:
     - Auto-detects Node.js and builds frontend if available
     - Control via `BUILD_FRONTEND` env var (true/false/auto)
     - Graceful fallback if frontend build fails

### Service Architecture

The project supports multiple voice service backends:
- **OpenAI API**: Cloud-based TTS/STT (requires API key)
- **Whisper.cpp**: Local speech-to-text service
- **Kokoro**: Local text-to-speech with multiple voices
- **LiveKit**: Room-based real-time communication

Services can be installed and managed through MCP tools, with automatic service discovery and health checking.

### Key Design Patterns

1. **OpenAI API Compatibility**: All voice services expose OpenAI-compatible endpoints, enabling transparent switching between providers
2. **Dynamic Tool Discovery**: Tools are auto-imported from the tools directory structure
3. **Failover Support**: Automatic fallback between services based on availability
4. **Transport Flexibility**: Supports both local microphone and LiveKit room-based communication
5. **Audio Format Negotiation**: Automatic format validation against provider capabilities

## Development Notes

- The project uses `uv` for package management (not pip directly)
- Python 3.10+ is required
- FFmpeg is required for audio processing
- The project follows a modular architecture with FastMCP patterns
- Service installation tools handle platform-specific setup (launchd on macOS, systemd on Linux)
- Event logging and conversation logging are available for debugging
- WebRTC VAD is used for silence detection when available
- Configuration precedence: Project `.voicemode.env` > User config > Environment > Defaults
- WSL2 requires additional audio packages (pulseaudio, libasound2-plugins) for microphone access

## Testing Approach

- Unit tests are in the `tests/` directory
- Manual tests requiring user interaction are in `tests/manual/`
- Use `pytest` for running tests, with fixtures for mocking external services
- Integration tests verify service discovery and provider selection
- The project includes comprehensive test coverage for configuration, providers, and tools
- **Test Markers**: Use pytest markers to run specific test types:
  - `@pytest.mark.unit`: Fast unit tests
  - `@pytest.mark.integration`: Integration tests with external dependencies
  - `@pytest.mark.slow`: Tests that take significant time
  - `@pytest.mark.manual`: Tests requiring user interaction

## Logging

VoiceMode maintains comprehensive logs in the `~/.voicemode/` directory:

```
~/.voicemode/
├── logs/
│   ├── conversations/     # JSONL files with daily conversation exchanges
│   │   └── exchanges_YYYY-MM-DD.jsonl
│   ├── events/           # JSONL files with detailed event logs
│   │   └── voicemode_events_YYYY-MM-DD.jsonl
│   └── debug/            # Debug logs when debug mode is enabled
├── audio/                # Saved audio recordings organized by date
│   └── YYYY/MM/         # TTS and STT audio files (.wav format)
├── config/               # User configuration files
│   ├── config.yaml       # Main configuration
│   └── pronunciation.yaml # Custom pronunciation rules
└── services/             # Installed voice services (Whisper, Kokoro, LiveKit)
    ├── whisper/         # Whisper.cpp installation and models
    ├── kokoro/          # Kokoro TTS service
    └── livekit/         # LiveKit server and agents
```

### Log Types

- **Conversation Logs** (`logs/conversations/`): Records of voice exchanges including timestamps, text, and metadata
- **Event Logs** (`logs/events/`): Detailed operational events including TTS/STT operations, errors, and provider selection
- **Audio Recordings** (`audio/`): Saved TTS outputs and STT inputs for debugging and review
- **Debug Logs** (`logs/debug/`): Verbose debugging information when running with `--debug` flag

## CI/CD Pipeline

GitHub Actions workflows handle automation:
- **create-release.yml**: Automated release creation from tags
- **publish-pypi-and-mcp.yml**: Package publishing to PyPI and MCP registry
- **test.yml**: Test suite execution on push/PR
- **test-installer.yml**: Installer script testing across platforms
- **deploy-pages.yml**: Documentation deployment to GitHub Pages
- **deploy-worker.yml**: Worker deployment for services

## Critical Files for Development

- **`voice_mode/tools/__init__.py`**: Tool loading and discovery logic
- **`build_hooks.py`**: Custom build hooks for frontend compilation
- **`voice_mode/config.py`**: Configuration management system
- **`voice_mode/cli.py`**: CLI command definitions
- **`voice_mode/server.py`**: MCP server setup and initialization
- **`server.json`**: MCP server manifest with tool definitions
- **`.voicemode.env`**: Project-level configuration overrides