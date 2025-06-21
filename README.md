# Voice Mode

> **Install via:** `uvx voice-mode` | `pip install voice-mode` | [getvoicemode.com](https://getvoicemode.com)

Natural voice conversations for AI assistants. Voice Mode brings human-like voice interactions to Claude, ChatGPT, and other LLMs through the Model Context Protocol (MCP).

## 🖥️ Compatibility

**Runs on:** Linux • macOS • Windows (WSL) | **Python:** 3.10+ | **Tested:** Ubuntu 24.04 LTS, Fedora 42

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

## Quick Start

```bash
claude mcp add --scope user voice-mode uvx voice-mode
export OPENAI_API_KEY=your-openai-key
claude
> /converse
```

## 🎬 Demo

Watch Voice Mode in action:

[![Voice Mode Demo](https://img.youtube.com/vi/aXRNWvpnwVs/maxresdefault.jpg)](https://www.youtube.com/watch?v=aXRNWvpnwVs)

## Example Usage

Once configured, try these prompts with Claude:

- `"Let's have a voice conversation"`
- `"Ask me about my day using voice"`
- `"Tell me a joke"` (Claude will speak and wait for your response)
- `"Say goodbye"` (Claude will speak without waiting)

The new `converse` function makes voice interactions more natural - it automatically waits for your response by default.

## Installation

### Prerequisites
- Python >= 3.10
- OpenAI API Key (or compatible service)

### Quick Install

```bash
# Using Claude Code (recommended)
claude mcp add --scope user voice-mode uvx voice-mode

# Using UV
uvx voice-mode

# Using pip
pip install voice-mode
```

### Manual Configuration for Different Clients

<details>
<summary><strong>Claude Code (CLI)</strong></summary>

```bash
claude mcp add voice-mode -- uvx voice-mode
```

Or with environment variables:
```bash
claude mcp add voice-mode --env OPENAI_API_KEY=your-openai-key -- uvx voice-mode
```
</details>

<details>
<summary><strong>Claude Desktop</strong></summary>

**macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`  
**Windows**: `%APPDATA%\Claude\claude_desktop_config.json`

```json
{
  "mcpServers": {
    "voice-mode": {
      "command": "uvx",
      "args": ["voice-mode"],
      "env": {
        "OPENAI_API_KEY": "your-openai-key"
      }
    }
  }
}
```
</details>

<details>
<summary><strong>Cline</strong></summary>

Add to your Cline MCP settings:

**Windows**:
```json
{
  "mcpServers": {
    "voice-mode": {
      "command": "cmd",
      "args": ["/c", "uvx", "voice-mode"],
      "env": {
        "OPENAI_API_KEY": "your-openai-key"
      }
    }
  }
}
```

**macOS/Linux**:
```json
{
  "mcpServers": {
    "voice-mode": {
      "command": "uvx",
      "args": ["voice-mode"],
      "env": {
        "OPENAI_API_KEY": "your-openai-key"
      }
    }
  }
}
```
</details>

<details>
<summary><strong>Continue</strong></summary>

Add to your `.continue/config.json`:
```json
{
  "experimental": {
    "modelContextProtocolServers": [
      {
        "transport": {
          "type": "stdio",
          "command": "uvx",
          "args": ["voice-mode"],
          "env": {
            "OPENAI_API_KEY": "your-openai-key"
          }
        }
      }
    ]
  }
}
```
</details>

<details>
<summary><strong>Cursor</strong></summary>

Add to `~/.cursor/mcp.json`:
```json
{
  "mcpServers": {
    "voice-mode": {
      "command": "uvx",
      "args": ["voice-mode"],
      "env": {
        "OPENAI_API_KEY": "your-openai-key"
      }
    }
  }
}
```
</details>

<details>
<summary><strong>VS Code</strong></summary>

Add to your VS Code MCP config:
```json
{
  "mcpServers": {
    "voice-mode": {
      "command": "uvx",
      "args": ["voice-mode"],
      "env": {
        "OPENAI_API_KEY": "your-openai-key"
      }
    }
  }
}
```
</details>

<details>
<summary><strong>Windsurf</strong></summary>

```json
{
  "mcpServers": {
    "voice-mode": {
      "command": "uvx",
      "args": ["voice-mode"],
      "env": {
        "OPENAI_API_KEY": "your-openai-key"
      }
    }
  }
}
```
</details>

<details>
<summary><strong>Zed</strong></summary>

Add to your Zed settings.json:
```json
{
  "context_servers": {
    "voice-mode": {
      "command": {
        "path": "uvx",
        "args": ["voice-mode"],
        "env": {
          "OPENAI_API_KEY": "your-openai-key"
        }
      }
    }
  }
}
```
</details>

<details>
<summary><strong>Roo Code</strong></summary>

Add to your Roo Code MCP configuration:
```json
{
  "mcpServers": {
    "voice-mode": {
      "command": "uvx",
      "args": ["voice-mode"],
      "env": {
        "OPENAI_API_KEY": "your-openai-key"
      }
    }
  }
}
```
</details>

### Alternative Installation Options

<details>
<summary><strong>Using Docker</strong></summary>

```bash
docker run -it --rm \
  -e OPENAI_API_KEY=your-openai-key \
  --device /dev/snd \
  -v /tmp/.X11-unix:/tmp/.X11-unix \
  -e DISPLAY=$DISPLAY \
  ghcr.io/mbailey/voicemode:latest
```
</details>

<details>
<summary><strong>Using pipx</strong></summary>

```bash
pipx install voice-mode
```
</details>

<details>
<summary><strong>From source</strong></summary>

```bash
git clone https://github.com/mbailey/voicemode.git
cd voicemode
pip install -e .
```
</details>

## Tools

| Tool | Description | Key Parameters |
|------|-------------|----------------|
| `converse` | Have a voice conversation - speak and optionally listen | `message`, `wait_for_response` (default: true), `listen_duration` (default: 10s), `transport` (auto/local/livekit) |
| `listen_for_speech` | Listen for speech and convert to text | `duration` (default: 5s) |
| `check_room_status` | Check LiveKit room status and participants | None |
| `check_audio_devices` | List available audio input/output devices | None |
| `start_kokoro` | Start the Kokoro TTS service | `models_dir` (optional, defaults to ~/Models/kokoro) |
| `stop_kokoro` | Stop the Kokoro TTS service | None |
| `kokoro_status` | Check the status of Kokoro TTS service | None |

**Note:** The `converse` tool is the primary interface for voice interactions, combining speaking and listening in a natural flow.

## Configuration

**📖 See [docs/configuration.md](docs/configuration.md) for complete setup instructions for all MCP hosts**

**📁 Ready-to-use config files in [config-examples/](config-examples/)**

### Quick Setup

The only required configuration is your OpenAI API key:

```bash
export OPENAI_API_KEY="your-key"
```

### Optional Settings

```bash
# Custom STT/TTS services (OpenAI-compatible)
export STT_BASE_URL="http://localhost:2022/v1"  # Local Whisper
export TTS_BASE_URL="http://localhost:8880/v1"  # Local TTS
export TTS_VOICE="alloy"                        # Voice selection

# LiveKit (for room-based communication)
# See docs/livekit/ for setup guide
export LIVEKIT_URL="wss://your-app.livekit.cloud"
export LIVEKIT_API_KEY="your-api-key"
export LIVEKIT_API_SECRET="your-api-secret"

# Debug mode
export VOICEMODE_DEBUG="true"

# Save all audio (TTS output and STT input)
export VOICEMODE_SAVE_AUDIO="true"

# Audio format configuration (default: opus)
export VOICEMODE_AUDIO_FORMAT="opus"        # Options: opus, mp3, wav, flac, aac
export VOICEMODE_TTS_AUDIO_FORMAT="opus"    # Override for TTS only
export VOICEMODE_STT_AUDIO_FORMAT="mp3"     # Override for STT upload

# Format-specific quality settings
export VOICEMODE_OPUS_BITRATE="32000"       # Opus bitrate (default: 32kbps)
export VOICEMODE_MP3_BITRATE="64k"          # MP3 bitrate (default: 64k)
```

### Audio Format Configuration

Voice Mode uses **Opus** audio format by default for optimal performance:

- **Opus** (default): Best for voice, 50-80% smaller files than MP3, low latency
- **MP3**: Wide compatibility, use if Opus causes issues  
- **WAV**: Highest quality, largest files
- **FLAC**: Lossless compression, good for archival
- **AAC**: Good compression, Apple ecosystem

The audio format is automatically validated against provider capabilities and will fallback to a supported format if needed.

## Local STT/TTS Services

For privacy-focused or offline usage, Voice Mode supports local speech services:

- **[Whisper.cpp](docs/whisper.cpp.md)** - Local speech-to-text with OpenAI-compatible API
- **[Kokoro](docs/kokoro.md)** - Local text-to-speech with multiple voice options

These services provide the same API interface as OpenAI, allowing seamless switching between cloud and local processing.

### OpenAI API Compatibility Benefits

By strictly adhering to OpenAI's API standard, Voice Mode enables powerful deployment flexibility:

- **🔀 Transparent Routing**: Users can implement their own API proxies or gateways outside of Voice Mode to route requests to different providers based on custom logic (cost, latency, availability, etc.)
- **🎯 Model Selection**: Deploy routing layers that select optimal models per request without modifying Voice Mode configuration
- **💰 Cost Optimization**: Build intelligent routers that balance between expensive cloud APIs and free local models
- **🔧 No Lock-in**: Switch providers by simply changing the `BASE_URL` - no code changes required

Example: Simply set `OPENAI_BASE_URL` to point to your custom router:
```bash
export OPENAI_BASE_URL="https://router.example.com/v1"
export OPENAI_API_KEY="your-key"
# Voice Mode now uses your router for all OpenAI API calls
```

The OpenAI SDK handles this automatically - no Voice Mode configuration needed!

## Architecture

```
┌─────────────────────┐     ┌──────────────────┐     ┌─────────────────────┐
│   Claude/LLM        │     │  LiveKit Server  │     │  Voice Frontend     │
│   (MCP Client)      │◄────►│  (Optional)     │◄───►│  (Optional)         │
└─────────────────────┘     └──────────────────┘     └─────────────────────┘
         │                            │
         │                            │
         ▼                            ▼
┌─────────────────────┐     ┌──────────────────┐
│  Voice MCP Server   │     │   Audio Services │
│  • converse         │     │  • OpenAI APIs   │
│  • listen_for_speech│◄───►│  • Local Whisper │
│  • check_room_status│     │  • Local TTS     │
│  • check_audio_devices    └──────────────────┘
└─────────────────────┘
```

## Troubleshooting

### Common Issues

- **No microphone access**: Check system permissions for terminal/application
- **UV not found**: Install with `curl -LsSf https://astral.sh/uv/install.sh | sh`
- **OpenAI API error**: Verify your `OPENAI_API_KEY` is set correctly
- **No audio output**: Check system audio settings and available devices

### Debug Mode

Enable detailed logging and audio file saving:

```bash
export VOICEMODE_DEBUG=true
```

Debug audio files are saved to: `~/voicemode_recordings/`

### Audio Saving

To save all audio files (both TTS output and STT input):

```bash
export VOICEMODE_SAVE_AUDIO=true
```

Audio files are saved to: `~/voicemode_audio/` with timestamps in the filename.

## Links

- **Website**: [getvoicemode.com](https://getvoicemode.com)
- **GitHub**: [github.com/mbailey/voicemode](https://github.com/mbailey/voicemode)
- **PyPI**: [pypi.org/project/voice-mcp](https://pypi.org/project/voice-mcp/)
- **npm**: [npmjs.com/package/voicemode](https://www.npmjs.com/package/voicemode)

### Community

- **Discord**: [Join our community](https://discord.gg/gVHPPK5U)
- **Twitter/X**: [@getvoicemode](https://twitter.com/getvoicemode)
- **YouTube**: [@getvoicemode](https://youtube.com/@getvoicemode)

## License

MIT - A [Failmode](https://failmode.com) Project
