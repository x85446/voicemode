# MCP Servers

# XXX This doc needs updates

This directory contains the Model Context Protocol (MCP) server implementations for voice-mcp.

## Available Servers

- `voice-mcp` - Local or Livekit voice communication server.
- `livekit-admin-mcp` - LiveKit administration tools
- `livekit-agent` - LiveKit agent implementation

## Usage

These servers are meant to be configured in your Claude Desktop app or other MCP-compatible clients.

For development, you can symlink these scripts to a directory in your PATH:

```bash
ln -s /path/to/voice-mcp/mcp-servers/livekit-voice-mcp ~/bin/
```

## Configuration

Add to your Claude Desktop config:

```json
{
  "mcpServers": {
    "voice-mcp": {
      "command": "/path/to/voice-mcp/mcp-servers/voice-mcp"
    }
  }
}
```

## Local Voice MCP Features

The `voice-mcp` server provides direct microphone access without requiring LiveKit:

- **ask_local_voice_question** - Speak a question using TTS and listen for voice response
- **speak_text** - Speak text using TTS without listening  
- **listen_for_speech** - Listen for speech and convert to text using STT
- **check_audio_devices** - List available audio input/output devices

### Dependencies

- Uses `sounddevice` for local microphone access
- Supports both Kokoro (local) and OpenAI TTS
- Supports both local Whisper and OpenAI STT
- Records at 16kHz mono for optimal speech recognition

### Configuration

Environment variables:

**Audio Saving:**
- `SAVE_AUDIO` - Enable saving recorded audio to disk (default: false)
- `AUDIO_SAVE_DIR` - Directory to save audio files (default: /tmp/voice-mcp-audio)

**Service Configuration:**
- `OPENAI_BASE_URL` - Base URL for OpenAI-compatible APIs (e.g., local Whisper)
- `STT_PROVIDER` - Speech-to-text provider: local or openai (default: local)
- `STT_BASE_URL` - Base URL for local STT (default: http://localhost:2022/v1)
- `KOKORO_URL` - Kokoro TTS service URL (default: http://127.0.0.1:8880)
- `KOKORO_VOICE` - Kokoro voice selection (default: af_sky)

To enable audio saving for debugging:
```bash
export SAVE_AUDIO=true
export AUDIO_SAVE_DIR=/path/to/audio/files
```

To use local Whisper or other OpenAI-compatible services:
```bash
export OPENAI_BASE_URL=http://localhost:2022/v1
export STT_PROVIDER=local
```

Audio files are saved as WAV with timestamps:
- `timeout_recording_YYYYMMDD_HHMMSS_mmm.wav` - Fixed duration recordings
- `vad_recording_YYYYMMDD_HHMMSS_mmm.wav` - VAD-based recordings
