# Voice-MCP Configuration

> For integration-specific setup instructions, see the [setup guide](setup/).

This document provides a comprehensive reference for all environment variables used by voice-mcp.

## MCP Environment Variable Precedence

When using voice-mcp with MCP hosts (Claude Desktop, VS Code, etc.), it's important to understand how environment variables are handled:

### Key Points

1. **Explicit Declaration Required**: If you include an `env` section in your MCP configuration, ONLY those variables are passed to the server
2. **No Variable Substitution**: MCP does not support `${VARIABLE}` syntax - only literal values work
3. **Inheritance Behavior**: If you omit the `env` section entirely, the server inherits the parent process environment

### Configuration Precedence

- Variables in MCP config `env` section override shell environment variables
- To use shell environment variables, either:
  - Omit the `env` section completely (inherits all)
  - Hardcode values in the `env` section (not recommended for secrets)

### Example Scenarios

```json
// ❌ This does NOT work - no variable substitution
{
  "mcpServers": {
    "voice-mode": {
      "env": {
        "OPENAI_API_KEY": "${OPENAI_API_KEY}"  // Won't expand
      }
    }
  }
}

// ✅ Option 1: Omit env to inherit from shell
{
  "mcpServers": {
    "voice-mode": {
      "command": "uvx",
      "args": ["voice-mode"]
      // No env section - inherits OPENAI_API_KEY from shell
    }
  }
}

// ✅ Option 2: Explicit values (avoid for secrets)
{
  "mcpServers": {
    "voice-mode": {
      "env": {
        "VOICEMODE_DEBUG": "true",
        "VOICEMODE_TTS_VOICE": "af_sky"
      }
    }
  }
}
```

### References

