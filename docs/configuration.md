# Voice-MCP Configuration

> For integration-specific setup instructions, see the [integration guides](integrations/README.md).

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
| `VOICEMODE_TTS_BASE_URLS` | `http://localhost:8880/v1,https://api.openai.com/v1` | Comma-separated list of TTS endpoints in priority order |
| `VOICEMODE_TTS_VOICES` | `af_sky,alloy` | Comma-separated list of preferred voices in priority order |
| `VOICEMODE_TTS_MODELS` | `gpt-4o-mini-tts,tts-1-hd,tts-1` | Comma-separated list of TTS models in priority order |

### Available Voices

- **OpenAI**: `alloy`, `nova`, `echo`, `fable`, `onyx`, `shimmer`
- **Kokoro**: `af_sky`, `af_sarah`, `am_adam`, `af_nicole`, `am_michael`

## STT (Speech-to-Text) Configuration

| Variable | Default | Description |
|----------|---------|-------------|
| `VOICEMODE_STT_BASE_URLS` | `http://localhost:2022/v1,https://api.openai.com/v1` | Comma-separated list of STT endpoints in priority order |

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
| `VOICEMODE_DEBUG` | `false` | Enable debug logging (`true`, `trace` for verbose). Automatically enables all saving. |
| `VOICEMODE_SAVE_ALL` | `false` | Enable all data saving (audio, transcriptions, event logs) |
| `VOICEMODE_SAVE_AUDIO` | `false` | Save audio recordings to `~/.voicemode/audio/` |
| `VOICEMODE_SAVE_TRANSCRIPTIONS` | `false` | Save transcriptions to `~/.voicemode/transcriptions/` |
| `VOICEMODE_EVENT_LOG_ENABLED` | `true` | Enable structured event logging |
| `VOICEMODE_EVENT_LOG_DIR` | `~/.voicemode/logs/events` | Directory for event log files |
| `VOICEMODE_EVENT_LOG_ROTATION` | `daily` | Log rotation frequency |
| `VOICEMODE_BASE_DIR` | `~/.voicemode` | Base directory for all voicemode data |

## Configuration Examples

### Prioritize Local Kokoro TTS
```bash
export VOICEMODE_TTS_BASE_URLS="http://localhost:8880/v1,https://api.openai.com/v1"
export VOICEMODE_TTS_VOICES="af_sky,nova"
```

### Use Only OpenAI with HD Voice
```bash
export VOICEMODE_TTS_BASE_URLS="https://api.openai.com/v1"
export VOICEMODE_TTS_VOICES="nova,alloy"
export VOICEMODE_TTS_MODELS="tts-1-hd,tts-1"
```

### Debug Mode (Automatically Saves Everything)
```bash
export VOICEMODE_DEBUG="true"
```

### Save All Data
```bash
export VOICEMODE_SAVE_ALL="true"
```

### Fine-grained Saving Control
```bash
export VOICEMODE_SAVE_AUDIO="true"
export VOICEMODE_SAVE_TRANSCRIPTIONS="true"
```

### Prioritize Local Whisper STT
```bash
export VOICEMODE_STT_BASE_URLS="http://localhost:2022/v1,https://api.openai.com/v1"
```

## Migration from Legacy Variables

The following legacy environment variables have been replaced with list-based configuration:

| Legacy Variable | New Variable | Notes |
|----------------|--------------|-------|
| `VOICEMODE_TTS_BASE_URL` | `VOICEMODE_TTS_BASE_URLS` | Now comma-separated list |
| `VOICEMODE_STT_BASE_URL` | `VOICEMODE_STT_BASE_URLS` | Now comma-separated list |
| `VOICEMODE_TTS_VOICE` | `VOICEMODE_TTS_VOICES` | Now comma-separated list |
| `VOICEMODE_TTS_MODEL` | `VOICEMODE_TTS_MODELS` | Now comma-separated list |

The new list-based approach allows Voice Mode to automatically failover between providers and select the best available option based on health checks and feature requirements.
