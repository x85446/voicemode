# Audio Format Configuration and Streaming Implementation

## Summary

This release adds configurable audio format support with Opus as the default, streaming audio playback infrastructure, and the ability to override audio formats per request.

## Key Features

### 1. Audio Format Configuration
- Added `VOICEMODE_AUDIO_FORMAT` environment variable (default: "opus")
- Separate format control for TTS and STT via `VOICEMODE_TTS_AUDIO_FORMAT` and `VOICEMODE_STT_AUDIO_FORMAT`
- Provider-aware format validation and fallback
- Support for: opus, mp3, wav, flac, aac, pcm

### 2. Streaming Audio Playback
- Added streaming infrastructure to reduce Time To First Audio (TTFA)
- Configuration via:
  - `VOICEMODE_STREAMING_ENABLED` (default: true)
  - `VOICEMODE_STREAM_CHUNK_SIZE` (default: 4096)
  - `VOICEMODE_STREAM_BUFFER_MS` (default: 150)
  - `VOICEMODE_STREAM_MAX_BUFFER` (default: 2.0 seconds)
- Currently uses buffered streaming approach due to OpenAI API limitations

### 3. Per-Request Format Override
- Added `audio_format` parameter to `converse()` and `ask_voice_question()` tools
- Allows overriding the default format on a per-request basis
- Useful for working around provider-specific issues

### 4. Environment Variable Migration
- All `VOICE_MCP_` environment variables renamed to `VOICEMODE_`
- Clean break with no backward compatibility (as requested)

## Known Issues

### OpenAI + Opus Audio Quality
- OpenAI TTS with Opus format produces "terrible" audio quality
- Documented in `docs/issues/openai-opus-audio-quality.md`
- Workaround: Use MP3 for OpenAI, Opus for other providers

## Technical Details

### Provider Format Support
```python
# Provider format capabilities
"openai": {
    "tts": ["opus", "mp3", "aac", "flac", "wav", "pcm"],
    "stt": ["mp3", "opus", "wav", "flac", "m4a", "webm"]
},
"kokoro": {
    "tts": ["mp3", "wav"],  # May support more
    "stt": []  # TTS only
},
"whisper-local": {
    "tts": [],  # STT only
    "stt": ["wav", "mp3", "opus", "flac", "m4a"]
}
```

### Usage Examples

#### Set default format via environment:
```bash
export VOICEMODE_AUDIO_FORMAT=mp3
```

#### Override format per request:
```python
# Use MP3 for better compatibility
await converse("Hello world", audio_format="mp3")

# Use Opus for smaller file size
await converse("Hello world", audio_format="opus")
```

## Migration Guide

### Environment Variables
Replace all `VOICE_MCP_` prefixes with `VOICEMODE_`:
- `VOICE_MCP_DEBUG` → `VOICEMODE_DEBUG`
- `VOICE_MCP_SAVE_AUDIO` → `VOICEMODE_SAVE_AUDIO`
- `VOICE_MCP_AUDIO_FEEDBACK` → `VOICEMODE_AUDIO_FEEDBACK`
- etc.

### Audio Format
The default format is now Opus. If you experience issues:
1. For OpenAI TTS: Set `VOICEMODE_TTS_AUDIO_FORMAT=mp3`
2. For specific requests: Use `audio_format="mp3"` parameter

## Testing Notes

- Kokoro + Opus: Good quality ✅
- OpenAI + Opus: Poor quality ❌ (use MP3)
- Streaming: Currently minimal benefit as full buffering still occurs
- TTFA metric: Added but shows 0s until true streaming is implemented

## Future Work

1. Implement true HTTP streaming when API support becomes available
2. Add provider-specific default formats
3. Investigate OpenAI Opus encoding issues
4. Add quality detection and automatic fallback