# Changelog

All notable changes to VoiceMode (formerly voice-mcp) will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [2.2.0] - 2025-06-22

### Added
- Configurable audio format support with Opus as the new default
- Environment variables for audio format configuration:
  - `VOICEMODE_AUDIO_FORMAT` - Primary format (default: opus)
  - `VOICEMODE_TTS_AUDIO_FORMAT` - TTS-specific override
  - `VOICEMODE_STT_AUDIO_FORMAT` - STT-specific override
- Support for multiple audio formats: opus, mp3, wav, flac, aac, pcm
- Format-specific quality settings:
  - `VOICEMODE_OPUS_BITRATE` (default: 32000)
  - `VOICEMODE_MP3_BITRATE` (default: 64k)
  - `VOICEMODE_AAC_BITRATE` (default: 64k)
- Automatic format validation based on provider capabilities
- Provider-aware format fallback logic
- Test suite for audio format configuration
- Streaming audio playback infrastructure:
  - `VOICEMODE_STREAMING_ENABLED` (default: true)
  - `VOICEMODE_STREAM_CHUNK_SIZE` (default: 4096)
  - `VOICEMODE_STREAM_BUFFER_MS` (default: 150)
  - `VOICEMODE_STREAM_MAX_BUFFER` (default: 2.0)
- TTFA (Time To First Audio) metric in timing output
- Per-request audio format override via `audio_format` parameter in conversation tools
- **Live Statistics Dashboard**: Comprehensive conversation performance tracking
  - Real-time performance metrics (TTFA, TTS generation, STT processing, total turnaround)
  - Session statistics (interaction counts, success rates, provider usage)
  - MCP tools: `voice_statistics`, `voice_statistics_summary`, `voice_statistics_recent`, `voice_statistics_reset`, `voice_statistics_export`
  - MCP resources: `voice://statistics/{type}`, `voice://statistics/summary/{format}`, `voice://statistics/export/{timestamp}`
  - Automatic integration with conversation tools - no manual tracking required
  - Thread-safe statistics collection across concurrent operations
  - Memory-efficient storage (maintains last 1000 interactions)

### Changed
- **BREAKING**: All `VOICE_MCP_` environment variables renamed to `VOICEMODE_`
  - `VOICE_MCP_DEBUG` → `VOICEMODE_DEBUG`
  - `VOICE_MCP_SAVE_AUDIO` → `VOICEMODE_SAVE_AUDIO`
  - `VOICE_MCP_AUDIO_FEEDBACK` → `VOICEMODE_AUDIO_FEEDBACK`
  - `VOICE_MCP_FEEDBACK_VOICE` → `VOICEMODE_FEEDBACK_VOICE`
  - `VOICE_MCP_FEEDBACK_MODEL` → `VOICEMODE_FEEDBACK_MODEL`
  - `VOICE_MCP_FEEDBACK_STYLE` → `VOICEMODE_FEEDBACK_STYLE`
  - `VOICE_MCP_PREFER_LOCAL` → `VOICEMODE_PREFER_LOCAL`
  - `VOICE_MCP_AUTO_START_KOKORO` → `VOICEMODE_AUTO_START_KOKORO`
- Also renamed non-prefixed variables to use `VOICEMODE_` prefix:
  - `VOICE_ALLOW_EMOTIONS` → `VOICEMODE_ALLOW_EMOTIONS`
  - `VOICE_EMOTION_AUTO_UPGRADE` → `VOICEMODE_EMOTION_AUTO_UPGRADE`
- Default audio format changed from MP3 to Opus for better compression and lower latency
- Audio format is now validated against provider capabilities before use
- Dynamic audio loading based on format instead of hardcoded MP3
- Centralized all configuration in `voice_mcp/config.py` to eliminate duplication
- Logger names updated from "voice-mcp" to "voicemode"
- Debug directory paths updated:
  - `~/voice-mcp_recordings/` → `~/voicemode_recordings/`
  - `~/voice-mcp_audio/` → `~/voicemode_audio/`

### Benefits
- 50-80% smaller audio files with Opus format
- Lower latency for real-time communication
- Better optimization for voice (vs music-focused MP3)
- Maintains backward compatibility with MP3
- Cleaner, consistent environment variable naming

### Fixed Issues
- ~~OpenAI TTS with Opus format produces poor audio quality~~ - **RESOLVED** (2025-06-22)
  - OpenAI now produces good quality audio with Opus format
  - See `docs/issues/openai-opus-audio-quality.md` for details

## [2.1.3] - 2025-06-20

## [2.1.2] - 2025-06-20

## [2.1.1] - 2025-06-20

### Fixed
- Fixed `voice_status` tool error where `get_provider_display_status` was called with incorrect arguments
- Updated `.mcp.json` to use local package installation with `--refresh` flag

