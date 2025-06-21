# Migration Guide: Environment Variable Updates

## Overview

Starting with version 2.2.0, all environment variables have been renamed from `VOICE_MCP_` prefix to `VOICEMODE_` prefix to reflect the project's new name.

## Environment Variable Changes

### Core Configuration

| Old Variable | New Variable |
|--------------|--------------|
| `VOICE_MCP_DEBUG` | `VOICEMODE_DEBUG` |
| `VOICE_MCP_SAVE_AUDIO` | `VOICEMODE_SAVE_AUDIO` |
| `VOICE_MCP_AUDIO_FEEDBACK` | `VOICEMODE_AUDIO_FEEDBACK` |
| `VOICE_MCP_FEEDBACK_VOICE` | `VOICEMODE_FEEDBACK_VOICE` |
| `VOICE_MCP_FEEDBACK_MODEL` | `VOICEMODE_FEEDBACK_MODEL` |
| `VOICE_MCP_FEEDBACK_STYLE` | `VOICEMODE_FEEDBACK_STYLE` |
| `VOICE_MCP_PREFER_LOCAL` | `VOICEMODE_PREFER_LOCAL` |
| `VOICE_MCP_AUTO_START_KOKORO` | `VOICEMODE_AUTO_START_KOKORO` |

### New Prefixed Variables

These variables previously had no prefix but now use `VOICEMODE_`:

| Old Variable | New Variable |
|--------------|--------------|
| `VOICE_ALLOW_EMOTIONS` | `VOICEMODE_ALLOW_EMOTIONS` |
| `VOICE_EMOTION_AUTO_UPGRADE` | `VOICEMODE_EMOTION_AUTO_UPGRADE` |

### New Audio Format Variables

New variables for configuring audio formats (defaulting to Opus):

- `VOICEMODE_AUDIO_FORMAT` - Primary audio format (default: opus)
- `VOICEMODE_TTS_AUDIO_FORMAT` - TTS-specific override
- `VOICEMODE_STT_AUDIO_FORMAT` - STT-specific override
- `VOICEMODE_OPUS_BITRATE` - Opus bitrate (default: 32000)
- `VOICEMODE_MP3_BITRATE` - MP3 bitrate (default: 64k)
- `VOICEMODE_AAC_BITRATE` - AAC bitrate (default: 64k)

### Variables That Remain Unchanged

These standard service variables keep their original names:

- `OPENAI_API_KEY`
- `TTS_BASE_URL`
- `STT_BASE_URL`
- `TTS_VOICE`
- `TTS_MODEL`
- `STT_MODEL`
- `LIVEKIT_URL`
- `LIVEKIT_API_KEY`
- `LIVEKIT_API_SECRET`

## Directory Path Changes

Debug and audio directories have also been renamed:

| Old Path | New Path |
|----------|----------|
| `~/voice-mcp_recordings/` | `~/voicemode_recordings/` |
| `~/voice-mcp_audio/` | `~/voicemode_audio/` |

## Migration Steps

1. **Update Environment Variables**
   ```bash
   # Old
   export VOICE_MCP_DEBUG=true
   export VOICE_MCP_SAVE_AUDIO=true
   
   # New
   export VOICEMODE_DEBUG=true
   export VOICEMODE_SAVE_AUDIO=true
   ```

2. **Update Configuration Files**
   - Update `.env` files
   - Update shell configuration (`.bashrc`, `.zshrc`, etc.)
   - Update MCP configuration files

3. **Update Claude Desktop Configuration**
   ```json
   {
     "mcpServers": {
       "voice-mode": {
         "command": "uvx",
         "args": ["voice-mode"],
         "env": {
           "OPENAI_API_KEY": "your-key",
           "VOICEMODE_DEBUG": "true"  // Updated from VOICE_MCP_DEBUG
         }
       }
     }
   }
   ```

4. **Move Existing Debug Files** (optional)
   ```bash
   # Move recordings
   mv ~/voice-mcp_recordings ~/voicemode_recordings
   
   # Move audio files
   mv ~/voice-mcp_audio ~/voicemode_audio
   ```

## Audio Format Migration

The default audio format has changed from MP3 to Opus for better performance:

- **To keep using MP3**: Set `VOICEMODE_AUDIO_FORMAT=mp3`
- **To use the new default (Opus)**: No action required
- **Benefits of Opus**: 50-80% smaller files, lower latency, optimized for voice

## Example Configuration

```bash
# Required
export OPENAI_API_KEY="your-openai-key"

# Optional - Debug and audio saving
export VOICEMODE_DEBUG=true
export VOICEMODE_SAVE_AUDIO=true

# Optional - Audio format (defaults to opus)
export VOICEMODE_AUDIO_FORMAT=opus
export VOICEMODE_OPUS_BITRATE=32000

# Optional - Provider preferences
export VOICEMODE_PREFER_LOCAL=true
export VOICEMODE_AUTO_START_KOKORO=true

# Optional - Emotional TTS
export VOICEMODE_ALLOW_EMOTIONS=true
```

## Need Help?

If you encounter any issues during migration:
1. Check the [documentation](https://docs.getvoicemode.com)
2. Report issues at [GitHub Issues](https://github.com/mbailey/voicemode/issues)
3. Join our community discussions