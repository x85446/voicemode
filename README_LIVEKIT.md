# LiveKit Integration for Voice Mode

Voice Mode now includes comprehensive LiveKit integration for real-time voice conversations through a web interface.

## Quick Start

```bash
# Install and start LiveKit server
voice-mode livekit install
voice-mode livekit start

# Start the voice assistant frontend
voice-mode frontend start
voice-mode frontend open  # Opens http://localhost:3000
```

**Default login**: Password is `voicemode123`

## What's Included

### 🚀 LiveKit Server Management
- Automatic installation for macOS and Linux
- Development configuration with auto-room creation
- Service management (systemd/launchd integration)
- Unified CLI with status, start, stop, enable, disable commands

### 🌐 Voice Assistant Frontend
- Web-based interface for voice conversations
- Bundled with Voice Mode Python package
- Automatic dependency management (npm/pnpm/yarn)
- Service lifecycle management
- Real-time voice chat with AI agents

### 🔧 Service Integration
- All services managed through unified `voice-mode service` command
- Status monitoring with CPU/memory usage
- Comprehensive logging and troubleshooting
- MCP tools for programmatic control

## Services Overview

| Service | Port | Purpose | Commands |
|---------|------|---------|----------|
| `livekit` | 7880 | Real-time communication server | `start`, `stop`, `status`, `enable`, `disable` |
| `frontend` | 3000 | Voice assistant web interface | `start`, `stop`, `status`, `enable`, `logs`, `open` |

## Commands

### LiveKit Server
```bash
voice-mode livekit install    # Install server binary
voice-mode livekit start      # Start server
voice-mode livekit status     # Check status
voice-mode livekit enable     # Auto-start at boot
voice-mode livekit logs       # View logs
```

### Frontend
```bash
voice-mode frontend start     # Start web interface
voice-mode frontend open      # Open in browser
voice-mode frontend status    # Check status
voice-mode frontend logs -f   # Follow logs
voice-mode frontend enable    # Auto-start at boot
```

### Service Management
```bash
voice-mode service livekit status    # Unified service command
voice-mode service frontend start    # Works with all services
```

## Architecture

- **LiveKit Server**: Handles WebRTC communication and room management
- **Frontend**: Next.js application for voice conversations
- **Service Management**: systemd (Linux) or launchd (macOS) integration
- **Configuration**: YAML config with development defaults
- **Bundling**: Frontend assets included in Python wheel distribution

## Files and Locations

```
~/.voicemode/
├── config/
│   └── livekit.yaml              # Server configuration
├── logs/
│   ├── livekit/livekit.log       # Server logs
│   └── frontend/frontend.log     # Frontend logs
└── services/                     # Service data

# Bundled frontend (in Python package)
voice_mode/frontend/              # Next.js application

# Service files (auto-created)
~/.config/systemd/user/voicemode-*.service    # Linux
~/Library/LaunchAgents/com.voicemode.*.plist  # macOS
```

## Integration Features

- **Persistent Services**: Automatically start services at boot/login
- **Health Monitoring**: Real-time status with resource usage
- **Log Management**: Centralized logging with rotation
- **Development Mode**: Easy setup with auto-room creation
- **Web Interface**: Modern React-based voice assistant frontend
- **API Access**: REST and WebSocket APIs for custom integrations

## Requirements

- **Node.js** (for frontend) - automatically detected and used
- **npm/pnpm/yarn** - automatically detected for dependency management
- **systemd** (Linux) or **launchd** (macOS) - for service management

## Documentation

For detailed setup, configuration, and usage instructions, see:
- [Complete Setup Guide](docs/LIVEKIT_SETUP.md)
- [API Documentation](docs/LIVEKIT_API.md) *(coming soon)*

## Example Usage

```bash
# Complete setup
voice-mode livekit install && voice-mode livekit enable
voice-mode frontend enable

# Start everything
voice-mode livekit start
voice-mode frontend start

# Check status
voice-mode livekit status
voice-mode frontend status

# Open web interface
voice-mode frontend open
# Navigate to http://localhost:3000, enter password: voicemode123
```

The LiveKit integration provides a complete real-time voice conversation platform with professional service management and an intuitive web interface.