# Audio Format Configuration Specification

## Overview

This specification describes making the audio format configurable in voicemode, with Opus as the default format for improved streaming performance and reduced bandwidth usage.

## Current State

- Audio format is hardcoded as "mp3" in `voicemode/core.py` (line 101)
- No environment variable control for audio formats
- STT uploads always use MP3 format
- All TTS responses are in MP3 format

## Proposed Changes

### 1. Environment Variables

Add the following environment variables:

```bash
# Primary audio format configuration
VOICEMODE_AUDIO_FORMAT=opus  # Default: opus (was mp3)

# Service-specific overrides
VOICEMODE_TTS_AUDIO_FORMAT=   # Override for TTS only
VOICEMODE_STT_AUDIO_FORMAT=   # Override for STT uploads

# Format-specific quality settings
VOICEMODE_OPUS_BITRATE=32000  # Opus bitrate (default: 32000)
VOICEMODE_MP3_BITRATE=64k     # MP3 bitrate (default: 64k)
```

### 2. Configuration Module Updates

In `voicemode/config.py`, add:

```python
# Audio format configuration
VOICEMODE_AUDIO_FORMAT = os.getenv("VOICEMODE_AUDIO_FORMAT", "opus").lower()
VOICEMODE_TTS_AUDIO_FORMAT = os.getenv("VOICEMODE_TTS_AUDIO_FORMAT", VOICEMODE_AUDIO_FORMAT).lower()
VOICEMODE_STT_AUDIO_FORMAT = os.getenv("VOICEMODE_STT_AUDIO_FORMAT", VOICEMODE_AUDIO_FORMAT).lower()

# Supported formats by provider
SUPPORTED_FORMATS = {
    "openai": ["mp3", "opus", "aac", "flac", "wav", "pcm"],
    "kokoro": ["mp3", "opus", "aac", "flac", "wav", "pcm"],  # Assuming OpenAI compatibility
}

# Format-specific settings
VOICEMODE_OPUS_BITRATE = int(os.getenv("VOICEMODE_OPUS_BITRATE", "32000"))
VOICEMODE_MP3_BITRATE = os.getenv("VOICEMODE_MP3_BITRATE", "64k")

def validate_audio_format(format: str, provider: str) -> bool:
    """Validate if a format is supported by a provider."""
    provider_formats = SUPPORTED_FORMATS.get(provider, SUPPORTED_FORMATS["openai"])
    return format in provider_formats

def get_audio_format_for_provider(provider: str, service_type: str = "tts") -> str:
    """Get the appropriate audio format for a provider."""
    if service_type == "tts":
        format = VOICEMODE_TTS_AUDIO_FORMAT
    elif service_type == "stt":
        format = VOICEMODE_STT_AUDIO_FORMAT
    else:
        format = VOICEMODE_AUDIO_FORMAT
    
    # Validate and fallback to mp3 if unsupported
    if not validate_audio_format(format, provider):
        logger.warning(f"Format {format} not supported by {provider}, falling back to mp3")
        return "mp3"
    
    return format
```

### 3. Core Module Updates

In `voicemode/core.py`, update the `text_to_speech` function:

```python
async def text_to_speech(text: str, openai_clients: dict, client_key: str = "tts", 
                        voice: str = TTS_VOICE, model: str = TTS_MODEL,
                        provider: str = None, **kwargs) -> Tuple[bytes, float, str]:
    """Convert text to speech audio."""
    start_time = time.time()
    
    # Get appropriate audio format for the provider
    if provider is None:
        # Try to detect provider from client_key or base URL
        provider = detect_provider_from_client(openai_clients[client_key])
    
    audio_format = get_audio_format_for_provider(provider, "tts")
    
    request_params = {
        "model": model,
        "input": text,
        "voice": voice,
        "response_format": audio_format,  # Now configurable
    }
    
    # Add format-specific parameters
    if audio_format == "opus" and provider == "openai":
        # OpenAI might support bitrate configuration in the future
        pass
    
    # ... rest of the function
    
    # Update file extension based on format
    with tempfile.NamedTemporaryFile(delete=False, suffix=f".{audio_format}") as tmp_file:
        tmp_file.write(response_content)
        temp_filename = tmp_file.name
    
    # Update audio loading based on format
    if audio_format in ["mp3", "opus", "aac", "flac"]:
        audio = AudioSegment.from_file(temp_filename, format=audio_format)
    elif audio_format == "wav":
        audio = AudioSegment.from_wav(temp_filename)
    elif audio_format == "pcm":
        # PCM requires additional parameters
        audio = AudioSegment.from_raw(
            temp_filename, 
            sample_width=2,  # 16-bit
            frame_rate=24000,  # Standard TTS rate
            channels=1
        )
    else:
        raise ValueError(f"Unsupported audio format: {audio_format}")
```

### 4. STT Updates

In `voicemode/tools/conversation.py`, update the `speech_to_text` function:

```python
# Convert audio to configured format for upload
upload_format = get_audio_format_for_provider(
    detect_provider_from_client(openai_clients['stt']), 
    "stt"
)

# Export in the configured format
buffer = io.BytesIO()
recorded_audio.export(buffer, format=upload_format)
buffer.seek(0)

# Create file-like object with proper extension
file_tuple = (f"audio.{upload_format}", buffer, f"audio/{upload_format}")
```

### 5. Benefits by Format

| Format | File Size | Latency | Quality | Best For |
|--------|-----------|---------|---------|----------|
| Opus   | Smallest (10-20KB/s) | Lowest | Excellent for voice | Streaming, real-time |
| AAC    | Small (16-32KB/s) | Low | Very good | Mobile, web |
| MP3    | Medium (32-64KB/s) | Medium | Good | Compatibility |
| FLAC   | Large (200-400KB/s) | Medium | Lossless | Quality priority |
| WAV    | Largest (700KB/s) | Low | Lossless | Processing |
| PCM    | Largest (700KB/s) | Lowest | Raw | Direct playback |

### 6. Migration Guide

For existing users:

1. **No action required** - System defaults to Opus but falls back to MP3 if needed
2. **To keep using MP3** - Set `VOICEMODE_AUDIO_FORMAT=mp3`
3. **For maximum compatibility** - Use MP3 or AAC
4. **For best performance** - Use Opus (default)

### 7. Testing Strategy

1. Test each format with both OpenAI and Kokoro
2. Verify fallback behavior for unsupported formats
3. Measure file sizes and latency for each format
4. Test format-specific parameters (bitrates, etc.)
5. Ensure backward compatibility

### 8. Future Enhancements

1. **Streaming playback** - Separate spec for progressive audio playback
2. **Adaptive format selection** - Choose format based on network conditions
3. **Format conversion** - Local conversion between formats
4. **Quality profiles** - Preset configurations for different use cases

## Implementation Priority

1. ✅ Environment variable configuration
2. ✅ Format validation and fallback logic
3. ✅ Update TTS to use configurable format
4. ✅ Update STT to use configurable format
5. ⏳ Add format-specific optimizations
6. ⏳ Comprehensive testing
7. ⏳ Documentation updates

## Backwards Compatibility

- Default behavior changes from MP3 to Opus
- Existing MP3-based workflows continue to work
- Format validation ensures graceful degradation
- Clear migration path documented