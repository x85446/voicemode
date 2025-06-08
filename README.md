# voice-mcp - Converse with Claude Code

A Model Context Protocol (MCP) server that enables voice interactions with Claude and other LLMs. Requires only an OpenAI API key and microphone/speakers.

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
claude mcp add --scope user voice-mcp uvx voice-mcp
export OPENAI_API_KEY=your-openai-key
claude
```

Try: *"Can you ask me a question using voice?"*

## Example Usage

Once configured, try these prompts with Claude:

- `"Can you ask me a question using voice and let me respond by speaking?"`
- `"Please read this text aloud to me: [your text here]"`
- `"Listen to what I'm saying for the next 10 seconds"`
- `"Have a voice conversation with me - ask me about my day"`

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

| Tool | Description |
|------|-------------|
| `ask_voice_question` | Ask a question via voice, get spoken response |
| `speak_text` | Convert text to speech |
| `listen_for_speech` | Record and transcribe speech |
| `check_room_status` | Show LiveKit room status |
| `check_audio_devices` | List audio devices |

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
