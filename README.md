# voice-mcp

MCP servers that enable voice interactions between LLMs and users through LiveKit.

## Quick Start with Python Package

The easiest way to use voice-mcp is through our Python package:

```bash
# Install with pip
pip install livekit-voice-mcp

# Or use with uvx (no installation needed)
uvx livekit-voice-mcp
```

### Configure Claude Desktop

Add to your Claude Desktop configuration file:

**macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
**Windows**: `%APPDATA%\Claude\claude_desktop_config.json`

```json
{
  "mcpServers": {
    "livekit-voice": {
      "command": "uvx",
      "args": ["livekit-voice-mcp"],
      "env": {
        "LIVEKIT_URL": "wss://your-app.livekit.cloud",
        "LIVEKIT_API_KEY": "your-api-key",
        "LIVEKIT_API_SECRET": "your-api-secret",
        "OPENAI_API_KEY": "your-openai-key"
      }
    }
  }
}
```

Restart Claude Desktop and you can now use voice commands!

## Overview

voice-mcp provides Model Context Protocol (MCP) servers that allow LLMs to communicate via voice, enabling natural spoken conversations with AI assistants.

### Architecture

```
┌─────────────────────┐     ┌──────────────────┐     ┌─────────────────────┐
│   Claude/LLM        │     │  LiveKit Server  │     │  Voice Frontend     │
│   (MCP Client)      │◄────►│  (Port 7880)     │◄────►│  (Port 3001)        │
└─────────────────────┘     └──────────────────┘     └─────────────────────┘
         │                            │
         │                            │
         ▼                            ▼
┌─────────────────────┐     ┌──────────────────┐
│  Voice MCP Server   │     │   Agent.py       │
│  (ask_voice_question│     │  (Voice Logic)   │
│   check_room_status)│     └──────────────────┘
└─────────────────────┘              │
                                     │
                    ┌────────────────┴────────────────┐
                    │                                 │
                    ▼                                 ▼
         ┌──────────────────┐             ┌──────────────────┐
         │  Whisper.cpp     │             │  Kokoro TTS      │
         │  (Port 2022)     │             │  (Port 8880)     │
         │  Local STT       │             │  Local TTS       │
         └──────────────────┘             └──────────────────┘
```

## Features

- **Voice Input/Output**: Bidirectional voice communication through LiveKit
- **Speech-to-Text**: Local whisper.cpp or OpenAI Whisper API
- **Text-to-Speech**: Multiple TTS providers (OpenAI TTS + local Kokoro-FastAPI)
- **Local STT/TTS**: Cost-free local speech recognition and voice generation
- **Real-time Streaming**: Low-latency voice interactions
- **MCP Integration**: Works seamlessly with Claude and other MCP-compatible clients

## Installation Options

### Option 1: Python Package (Recommended for Users)

```bash
# Install globally
pip install livekit-voice-mcp

# Or use without installation
uvx livekit-voice-mcp

# Or use pipx for isolated installation  
pipx install livekit-voice-mcp
```

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
git clone https://github.com/mbailey/voice-mcp-public.git
cd voice-mcp-public

# Build container image
make build-container

# Or install development environment
make install
```

## Configuration

### Python Package Configuration

Set environment variables before running:
```bash
export LIVEKIT_URL="wss://your-app.livekit.cloud"
export LIVEKIT_API_KEY="your-api-key"
export LIVEKIT_API_SECRET="your-api-secret"
export OPENAI_API_KEY="your-openai-key"  # For STT/TTS
```

### Local Development Configuration

Copy the example configuration and customize:
```bash
cp .env.example .env.local
# Edit .env.local with your settings
```

### Provider Selection
voice-mcp supports multiple STT/TTS providers with smart fallback:

#### TTS Providers
- **`TTS_PROVIDER=auto`** (default): Try Kokoro → OpenAI → LiveKit
- **`TTS_PROVIDER=kokoro`**: Use only local Kokoro TTS  
- **`TTS_PROVIDER=openai`**: Use only OpenAI TTS

#### STT Configuration
- **Local Whisper**: Automatically used when available at `http://localhost:2022`
- **OpenAI Whisper**: Fallback when local whisper is not running

