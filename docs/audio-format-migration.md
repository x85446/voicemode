# Audio Format Migration Guide

## Overview

Voice Mode now uses **Opus** audio format by default instead of MP3. This change provides:

- **50-80% smaller files** - More efficient storage and transmission
- **Lower latency** - Better for real-time communication
- **Voice optimization** - Opus is designed specifically for speech
- **Modern codec** - Better compression algorithms

## Quick Start

For most users, no action is required. Voice Mode will automatically use Opus format for new installations.

### To Keep Using MP3

If you prefer to continue using MP3 format:

```bash
export VOICE_AUDIO_FORMAT="mp3"
```

Or add to your MCP configuration:

```json
{
  "mcpServers": {
    "voice-mode": {
      "command": "uvx",
      "args": ["voice-mode"],
      "env": {
        "OPENAI_API_KEY": "your-key",
        "VOICE_AUDIO_FORMAT": "mp3"
      }
    }
  }
}
```

## Configuration Options

### Basic Configuration

```bash
# Set default format for all operations
export VOICE_AUDIO_FORMAT="opus"  # Options: opus, mp3, wav, flac, aac
```

### Advanced Configuration

```bash
# Different formats for TTS and STT
export VOICE_TTS_AUDIO_FORMAT="opus"    # For text-to-speech
export VOICE_STT_AUDIO_FORMAT="mp3"     # For speech-to-text upload

# Quality settings
export VOICE_OPUS_BITRATE="32000"       # Opus bitrate (default: 32kbps)
export VOICE_MP3_BITRATE="64k"          # MP3 bitrate (default: 64k)
export VOICE_AAC_BITRATE="64k"          # AAC bitrate (default: 64k)
```

## Provider Compatibility

Voice Mode automatically validates format compatibility with your providers:

| Provider | TTS Formats | STT Formats |
|----------|-------------|-------------|
| OpenAI | opus, mp3, aac, flac, wav, pcm | mp3, opus, wav, flac, m4a, webm |
| Kokoro (local) | mp3, wav | N/A |
| Whisper.cpp (local) | N/A | wav, mp3, opus, flac, m4a |

If you select an unsupported format, Voice Mode will automatically fallback to a compatible format.

## Migration from Existing Setup

### Checking Your Current Setup

If you have existing audio files saved with `VOICE_MCP_SAVE_AUDIO=true`, they are likely in MP3 format. You can check:

```bash
ls ~/voice-mcp_audio/
```

### Gradual Migration

You can run both formats side-by-side:

1. Keep existing MP3 files
2. New recordings will use Opus
3. Both formats will work seamlessly

### Converting Existing Files

To convert existing MP3 files to Opus (optional):

```bash
# Using ffmpeg
for file in ~/voice-mcp_audio/*.mp3; do
    ffmpeg -i "$file" -c:a libopus -b:a 32k "${file%.mp3}.opus"
done
```

## Troubleshooting

### Issue: "Provider doesn't support Opus"

Voice Mode will automatically fallback to a supported format. You'll see a log message like:
```
Format 'opus' not supported by kokoro, using 'mp3' instead
```

### Issue: "Audio playback issues"

Some older systems might have issues with Opus playback. Try:

1. Update your audio libraries:
   ```bash
   # Ubuntu/Debian
   sudo apt update && sudo apt install libopus0 libopusfile0
   
   # macOS
   brew install opus opus-tools
   ```

2. Or switch back to MP3:
   ```bash
   export VOICE_AUDIO_FORMAT="mp3"
   ```

### Issue: "Larger file sizes than expected"

Opus files might appear larger if saved in an OGG container. The actual audio data is still compressed efficiently.

## Format Comparison

| Format | File Size* | Quality | Latency | Best For |
|--------|-----------|---------|---------|----------|
| Opus | Smallest (100KB) | Excellent for voice | Lowest | Default choice, streaming |
| MP3 | Medium (500KB) | Good | Medium | Compatibility |
| AAC | Medium (450KB) | Good | Medium | Apple ecosystem |
| FLAC | Large (2MB) | Lossless | Low | Archival |
| WAV | Largest (5MB) | Uncompressed | Lowest | Processing |

*Approximate sizes for 1 minute of speech

## Benefits of Opus

1. **Bandwidth Efficiency**: Crucial for cloud API calls
2. **Real-time Performance**: Better for LiveKit streaming
3. **Dynamic Bitrate**: Adapts to network conditions
4. **Wide Platform Support**: Works on all modern systems
5. **Future-proof**: Active development and improvements

## Reverting to MP3

If you need to revert to MP3 as default:

1. Set environment variable:
   ```bash
   export VOICE_AUDIO_FORMAT="mp3"
   ```

2. Or update your MCP configuration as shown above

3. Restart your MCP client

Your existing Opus files will continue to work, and new files will be created in MP3 format.