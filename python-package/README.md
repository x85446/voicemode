# voice-mcp

A Model Context Protocol (MCP) server that enables voice interactions between LLMs and users through multiple transport methods.

## Quick Start with Python Package

The easiest way to use voice-mcp is through our Python package:

```bash
# Install with pip
pip install voice-mcp

# Or use with uvx (no installation needed)
uvx voice-mcp

# Or use pipx for isolated installation  
pipx install voice-mcp
```

### Configure Claude Desktop

Add to your Claude Desktop configuration file:

**macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
**Windows**: `%APPDATA%\Claude\claude_desktop_config.json`

```json
{
  "mcpServers": {
    "voice-mcp": {
      "command": "voice-mcp",
      "env": {
        "OPENAI_API_KEY": "your-openai-key",
        "LIVEKIT_URL": "ws://localhost:7880",
        "LIVEKIT_API_KEY": "devkey",
        "LIVEKIT_API_SECRET": "secret"
      }
    }
  }
}
```

Restart Claude Desktop and you can now use voice commands!

## Overview

voice-mcp provides a Model Context Protocol server that allows LLMs to communicate via voice, enabling natural spoken conversations with AI assistants through multiple transport methods:

- **Local microphone**: Direct recording and playback on your machine
- **LiveKit rooms**: Real-time voice communication through LiveKit infrastructure
- **Automatic fallback**: Seamlessly switches between transport methods

## Features

- **🎙️ Voice Input/Output**: Bidirectional voice communication
- **🗣️ Text-to-Speech**: OpenAI TTS API support with configurable voices
- **👂 Speech-to-Text**: OpenAI Whisper API with local fallback support
- **🔄 Multiple Transports**: Local microphone or LiveKit room-based communication
- **⚡ Real-time**: Low-latency voice interactions
- **🔧 MCP Integration**: Works seamlessly with Claude and other MCP-compatible clients
- **🛡️ Privacy-conscious**: Clear user consent requirements for microphone access

## Available MCP Tools

Once configured, Claude can use these voice interaction tools:

- **`ask_voice_question`**: Ask a question via voice and get a text response
- **`speak_text`**: Convert text to speech and play it through speakers
- **`listen_for_speech`**: Listen for speech input and convert to text
- **`check_room_status`**: Check active LiveKit rooms and participants
- **`check_audio_devices`**: List available audio input and output devices

## Installation Options

### Option 1: Python Package (Recommended)

```bash
# Install globally
pip install voice-mcp

# Or use without installation
uvx voice-mcp

# Or use pipx for isolated installation  
pipx install voice-mcp
```

**Requirements**: Python 3.8+, UV package manager

### Option 2: Container Image

```bash
# Pull and run the container
docker pull ghcr.io/mbailey/voice-mcp:latest

# Run with environment variables
docker run -e OPENAI_API_KEY=your_key_here \
  -e VOICE_MCP_DEBUG=true \
  ghcr.io/mbailey/voice-mcp:latest
```

See [CONTAINER.md](CONTAINER.md) for detailed container usage instructions.

### Option 3: Local Development Setup

```bash
# Clone the repository
git clone https://github.com/mbailey/voice-mcp.git
cd voice-mcp

# Build container image
make build-container

# Or install development environment
make install
```

## Configuration

### Environment Variables

Set these environment variables before running:

```bash
# Required
export OPENAI_API_KEY="your-openai-key"  # For STT/TTS

# Optional - LiveKit configuration
export LIVEKIT_URL="ws://localhost:7880"
export LIVEKIT_API_KEY="devkey"
export LIVEKIT_API_SECRET="secret"

# Optional - Service customization
export STT_BASE_URL="https://api.openai.com/v1"  # Speech-to-text service
export TTS_BASE_URL="https://api.openai.com/v1"  # Text-to-speech service
export TTS_VOICE="nova"                           # Voice for TTS
export TTS_MODEL="tts-1"                          # TTS model
export STT_MODEL="whisper-1"                      # STT model

# Optional - Debug mode
export VOICE_MCP_DEBUG="true"  # Saves audio files and enables verbose logging
```

### Local Development Configuration

For local development with the full stack (including Kokoro TTS and Whisper STT):

```bash
cp .env.example .env.local
# Edit .env.local with your settings
```

## Usage

### Using with Claude Desktop

1. Install and configure voice-mcp in Claude Desktop (see Quick Start above)
2. Ask Claude: "Can you help me with voice?"
3. Claude will use voice MCP tools to enable voice communication
4. Speak your questions and hear responses

### Example Voice Interactions

```
You: "Claude, can you ask me a question via voice?"
Claude: [Uses ask_voice_question tool]
You: [Speaks response]
Claude: [Processes voice input and responds]

You: "Claude, please read this text aloud"
Claude: [Uses speak_text tool to convert text to speech]

You: "What audio devices do I have available?"
Claude: [Uses check_audio_devices tool to list devices]
```

## Local Development Stack

For advanced users who want the full local voice processing stack:

```bash
# Download external repositories
mt sync

# Install and build all dependencies
make install

# Start the complete development environment
make dev
```

This starts:
- LiveKit server (port 7880)
- Kokoro TTS (port 8880) - Local text-to-speech
- Whisper STT (port 2022) - Local speech-to-text
- Voice assistant frontend (port 3001)

Individual components:
```bash
make livekit-server   # Start LiveKit server
make frontend         # Start voice frontend
make kokoro-start     # Start Kokoro TTS
make whisper-start    # Start Whisper STT
```

## Architecture

```
┌─────────────────────┐     ┌──────────────────┐     ┌─────────────────────┐
│   Claude/LLM        │     │  LiveKit Server  │     │  Voice Frontend     │
│   (MCP Client)      │◄────►│  (Port 7880)     │◄────►│  (Port 3001)        │
└─────────────────────┘     └──────────────────┘     └─────────────────────┘
         │                            │
         │                            │
         ▼                            ▼
┌─────────────────────┐     ┌──────────────────┐
│  Voice MCP Server   │     │   Local Services │
│  • ask_voice_question     │  • Whisper STT   │
│  • speak_text       │     │  • Kokoro TTS    │
│  • listen_for_speech│     │  • OpenAI APIs   │
│  • check_room_status│     └──────────────────┘
│  • check_audio_devices
└─────────────────────┘
```

## Troubleshooting

### Common Issues

1. **"No microphone access"**: Ensure your system allows microphone access for the terminal/application
2. **"UV not found"**: Install UV package manager: `curl -LsSf https://astral.sh/uv/install.sh | sh`
3. **"OpenAI API error"**: Verify your `OPENAI_API_KEY` is set correctly
4. **"No audio output"**: Check your system's audio settings and available devices

### Debug Mode

Enable debug mode for detailed logging and audio file saving:

```bash
export VOICE_MCP_DEBUG=true
voice-mcp
```

Debug files are saved to `~/voice-mcp_recordings/`

## Requirements

- **Python 3.8+**
- **UV package manager** (automatically installed with the package)
- **OpenAI API key** (for STT/TTS)
- **Audio devices** (microphone and speakers)

Optional for local development:
- LiveKit server
- Podman or Docker (for local TTS/STT services)
- Build tools (cmake, make, gcc/g++) for Whisper.cpp
- `mt` command for managing external repositories

## Development

See [TASKS.md](TASKS.md) for development roadmap and technical tasks.

## License

MIT