### Key Configuration Options
```bash
# TTS Provider (auto/kokoro/openai)
TTS_PROVIDER=auto

# Kokoro TTS (local)
KOKORO_URL=http://127.0.0.1:8880
KOKORO_ENABLED=true

# Whisper STT (local)
WHISPER_BASE_URL=http://localhost:2022

# OpenAI (fallback for both STT and TTS)
OPENAI_API_KEY=your_key_here

# LiveKit
LIVEKIT_URL=ws://localhost:7880
```

## Usage

### Using the Python Package

Once installed and configured in Claude Desktop, you can use voice commands:

1. Ask Claude: "Can you help me with voice?"
2. Claude will use the voice MCP tools to communicate
3. Speak your questions and hear responses

Available MCP tools:
- `ask_voice_question`: Ask a question via voice and get a text response
- `check_room_status`: Check active voice rooms and participants

### Local Development Usage

1. **Download external repositories:**
   ```bash
   mt sync
   ```

2. **Install and build all dependencies:**
   ```bash
   make install
   ```

3. **Start the development environment:**
   ```bash
   make dev
   ```

This will start:
- LiveKit server (port 7880)
- Kokoro TTS (port 8880) 
- Whisper STT (port 2022)
- Voice assistant frontend (port 3001)

Individual components:
```bash
make livekit-server   # Start LiveKit server
make frontend         # Start voice frontend
make kokoro-start     # Start Kokoro TTS
make whisper-start    # Start Whisper STT
```

## Architecture

- **livekit-voice-mcp**: MCP server for voice interactions
- **livekit-admin-mcp**: Administrative tools for LiveKit management  
- **livekit-agent**: Python agent handling voice processing
- **kokoro-fastapi**: Local TTS server providing OpenAI-compatible API
- **whisper.cpp**: Local STT server providing OpenAI-compatible API

## Kokoro-FastAPI (Local TTS)

voice-mcp includes Kokoro-FastAPI for cost-free local text-to-speech generation:

- **70+ Voice Options**: Multiple languages and voice styles
- **OpenAI Compatible**: Drop-in replacement for OpenAI TTS API
- **Web Interface**: Interactive voice testing at http://127.0.0.1:8880/web/
- **Browser Support**: Chrome/Chromium recommended (Firefox has streaming limitations)

### Kokoro Commands
```bash
make kokoro-start     # Start Kokoro TTS service
make kokoro-stop      # Stop Kokoro TTS service  
make kokoro-build     # Build Kokoro container
make test-kokoro      # Test Kokoro functionality
```

### Quick Test
```bash
# Generate speech using Kokoro API
curl -X POST http://127.0.0.1:8880/v1/audio/speech \
  -H "Content-Type: application/json" \
  -d '{"input": "Hello from Kokoro!", "voice": "nova"}' \
  --output test.mp3
```

## Whisper.cpp (Local STT)

voice-mcp includes whisper.cpp for cost-free local speech-to-text:

- **Hardware Optimization**: Automatically selects best model for your hardware
- **OpenAI Compatible**: Drop-in replacement for OpenAI Whisper API
- **Multiple Models**: From tiny to large-v3-turbo
- **GPU Support**: CUDA, Metal, and Vulkan acceleration

### Whisper Commands
```bash
make whisper-build    # Build Whisper container
make whisper-start    # Start Whisper STT service
make whisper-stop     # Stop Whisper STT service
```

### Quick Test
```bash
# Test whisper API (OpenAI-compatible)
curl -X POST http://localhost:2022/v1/audio/transcriptions \
  -H "Content-Type: multipart/form-data" \
  -F "file=@audio.wav"
```

## Requirements

- Python 3.8+
- LiveKit server  
- Podman or Docker (for Kokoro TTS only)
- Build tools (cmake, make, gcc/g++) for Whisper.cpp
- OpenAI API key (optional, for cloud fallback)
- `mt` command for managing external repos

## Development

See [TASKS.md](TASKS.md) for development roadmap and technical tasks.

## License

MIT
