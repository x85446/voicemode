# Audio Format Configuration Implementation

## Summary

Implemented configurable audio format support in voice-mode with PCM as the default format for TTS streaming, replacing the hardcoded MP3 format. While Opus was initially considered, PCM provides better streaming performance as OpenAI doesn't properly support Opus for streaming TTS.

## Changes Made

### 1. Configuration Module (`voice_mode/config.py`)

Added audio format configuration:
- `AUDIO_FORMAT` - Primary format (default: "pcm")
- `TTS_AUDIO_FORMAT` - TTS-specific override (default: "pcm" for optimal streaming)
- `STT_AUDIO_FORMAT` - STT-specific override (default: "mp3" if primary is pcm, since OpenAI Whisper doesn't support pcm)
- Format validation with fallback to pcm
- Format-specific bitrate settings (OPUS_BITRATE, MP3_BITRATE, AAC_BITRATE)

Added utility functions:
- `get_provider_supported_formats()` - Returns supported formats by provider
- `validate_audio_format()` - Validates and adjusts format for provider compatibility
- `get_audio_loader_for_format()` - Returns appropriate PyDub loader
- `get_format_export_params()` - Returns export parameters for each format

### 2. Core Module (`voice_mode/core.py`)

Updated `text_to_speech()` function:
- Replaced hardcoded `audio_format = "mp3"` with configurable format
- Added provider detection from base URL
- Format validation before API request
- Dynamic audio loading based on format
- Updated fallback file extension

### 3. Conversation Module (`voice_mode/tools/conversation.py`)

Updated `speech_to_text()` function:
- Replaced hardcoded MP3 conversion with configurable format
- Added provider detection for STT
- Format validation for upload
- Dynamic export parameters based on format
- Updated variable names from `mp3_file` to `export_file`

### 4. Documentation

- **README.md**: Added audio format configuration section
- **CHANGELOG.md**: Documented the new feature
- **docs/audio-format-migration.md**: Comprehensive migration guide

### 5. Testing

- **tests/test_audio_format_config.py**: Comprehensive test suite for format configuration
- Tests cover default values, custom configuration, validation, and format utilities

### 6. Utilities

- **voice_mode/utils/format_migration.py**: Migration detection utilities (for future use)

## Provider Format Support

| Provider | TTS Formats | STT Formats |
|----------|-------------|-------------|
| OpenAI | opus, mp3, aac, flac, wav, pcm | mp3, opus, wav, flac, m4a, webm |
| Kokoro | mp3, wav | N/A |
| Whisper.cpp | N/A | wav, mp3, opus, flac, m4a |

## Benefits

1. **Performance**: PCM provides zero-latency streaming for TTS (no decoding required)
2. **Flexibility**: Users can choose format based on their needs
3. **Compatibility**: Automatic fallback ensures providers always get supported formats
4. **Quality**: Format-specific bitrate settings allow quality tuning for compressed formats
5. **Future-proof**: Easy to add new formats as providers support them
6. **Streaming**: PCM avoids issues with Opus containers that break OpenAI's streaming

## Backward Compatibility

- Existing MP3 workflows continue to work
- Users can set `VOICEMODE_AUDIO_FORMAT=mp3` to maintain previous behavior
- All existing audio files remain playable
- No breaking changes to the API
- Default changed from MP3 to PCM for better streaming performance

## Next Steps

1. Monitor user feedback on PCM streaming performance
2. Consider adding format auto-detection based on provider capabilities
3. Investigate Opus container issues with OpenAI streaming
4. Consider adding format conversion utilities for non-streaming use cases