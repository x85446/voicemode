# Voice MCP Container

This repository includes containerization for the voice-mcp server to enable easy deployment and distribution.

## Building the Container

### Using Docker/Podman

```bash
# Build locally
docker build -f Containerfile -t voice-mcp .

# Or with Podman
podman build -f Containerfile -t voice-mcp .
```

### Using GitHub Actions

The container is automatically built and published to GitHub Container Registry when:
- Pushing to main/master branch
- Creating tags starting with 'v'
- Modifying voice-mcp files or container configuration

## Running the Container

### Pull from GitHub Container Registry

```bash
# Pull the latest image
docker pull ghcr.io/mbailey/voice-mcp:latest
```

### Basic Usage

```bash
# Run with environment variables
docker run -e OPENAI_API_KEY=your_key_here \
  -e VOICE_MCP_DEBUG=true \
  ghcr.io/mbailey/voice-mcp:latest
```

### Full Configuration

```bash
docker run \
  -e OPENAI_API_KEY=your_openai_key \
  -e STT_BASE_URL=https://api.openai.com/v1 \
  -e TTS_BASE_URL=https://api.openai.com/v1 \
  -e TTS_VOICE=nova \
  -e TTS_MODEL=tts-1 \
  -e STT_MODEL=whisper-1 \
  -e LIVEKIT_URL=ws://localhost:7880 \
  -e LIVEKIT_API_KEY=devkey \
  -e LIVEKIT_API_SECRET=secret \
  -e VOICE_MCP_DEBUG=true \
  -v $(pwd)/recordings:/app/recordings \
  ghcr.io/mbailey/voice-mcp:latest
```

### Docker Compose

```yaml
version: '3.8'
services:
  voice-mcp:
    image: ghcr.io/mbailey/voice-mcp:latest
    environment:
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - VOICE_MCP_DEBUG=true
      - STT_BASE_URL=https://api.openai.com/v1
      - TTS_BASE_URL=https://api.openai.com/v1
    volumes:
      - ./recordings:/app/recordings
    restart: unless-stopped
```

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `OPENAI_API_KEY` | *required* | OpenAI API key for TTS/STT services |
| `STT_BASE_URL` | `https://api.openai.com/v1` | Speech-to-text service base URL |
| `TTS_BASE_URL` | `https://api.openai.com/v1` | Text-to-speech service base URL |
| `TTS_VOICE` | `nova` | Voice to use for TTS |
| `TTS_MODEL` | `tts-1` | TTS model to use |
| `STT_MODEL` | `whisper-1` | STT model to use |
| `LIVEKIT_URL` | `ws://localhost:7880` | LiveKit server URL |
| `LIVEKIT_API_KEY` | `devkey` | LiveKit API key |
| `LIVEKIT_API_SECRET` | `secret` | LiveKit API secret |
| `VOICE_MCP_DEBUG` | `false` | Enable debug mode (saves audio files) |

## Debug Mode

When `VOICE_MCP_DEBUG=true`, the container will:
- Save all audio files to `/app/recordings/` with timestamps
- Provide verbose logging for troubleshooting
- Log detailed API request/response information

Mount a volume to persist debug recordings:
```bash
-v $(pwd)/recordings:/app/recordings
```

## MCP Integration

To use this container with MCP clients:

### .mcp.json Configuration

```json
{
  "mcpServers": {
    "voice-mcp": {
      "type": "stdio",
      "command": "docker",
      "args": [
        "run", "-i", "--rm",
        "-e", "OPENAI_API_KEY=your_key_here",
        "-e", "VOICE_MCP_DEBUG=true",
        "ghcr.io/mbailey/voice-mcp:latest"
      ]
    }
  }
}
```

### Local Development

For local development with bind mounts:
```json
{
  "mcpServers": {
    "voice-mcp": {
      "type": "stdio", 
      "command": "docker",
      "args": [
        "run", "-i", "--rm",
        "-v", "./recordings:/app/recordings",
        "-e", "OPENAI_API_KEY=your_key_here",
        "voice-mcp:local"
      ]
    }
  }
}
```

## Supported Platforms

The container is built for:
- `linux/amd64` (x86_64)
- `linux/arm64` (ARM 64-bit)

## Audio Support

The container includes:
- PortAudio for cross-platform audio I/O
- ALSA utilities for Linux audio
- PulseAudio utilities for desktop audio
- FFmpeg for audio format conversion
- libsndfile for audio file processing

## Troubleshooting

### Audio Issues
- Ensure proper audio device access if running with audio hardware
- Use debug mode to inspect audio file generation
- Check logs for sounddevice or audio library errors

### API Issues  
- Verify `OPENAI_API_KEY` is set correctly
- Check API endpoints are accessible from container
- Review debug logs for API request/response details

### MCP Connection Issues
- Ensure container can communicate via stdio
- Check that MCP client can execute docker commands
- Verify environment variables are passed correctly