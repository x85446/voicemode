# Environment Variables

Complete reference of all environment variables supported by Voice Mode.

## API Keys

| Variable | Default | Description |
|----------|---------|-------------|
| `OPENAI_API_KEY` | (none) | OpenAI API key - Required for OpenAI services, optional for local-only setups |

## TTS/STT Configuration

| Variable | Default | Description |
|----------|---------|-------------|
| `VOICEMODE_TTS_BASE_URLS` | `http://127.0.0.1:8880/v1,https://api.openai.com/v1` | Comma-separated list of TTS endpoints |
| `VOICEMODE_STT_BASE_URLS` | `http://127.0.0.1:2022/v1,https://api.openai.com/v1` | Comma-separated list of STT endpoints |
| `VOICEMODE_TTS_VOICES` | `af_sky,alloy` | Comma-separated list of preferred voices |
| `VOICEMODE_TTS_MODELS` | `gpt-4o-mini-tts,tts-1-hd,tts-1` | Comma-separated list of TTS models |

## Audio Configuration

| Variable | Default | Description |
|----------|---------|-------------|
| `VOICEMODE_AUDIO_FORMAT` | `pcm` | Default audio format (pcm, opus, mp3, wav, flac, aac) |
| `VOICEMODE_TTS_AUDIO_FORMAT` | `pcm` | TTS audio format override |
| `VOICEMODE_STT_AUDIO_FORMAT` | `mp3` (if base is pcm) | STT audio format override |
| `VOICEMODE_OPUS_BITRATE` | `32000` | Opus bitrate in bps |
| `VOICEMODE_MP3_BITRATE` | `64k` | MP3 bitrate |
| `VOICEMODE_AAC_BITRATE` | `64k` | AAC bitrate |

## Provider Selection

| Variable | Default | Description |
|----------|---------|-------------|
| `VOICEMODE_PREFER_LOCAL` | `true` | Prefer local providers when available |
| `VOICEMODE_AUTO_START_KOKORO` | `false` | Auto-start Kokoro TTS on startup |

## LiveKit Configuration

| Variable | Default | Description |
|----------|---------|-------------|
| `LIVEKIT_URL` | `ws://127.0.0.1:7880` | LiveKit server WebSocket URL |
| `LIVEKIT_API_KEY` | `devkey` | LiveKit API key |
| `LIVEKIT_API_SECRET` | `secret` | LiveKit API secret |

## Audio Feedback

| Variable | Default | Description |
|----------|---------|-------------|
| `VOICEMODE_AUDIO_FEEDBACK` | `true` | Play audio feedback when recording |

## Streaming

| Variable | Default | Description |
|----------|---------|-------------|
| `VOICEMODE_STREAMING_ENABLED` | `true` | Enable streaming audio playback |
| `VOICEMODE_STREAM_CHUNK_SIZE` | `4096` | Download chunk size in bytes |
| `VOICEMODE_STREAM_BUFFER_MS` | `150` | Initial buffer before playback (ms) |
| `VOICEMODE_STREAM_MAX_BUFFER` | `2.0` | Maximum buffer size in seconds |

## Data Saving

| Variable | Default | Description |
|----------|---------|-------------|
| `VOICEMODE_SAVE_ALL` | `false` | Enable all data saving at once |
| `VOICEMODE_SAVE_AUDIO` | `false` | Save audio recordings |
| `VOICEMODE_SAVE_TRANSCRIPTIONS` | `false` | Save transcriptions |
| `VOICEMODE_EVENT_LOG_ENABLED` | `true` | Enable event logging |
| `VOICEMODE_BASE_DIR` | `~/.voicemode` | Base directory for all data |

## Debug & Logging

| Variable | Default | Description |
|----------|---------|-------------|
| `VOICEMODE_DEBUG` | `false` | Enable debug mode (auto-enables all saving) |
| `VOICEMODE_EVENT_LOG_DIR` | `~/.voicemode/logs/events` | Event log directory |
| `VOICEMODE_EVENT_LOG_ROTATION` | `daily` | Log rotation frequency |

## Notes

- Setting `VOICEMODE_DEBUG=true` automatically enables all data saving
- Setting `VOICEMODE_SAVE_ALL=true` enables audio, transcription, and event log saving
- All data is saved under `VOICEMODE_BASE_DIR` (default: `~/.voicemode`)
  - Audio: `~/.voicemode/audio/`
  - Transcriptions: `~/.voicemode/transcriptions/`
  - Logs: `~/.voicemode/logs/`
  - Config: `~/.voicemode/config/`