- [MCP Configuration Documentation](mcp-config-json.md) - Detailed MCP configuration behavior
- [Model Context Protocol Specification](https://modelcontextprotocol.io/docs/specification) - Official MCP specification
- [Known Limitations](https://github.com/microsoft/vscode/issues/245237) - Feature request for variable substitution

## Required Configuration

| Variable | Description |
|----------|-------------|
| `OPENAI_API_KEY` | Your OpenAI API key (required for cloud STT/TTS services) |

## TTS (Text-to-Speech) Configuration

| Variable | Default | Description |
|----------|---------|-------------|
| `VOICEMODE_TTS_BASE_URL` | `https://api.openai.com/v1` | Base URL for TTS service |
| `VOICEMODE_TTS_VOICE` | `alloy` | Default voice to use |
| `VOICEMODE_TTS_MODEL` | `tts-1` | TTS model (`tts-1`, `tts-1-hd`, `gpt-4o-mini-tts`) |
| `VOICEMODE_VOICES` | `af_sky,nova` | Comma-separated list of preferred voices in order |
| `VOICEMODE_OPENAI_TTS_BASE_URL` | `https://api.openai.com/v1` | OpenAI-specific TTS endpoint |
| `VOICEMODE_KOKORO_TTS_BASE_URL` | `http://localhost:8880/v1` | Kokoro-specific TTS endpoint |

### Available Voices

- **OpenAI**: `alloy`, `nova`, `echo`, `fable`, `onyx`, `shimmer`
- **Kokoro**: `af_sky`, `af_sarah`, `am_adam`, `af_nicole`, `am_michael`

## STT (Speech-to-Text) Configuration

| Variable | Default | Description |
|----------|---------|-------------|
| `VOICEMODE_STT_BASE_URL` | `https://api.openai.com/v1` | Base URL for STT service |
| `VOICEMODE_STT_MODEL` | `whisper-1` | STT model to use |

## Audio Format Configuration

| Variable | Default | Description |
|----------|---------|-------------|
| `VOICEMODE_AUDIO_FORMAT` | `pcm` | Primary audio format (`pcm`, `opus`, `mp3`, `wav`, `flac`, `aac`) |
| `VOICEMODE_TTS_AUDIO_FORMAT` | `pcm` | Override format for TTS (defaults to primary) |
| `VOICEMODE_STT_AUDIO_FORMAT` | `mp3`* | Override format for STT (*auto-selects `mp3` if primary is `pcm`) |
| `VOICEMODE_OPUS_BITRATE` | `32000` | Opus bitrate in bps |
| `VOICEMODE_MP3_BITRATE` | `64k` | MP3 bitrate |
| `VOICEMODE_AAC_BITRATE` | `64k` | AAC bitrate |

## Provider Selection

| Variable | Default | Description |
|----------|---------|-------------|
| `VOICEMODE_PREFER_LOCAL` | `true` | Prefer local providers (Kokoro/Whisper) when available |
| `VOICEMODE_AUTO_START_KOKORO` | `false` | Automatically start Kokoro TTS on startup |

## LiveKit Configuration

| Variable | Default | Description |
|----------|---------|-------------|
| `LIVEKIT_URL` | `ws://localhost:7880` | LiveKit server WebSocket URL |
| `LIVEKIT_API_KEY` | `devkey` | LiveKit API key |
| `LIVEKIT_API_SECRET` | `secret` | LiveKit API secret |

## Audio Feedback & Interaction

| Variable | Default | Description |
|----------|---------|-------------|
| `VOICEMODE_AUDIO_FEEDBACK` | `true` | Play audio feedback when recording starts/stops |

## Streaming Configuration

| Variable | Default | Description |
|----------|---------|-------------|
| `VOICEMODE_STREAMING_ENABLED` | `true` | Enable streaming audio playback |
| `VOICEMODE_STREAM_CHUNK_SIZE` | `4096` | Download chunk size in bytes |
| `VOICEMODE_STREAM_BUFFER_MS` | `150` | Initial buffer before playback (milliseconds) |
| `VOICEMODE_STREAM_MAX_BUFFER` | `2.0` | Maximum buffer size in seconds |

## Debug & Logging

| Variable | Default | Description |
|----------|---------|-------------|
| `VOICEMODE_DEBUG` | `false` | Enable debug logging (`true`, `trace` for verbose) |
| `VOICEMODE_SAVE_AUDIO` | `false` | Save audio recordings to `~/voicemode_audio/` |
| `VOICEMODE_EVENT_LOG_ENABLED` | `true` | Enable structured event logging |
| `VOICEMODE_EVENT_LOG_DIR` | `~/voicemode_logs` | Directory for event log files |
| `VOICEMODE_EVENT_LOG_ROTATION` | `daily` | Log rotation frequency |

## Configuration Examples

### Use Local Kokoro TTS
```bash
export VOICEMODE_TTS_BASE_URL="http://localhost:8880/v1"
export VOICEMODE_TTS_VOICE="af_sky"
```

### Use OpenAI with HD Voice
```bash
export VOICEMODE_TTS_MODEL="tts-1-hd"
export VOICEMODE_TTS_VOICE="nova"
```

### Debug Mode with Audio Saving
```bash
export VOICEMODE_DEBUG="true"
export VOICEMODE_SAVE_AUDIO="true"
```

### Custom Whisper STT Endpoint
```bash
export VOICEMODE_STT_BASE_URL="http://localhost:2022/v1"
```

## Backward Compatibility

For backward compatibility, the following environment variables are also supported (but the `VOICEMODE_` prefixed versions take precedence):

- `TTS_BASE_URL` → `VOICEMODE_TTS_BASE_URL`
- `TTS_VOICE` → `VOICEMODE_TTS_VOICE`
- `TTS_MODEL` → `VOICEMODE_TTS_MODEL`
- `STT_BASE_URL` → `VOICEMODE_STT_BASE_URL`
- `STT_MODEL` → `VOICEMODE_STT_MODEL`
- `OPENAI_TTS_BASE_URL` → `VOICEMODE_OPENAI_TTS_BASE_URL`
- `KOKORO_TTS_BASE_URL` → `VOICEMODE_KOKORO_TTS_BASE_URL`