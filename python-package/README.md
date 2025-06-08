# voice-mcp - Converse with Claude Code

A Model Context Protocol (MCP) server that enables voice interactions between LLMs and users through multiple transport methods.

## ✨ Features

- **🎙️ Voice conversations** with Claude - ask questions and hear responses
- **🔄 Multiple transports** - local microphone or LiveKit room-based communication  
- **🗣️ OpenAI-compatible** - works with any STT/TTS service (local or cloud)
- **⚡ Real-time** - low-latency voice interactions with automatic transport selection
- **🔧 MCP Integration** - seamless with Claude Desktop and other MCP clients

## 🎯 Simple Requirements

**All you need to get started:**

1. **🔑 OpenAI API Key** (or compatible service) - for speech-to-text and text-to-speech
2. **🎤 Computer with microphone and speakers** OR **☁️ LiveKit server** ([LiveKit Cloud](https://docs.livekit.io/home/cloud/) or [self-hosted](https://github.com/livekit/livekit))

That's it! No complex setup, no local services to install.

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

<details>
<summary>Using uvx (recommended)</summary>

```json
{
  "mcpServers": {
    "voice-mcp": {
      "command": "uvx",
      "args": ["voice-mcp"],
      "env": {
        "OPENAI_API_KEY": "your-openai-key"
      }
    }
  }
}
```

</details>

<details>
<summary>Using Docker/Podman</summary>

```json
{
  "mcpServers": {
    "voice-mcp": {
      "command": "docker",
      "args": [
        "run", "--rm", "-i",
        "--device", "/dev/snd",
        "-e", "PULSE_RUNTIME_PATH=/run/user/1000/pulse",
        "-v", "/run/user/1000/pulse:/run/user/1000/pulse",
        "ghcr.io/mbailey/voice-mcp:latest"
      ],
      "env": {
        "OPENAI_API_KEY": "your-openai-key"
      }
    }
  }
}
```

</details>

<details>
<summary>Using pip install</summary>

```json
{
  "mcpServers": {
    "voice-mcp": {
      "command": "voice-mcp",
      "env": {
        "OPENAI_API_KEY": "your-openai-key"
      }
    }
  }
}
```

</details>

<details>
<summary>Using python -m (if installed via pip)</summary>

```json
{
  "mcpServers": {
    "voice-mcp": {
      "command": "python",
      "args": ["-m", "voice_mcp"],
      "env": {
        "OPENAI_API_KEY": "your-openai-key"
      }
    }
  }
}
```

</details>

<details>
<summary>With LiveKit Configuration</summary>

If you want to use LiveKit instead of local microphone, add these environment variables to any of the above configurations:

```json
{
  "mcpServers": {
    "voice-mcp": {
      "command": "uvx",
      "args": ["voice-mcp"],
      "env": {
        "OPENAI_API_KEY": "your-openai-key",
        "LIVEKIT_URL": "wss://your-app.livekit.cloud",
        "LIVEKIT_API_KEY": "your-api-key",
        "LIVEKIT_API_SECRET": "your-api-secret"
      }
    }
  }
}
```

</details>

Restart Claude Desktop and you can now use voice commands!

## Overview

voice-mcp provides a Model Context Protocol server that allows LLMs to communicate via voice, enabling natural spoken conversations with AI assistants. 

**🎯 Simple & Flexible:**
- **Works immediately** with just an OpenAI API key + microphone/speakers
- **Local microphone**: Direct recording and playback on your machine  
- **LiveKit rooms**: Real-time voice communication through [LiveKit Cloud](https://docs.livekit.io/home/cloud/) or [self-hosted](https://github.com/livekit/livekit)
- **OpenAI-compatible**: Use any compatible STT/TTS service (local or cloud)
- **Automatic transport selection**: Seamlessly switches between available methods

## Features

- **🎙️ Voice Input/Output**: Bidirectional voice communication
- **🗣️ Text-to-Speech**: OpenAI TTS API support with configurable voices
- **👂 Speech-to-Text**: OpenAI Whisper API with local fallback support
- **🔄 Multiple Transports**: Local microphone or LiveKit room-based communication
- **⚡ Real-time**: Low-latency voice interactions
- **🔧 MCP Integration**: Works seamlessly with Claude and other MCP-compatible clients
- **🛡️ Privacy-conscious**: Clear user consent requirements for microphone access

## Available MCP Tools

| **Category** | **Tool** | **Description** |
|-------------|----------|-----------------|
| **Voice Interaction** | `ask_voice_question` | Ask a question via voice and get a text response. Supports auto-transport selection (local/LiveKit) |
| **Speech Output** | `speak_text` | Convert text to speech and play it through speakers |
| **Speech Input** | `listen_for_speech` | Listen for speech input and convert to text using configured STT service |
| **Room Management** | `check_room_status` | Check active LiveKit rooms and participants |
| **Device Management** | `check_audio_devices` | List available audio input and output devices on the system |

## Example Usage Prompts

Try these prompts with Claude to test voice functionality:

- `"Can you ask me a question using voice and let me respond by speaking?"`
- `"Please read this text aloud to me: [your text here]"`
- `"Listen to what I'm saying for the next 10 seconds"`
- `"What audio devices are available on my system?"`
- `"Check if there are any active LiveKit rooms"`
- `"Have a voice conversation with me - ask me about my day"`
- `"Read me the latest commit message from this repository"`

## Available Resources  

Currently, voice-mcp does not provide static resources. All functionality is delivered through real-time tools.

## Tool Reference

### ask_voice_question
**Purpose**: Interactive voice Q&A with automatic transport selection  
**Parameters**:
- `question` (required): The question to ask via voice
- `transport` (optional): "auto", "local", or "livekit" (default: "auto")
- `room_name` (optional): LiveKit room name for livekit transport
- `duration` (optional): Recording duration in seconds for local transport (default: 5.0)
- `timeout` (optional): Maximum wait time for response (default: 60.0)

### speak_text  
**Purpose**: Convert text to speech and play through speakers  
**Parameters**:
- `text` (required): Text to convert to speech

### listen_for_speech
**Purpose**: Record audio from microphone and convert to text  
**Parameters**:
- `duration` (optional): How long to listen in seconds (default: 5.0)

### check_room_status
**Purpose**: Get information about active LiveKit rooms  
**Parameters**: None

### check_audio_devices
**Purpose**: List available audio input/output devices  
**Parameters**: None

## Installation

### Using uvx (recommended)

You can run voice-mcp directly without installation using `uvx`:

```bash
uvx voice-mcp
```

### Using pip

Alternatively, you can install voice-mcp as a Python package:

```bash
# Install globally
pip install voice-mcp

# Or use pipx for isolated installation  
pipx install voice-mcp
```

**Requirements**: Python 3.8+, UV package manager (automatically installed)

### Alternative: Container Image

```bash
# Pull and run the container
docker pull ghcr.io/mbailey/voice-mcp:latest

# Run with environment variables
docker run -e OPENAI_API_KEY=your_key_here \
  -e VOICE_MCP_DEBUG=true \
  ghcr.io/mbailey/voice-mcp:latest
```

See [CONTAINER.md](CONTAINER.md) for detailed container usage instructions.

### Alternative: Local Development Setup

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

### 🔑 Required: OpenAI API Key

The only required configuration is your OpenAI API key (or compatible service):

```bash
export OPENAI_API_KEY="your-openai-key"
```

**That's it!** voice-mcp works out of the box with:
- **Local microphone and speakers** (automatic detection)
- **OpenAI Whisper API** (speech-to-text) 
- **OpenAI TTS API** (text-to-speech)

### 🔧 Optional: Custom Service Endpoints

Use alternative OpenAI-compatible services by setting base URLs:

```bash
# For local Whisper STT (if running)
export STT_BASE_URL="http://localhost:2022/v1"

# For local TTS services (if running)  
export TTS_BASE_URL="http://localhost:8880/v1"

# Customize voice and models
export TTS_VOICE="nova"        # Voice for text-to-speech
export TTS_MODEL="tts-1"       # TTS model
export STT_MODEL="whisper-1"   # STT model
```

### ☁️ Optional: LiveKit Server

For LiveKit room-based communication instead of local microphone:

```bash
# LiveKit Cloud (https://docs.livekit.io/home/cloud/)
export LIVEKIT_URL="wss://your-app.livekit.cloud"
export LIVEKIT_API_KEY="your-api-key" 
export LIVEKIT_API_SECRET="your-api-secret"

# OR self-hosted LiveKit (https://github.com/livekit/livekit)
export LIVEKIT_URL="ws://localhost:7880"
export LIVEKIT_API_KEY="devkey"
export LIVEKIT_API_SECRET="secret"
```

### 🐛 Optional: Debug Mode

```bash
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

## 📋 Requirements Summary

### ✅ Minimal Requirements (Get Started Immediately)

1. **🔑 OpenAI API key** - Or any OpenAI-compatible service (local Whisper, local TTS, etc.)
2. **🎤 Computer with microphone and speakers** - OR LiveKit server ([cloud](https://docs.livekit.io/home/cloud/)/[self-hosted](https://github.com/livekit/livekit))

### 🔧 Technical Requirements

- **Python 3.8+** (for the package)
- **UV package manager** (automatically installed with the package)

### 🚀 Optional Enhancements

- **[LiveKit Cloud](https://docs.livekit.io/home/cloud/) or [self-hosted server](https://github.com/livekit/livekit)** - For room-based voice communication
- **Local STT/TTS services** - For cost-free speech processing
- **Development tools** - For building the full local stack (Docker, cmake, etc.)

## Development

See [TASKS.md](TASKS.md) for development roadmap and technical tasks.

## License

MIT
