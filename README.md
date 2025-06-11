# voice-mcp - Voice Mode for Claude Code

A Model Context Protocol (MCP) server that enables voice interactions with Claude and other LLMs. Requires only an OpenAI API key and microphone/speakers.

[![Build and Publish Voice MCP Container](https://github.com/mbailey/voice-mcp/actions/workflows/build-container.yml/badge.svg)](https://github.com/mbailey/voice-mcp/actions/workflows/build-container.yml)

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

Setup for Claude Code:

```bash
export OPENAI_API_KEY=your-openai-key
claude mcp add voice-mcp uvx voice-mcp
# Alternatively, run a container image
# docker pull ghcr.io/mbailey/voice-mcp:latest
# claude mcp add voice-mcp podman run -e OPENAI_API_KEY ghcr.io/mbailey/voice-mcp:latest
claude
```

Try: *"Let's have a voice conversation"*

## Example Usage

Once configured, try these prompts with Claude:

- `"Let's have a voice conversation"`
- `"Ask me about my day using voice"`
- `"Tell me a joke"` (Claude will speak and wait for your response)
- `"Say goodbye"` (Claude will speak without waiting)

The new `converse` function makes voice interactions more natural - it automatically waits for your response by default.

## Claude Desktop Setup

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

## Tools

| Tool | Description | Key Parameters |
|------|-------------|----------------|
| `converse` | Speak and optionally listen for response | `wait_for_response` (default: true), `listen_duration` (default: 10s) |
| `listen_for_speech` | Just listen and transcribe speech | `duration` (default: 5s) |
| `check_room_status` | Show LiveKit room status | N/A |
| `check_audio_devices` | List audio devices | N/A |

## Configuration

### Required
```bash
export OPENAI_API_KEY="your-key"
```

### Optional
```bash
# Custom services (OpenAI-compatible)
export STT_BASE_URL="http://localhost:2022/v1"  # Local Whisper
export TTS_BASE_URL="http://localhost:8880/v1"  # Local TTS
export TTS_VOICE="af_sky"                       # Sky Voice (Kokoro)
export TTS_MODEL="tts-1"
export STT_MODEL="whisper-1"

# LiveKit (for room-based communication)
export LIVEKIT_URL="wss://your-app.livekit.cloud"
export LIVEKIT_API_KEY="your-api-key"
export LIVEKIT_API_SECRET="your-api-secret"

# Debug
export VOICE_MCP_DEBUG="true"
```

## Troubleshooting

- **No microphone**: Check system permissions
- **UV not found**: `curl -LsSf https://astral.sh/uv/install.sh | sh`
- **API errors**: Verify `OPENAI_API_KEY`
- **Debug mode**: Set `VOICE_MCP_DEBUG=true` (saves audio to `~/voice-mcp_recordings/`)

## License

MIT
