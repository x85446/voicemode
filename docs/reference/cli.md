# CLI Command Reference

Complete reference for all VoiceMode command-line interface commands.

## Global Options

```bash
voice-mode [OPTIONS] COMMAND [ARGS]...

Options:
  --version              Show version and exit
  --help                 Show help message and exit
  --debug                Enable debug output
  --config FILE          Path to config file
```

## Core Commands

### voice-mode (default)
Start the MCP server
```bash
voice-mode
```

### converse
Start an interactive voice conversation
```bash
voice-mode converse [OPTIONS]

Options:
  --voice TEXT          Override TTS voice
  --model TEXT          Override TTS model
  --debug               Enable debug mode
  --skip-tts            Text-only output
  --timeout INTEGER     Recording timeout in seconds
```

### transcribe
Transcribe audio from stdin
```bash
echo "Hello" | voice-mode transcribe
voice-mode transcribe < audio.wav
```

## Service Management

### whisper
Manage Whisper STT service

```bash
# Installation and setup
voice-mode whisper install [--model MODEL]
voice-mode whisper uninstall

# Service control
voice-mode whisper start
voice-mode whisper stop
voice-mode whisper restart
voice-mode whisper status

# Service management
voice-mode whisper enable    # Start at boot
voice-mode whisper disable   # Don't start at boot

# Model management
voice-mode whisper models                    # List available models
voice-mode whisper model active             # Show active model
voice-mode whisper model active MODEL       # Set active model
voice-mode whisper model install MODEL      # Install specific model
voice-mode whisper model remove MODEL       # Remove model

# Logs and debugging
voice-mode whisper logs [--follow]
```

Available models:
- tiny, tiny.en (39 MB)
- base, base.en (142 MB)
- small, small.en (466 MB)
- medium, medium.en (1.5 GB)
- large-v1, large-v2, large-v3 (2.9-3.1 GB)
- large-v3-turbo (1.6 GB)

### kokoro
Manage Kokoro TTS service

```bash
# Installation and setup
voice-mode kokoro install
voice-mode kokoro uninstall

# Service control
voice-mode kokoro start
voice-mode kokoro stop
voice-mode kokoro restart
voice-mode kokoro status

# Service management
voice-mode kokoro enable
voice-mode kokoro disable

# Information
voice-mode kokoro voices     # List available voices
voice-mode kokoro logs [--follow]
```

### livekit
Manage LiveKit server

```bash
# Installation and setup
voice-mode livekit install
voice-mode livekit uninstall [--remove-all-data]

# Service control
voice-mode livekit start
voice-mode livekit stop
voice-mode livekit restart
voice-mode livekit status

# Service management
voice-mode livekit enable
voice-mode livekit disable

# Configuration
voice-mode livekit update    # Update service files
voice-mode livekit logs [--follow]
```

### frontend
Manage Voice Assistant Frontend

```bash
# Service control
voice-mode frontend start
voice-mode frontend stop
voice-mode frontend status

# Service management
voice-mode frontend enable
voice-mode frontend disable

# Utilities
voice-mode frontend open     # Open in browser
voice-mode frontend logs [--follow]
voice-mode frontend build    # Build frontend
```

### service
Unified service management

```bash
# Generic service commands
voice-mode service SERVICE COMMAND

Examples:
voice-mode service whisper status
voice-mode service kokoro start
voice-mode service livekit enable

Supported services:
- whisper
- kokoro
- livekit
- frontend
```

## Configuration Commands

### config
Manage configuration

```bash
# Show current configuration
voice-mode config show

# Initialize default config
voice-mode config init

# Test configuration
voice-mode config test

# Edit configuration
voice-mode config edit
```

### audio
Audio device management

```bash
# List audio devices
voice-mode audio devices

# Test audio recording
voice-mode audio test [--duration SECONDS]

# Select audio device
voice-mode audio select
```

## Development Commands

### test
Run tests

```bash
# Run all tests
voice-mode test

# Test specific component
voice-mode test whisper
voice-mode test kokoro
voice-mode test audio

# Test with coverage
voice-mode test --coverage
```

### build
Build package

```bash
# Build distribution packages
voice-mode build

# Build with specific version
voice-mode build --version 2.3.0

# Build development version
voice-mode build --dev
```

### logs
View VoiceMode logs

```bash
# View recent logs
voice-mode logs

# Follow logs in real-time
voice-mode logs --follow

# View last N lines
voice-mode logs --tail 50

# Filter by level
voice-mode logs --level error
```

## Utility Commands

### version
Show version information

```bash
voice-mode version

# Verbose output
voice-mode version --verbose
```

### doctor
Check system configuration

```bash
voice-mode doctor

# Checks:
# - Python version
# - Dependencies
# - Service status
# - API connectivity
# - Audio devices
```

### clean
Clean up temporary files

```bash
# Clean cache and temp files
voice-mode clean

# Clean everything including logs
voice-mode clean --all

# Dry run (show what would be deleted)
voice-mode clean --dry-run
```

## Environment Variables

Commands respect environment variables for configuration:

```bash
# Use specific API key
OPENAI_API_KEY=sk-... voice-mode converse

# Enable debug mode
VOICEMODE_DEBUG=true voice-mode

# Use local services
VOICEMODE_TTS_BASE_URLS=http://localhost:8880/v1 voice-mode converse
```

## Exit Codes

- 0: Success
- 1: General error
- 2: Command line syntax error
- 3: Service not running
- 4: Service already running
- 5: Permission denied
- 127: Command not found

## Examples

### Basic Usage
```bash
# Start MCP server
voice-mode

# Have a conversation
voice-mode converse

# Transcribe audio file
voice-mode transcribe < recording.wav
```

### Service Setup
```bash
# Full local setup
voice-mode whisper install
voice-mode kokoro install
voice-mode whisper enable
voice-mode kokoro enable
```

### Development
```bash
# Debug mode with all saves
VOICEMODE_DEBUG=true VOICEMODE_SAVE_ALL=true voice-mode converse

# Test local changes
uvx --from . voice-mode

# Check everything is working
voice-mode doctor
```

### Troubleshooting
```bash
# Check what's running
voice-mode whisper status
voice-mode kokoro status

# View logs
voice-mode logs --tail 100
voice-mode whisper logs --follow

# Clean and restart
voice-mode clean
voice-mode whisper restart
```