### Added
- Audio feedback chimes for recording start/stop (inspired by PR #1 from @jtuffin)
- New `VOICE_MCP_AUDIO_FEEDBACK` configuration with options: `chime` (default), `voice`, `both`, `none`
- Backward compatibility for boolean audio feedback values

### Changed
- Replaced all references from `voice-mcp` to `voice-mode` throughout documentation
- Updated MCP configuration examples to use `uvx` instead of outdated `./mcp-servers/` directory
- Removed hardcoded version from `server_new.py`
- Changed default listen duration to 15 seconds (from 10s/20s) in all voice conversation functions for better balance
- Audio feedback now defaults to chimes instead of voice for faster, less intrusive feedback

## [2.1.0] - 2025-06-20

## [2.0.3] - 2025-06-20

## [2.0.2] - 2025-06-20

## [2.0.1] - 2025-06-20

### Changed
- Consolidated package structure from three to two pyproject.toml files
- Removed unpublishable `voicemode` package configuration
- Made `voice-mode` the primary package (in pyproject.toml)
- Moved `voice-mcp` to secondary configuration (pyproject-voice-mcp.toml)

### Added
- Documentation for local development with uvx (`docs/local-development-uvx.md`)

## [2.0.0] - 2025-06-20

### 🎉 Major Project Rebrand: VoiceMCP → VoiceMode

We're excited to announce that **voice-mcp** has been rebranded to **VoiceMode**! 

This change reflects our vision for the project's future. While MCP (Model Context Protocol) describes the underlying technology, VoiceMode better captures what this tool actually delivers - a seamless voice interaction mode for AI assistants.

#### Why the Change?
- **Clarity**: VoiceMode immediately communicates the tool's purpose
- **Timelessness**: The name isn't tied to a specific protocol that may evolve
- **Simplicity**: Easier to remember and more intuitive for users

#### What's Changed?
- Primary command renamed from `voice-mcp` to `voicemode`
- GitHub repository moved to `mbailey/voicemode`
- Primary PyPI package is now `voice-mode` (hyphenated due to naming restrictions)
- Legacy `voice-mcp` package maintained for backward compatibility
- Documentation and branding updated throughout
- Simplified package structure to dual-package configuration

#### Backward Compatibility
- The `voice-mcp` command remains available for existing users
- Both `voice-mode` and `voice-mcp` packages available on PyPI
- All packages provide the `voicemode` command

### Changed
- Consolidated package configuration to two pyproject.toml files
- Made `voice-mode` the primary package with VoiceMode branding
- Updated package descriptions to reflect the rebrand

### Added
- Local development documentation for uvx usage

## [0.1.30] - 2025-06-19

### Added
- Audio feedback with whispered responses by default
- Configurable audio feedback style (whisper or shout) via VOICE_MCP_FEEDBACK_STYLE environment variable
- Support for overriding audio feedback settings per conversation

## [0.1.29] - 2025-06-17

### Changed
- Refactored MCP prompt names to use kebab-case convention (kokoro-start, kokoro-stop, kokoro-status, voice-status)
- Renamed Kokoro tool functions to follow consistent naming pattern (start_kokoro → kokoro_start, stop_kokoro → kokoro_stop)

## [0.1.28] - 2025-06-17

### Added
- MCP prompts for Kokoro TTS management:
  - `kokoro-start` - Start the local Kokoro TTS service
  - `kokoro-stop` - Stop the local Kokoro TTS service
  - `kokoro-status` - Check the status of Kokoro service
  - `voice-status` - Check comprehensive status of all voice services
- Instructions in CLAUDE.md for AI assistants on when to use Kokoro tools

## [0.1.27] - 2025-06-17

### Added
- Voice chat prompt/command (`/voice-mcp:converse`) for interactive voice conversations
- Automatic local provider preference with VOICE_MCP_PREFER_LOCAL environment variable
- Documentation improvements with better organization and cross-linking

### Changed
- Renamed voice_chat prompt to converse for clarity
- Simplified voice_chat prompt to take no arguments


## [0.1.26] - 2025-06-17

### Fixed
- Added missing voice_mode() function to cli.py for voice-mode command

## [0.1.25] - 2025-06-17

### Added
- Build tooling improvements for dual package maintenance

### Fixed
- Missing psutil dependency in voice-mode package

## [0.1.24] - 2025-06-17

### Fixed
- Improved signal handling for proper Ctrl-C shutdown
  - First Ctrl-C attempts graceful shutdown
  - Second Ctrl-C forces immediate exit

## [0.1.23] - 2025-06-17

### Added
- Provider registry system MVP for managing TTS/STT providers
  - Dynamic provider discovery and registration
  - Automatic availability checking
  - Feature-based provider filtering
- Dual package name support (voice-mcp and voice-mode)
  - Both commands now available in voice-mode package
  - Maintains backward compatibility
- Service management tools for Kokoro TTS:
  - `start_kokoro` - Start the Kokoro TTS service using uvx
  - `stop_kokoro` - Stop the running Kokoro service
  - `kokoro_status` - Check service status with CPU/memory usage
- Automatic cleanup of services on server shutdown
- psutil dependency for process monitoring
- `list_tts_voices` tool to list all available TTS voices by provider
  - Shows OpenAI standard and enhanced voices with characteristics
  - Lists Kokoro voices with descriptions
  - Includes usage examples and emotional speech guidance
  - Checks API/service availability for each provider

### Changed
- Default TTS voices updated: alloy for OpenAI, af_sky for Kokoro

## [0.1.22] - 2025-06-16

### Added
- Local STT/TTS configuration support in .mcp.json
- Split TTS metrics into generation and playback components for better performance insights
  - Tracks TTS generation time (API call) separately from playback time
  - Displays metrics as tts_gen, tts_play, and tts_total

### Changed
- Modified text_to_speech() to return (success, metrics) tuple
- Updated all tests to handle new TTS return format

## [0.1.21] - 2025-06-16

### Added
- VOICE_MCP_SAVE_AUDIO environment variable to save all TTS/STT audio files
- Audio files saved to ~/voice-mcp_audio/ with timestamps
- Improved voice selection documentation and guidance

### Changed
- Voice parameter changed from Literal to str for flexibility in voice selection


## [0.1.19] - 2025-06-15

### Added
- TTS provider selection parameter to converse function ("openai" or "kokoro")
- Auto-detection of TTS provider based on voice selection
- Support for multiple TTS endpoints with provider-specific clients

## [0.1.18] - 2025-06-15

### Changed
- Removed mcp-neovim-server from .mcp.json configuration

## [0.1.17] - 2025-06-15

### Changed
- Minor version bump (no functional changes)

## [0.1.16] - 2025-06-15

## [0.1.16] - 2025-06-15

### Added
- Voice parameter to converse function for dynamic TTS voice selection
- Support for Kokoro voices: af_sky, af_sarah, am_adam, af_nicole, am_michael
- Python 3.13 support with conditional audioop-lts dependency

### Fixed
- BrokenResourceError when concurrent voice operations interfere with MCP stdio communication
- Enhanced sounddevice stderr redirection workaround to prevent stdio corruption
- Added concurrency lock to serialize audio operations and prevent race conditions
- Protected stdio file descriptors during audio recording and playback operations
- Added anyio.BrokenResourceError to exception handling for MCP disconnections
- Configure pytest to exclude manual test scripts from CI builds

## [0.1.15] - 2025-06-14

### Fixed
- Removed load_dotenv call that was causing import error

## [0.1.14] - 2025-06-14

### Fixed
- Updated GitHub workflows for new project structure

## [0.1.13] - 2025-06-14

### Added
- Performance timing in voice responses showing TTS, recording, and STT durations
- Local STT/TTS documentation for Whisper.cpp and Kokoro
- CONTRIBUTING.md with development setup instructions
- CHANGELOG.md for tracking changes

### Changed
- Refactored from python-package subdirectory to top-level Python package
- Moved MCP server symlinks from mcp-servers/ to bin/ directory
- Updated wrapper script to properly resolve symlinks for venv detection
- Improved signal handlers to prevent premature exit
- Configure build to only include essential files in package

### Fixed
- Audio playback dimension mismatch when adding silence buffer
- MCP server connection persistence (was disconnecting after each request)
- Event loop cleanup errors on shutdown
- Wrapper script path resolution for symlinked execution
- Critical syntax errors in voice-mcp script

### Removed
- Unused python-dotenv dependency
- Temporary test files (test_audio.py, test_minimal_mcp.py)
- Redundant test dependencies in pyproject.toml
- All container/Docker support

## [0.1.12] - 2025-06-14

### Added
- Kokoro TTS support with configuration examples
- Export examples in .env.example for various setups
- Centralized version management and automatic PyPI publishing

### Changed
- Simplified project structure with top-level package

## [0.1.11] - 2025-06-13

### Added
- Initial voice-mcp implementation
- OpenAI-compatible STT/TTS support
- LiveKit integration for room-based voice communication
- MCP tool interface with converse, listen_for_speech, check_room_status, and check_audio_devices
- Debug mode with audio recording capabilities
- Support for multiple transport methods (local microphone and LiveKit)

## [0.1.0 - 0.1.10] - 2025-06-13

### Added
- Initial development and iteration of voice-mcp
- Basic MCP server structure
- OpenAI API integration for STT/TTS
- Audio recording and playback functionality
- Configuration via environment variables
