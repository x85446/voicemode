# voice-mcp - Converse with Claude Code

A Model Context Protocol (MCP) server that enables voice interactions with Claude and other LLMs. Requires only an OpenAI API key and microphone/speakers.

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
