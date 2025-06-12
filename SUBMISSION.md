# MCP Community Server Submission: voice-mcp

## Community Server List Entry

**[Voice MCP](https://github.com/mbailey/voice-mcp)** - Enable voice conversations with Claude using any OpenAI-compatible STT/TTS service ([voice-mcp.com](https://voice-mcp.com))

## Why voice-mcp is unique

Unlike Cartesia (which focuses on voice platform integration), voice-mcp provides:
- **Universal voice interactions** - Works with any MCP client (Claude Desktop, Claude Code, etc.)
- **OpenAI-compatible** - Supports any STT/TTS service (OpenAI, local Whisper, Kokoro, etc.)
- **Multiple transports** - Local microphone or LiveKit room-based communication
- **Simple setup** - Requires only an OpenAI API key to start

## Security Considerations

- **API Key Security**: Uses environment variables for sensitive credentials
- **Input Validation**: All user inputs are validated before processing
- **Privacy**: Audio is processed per user configuration (local or cloud)
- **Error Handling**: Graceful fallback when services are unavailable

## PR Description Draft

Title: Add voice-mcp to community servers list

Description:
This PR adds voice-mcp to the community servers list. Voice-mcp enables voice conversations with Claude and other LLMs through MCP, supporting both local microphone and LiveKit room-based communication.

Key features:
- Works with any OpenAI-compatible STT/TTS service
- Supports multiple transport modes (local mic or LiveKit rooms)
- Simple setup requiring only an OpenAI API key
- Real-time, low-latency voice interactions

Unlike existing voice-related servers, voice-mcp focuses on enabling natural voice conversations with LLMs rather than just TTS/voice cloning capabilities.

Project links:
- GitHub: https://github.com/mbailey/voice-mcp
- Website: https://voice-mcp.com
- PyPI: https://pypi.org/project/voice-mcp/

## TODO for Logo
Need to create a 12x12 pixel logo. Consider using:
- 🎙️ microphone emoji
- 🗣️ speaking head emoji
- Simple "V" letter design
- Waveform icon