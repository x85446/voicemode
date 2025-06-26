# Voice Mode Configuration Examples

This directory contains ready-to-use configuration files for various MCP hosts and installation methods.

## Directory Structure

```
config-examples/
├── claude-desktop/     # Claude Desktop configurations
│   ├── uvx.json       # Using uvx (no installation required)
│   ├── pip-install.json # Using globally installed package
│   ├── python-m.json  # Using python -m module execution
│   ├── docker.json    # Using Docker container
│   ├── podman.json    # Using Podman container
│   └── livekit.json   # Example with LiveKit configuration
└── claude-code/       # Claude Code configurations (coming soon)
```

## How to Use

### Claude Desktop

1. Choose the configuration file that matches your installation method
2. Copy the content or download the file
3. Edit your Claude Desktop config file:
   - **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
   - **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`
   - **Linux**: `~/.config/Claude/claude_desktop_config.json`
4. Replace `"your-openai-key"` with your actual OpenAI API key
5. Restart Claude Desktop

### Claude Code

For Claude Code, use the command line:

```bash
export OPENAI_API_KEY=your-openai-key
claude mcp add voice-mcp uvx voice-mcp
```

## Configuration Options

All configurations support these environment variables:

- `OPENAI_API_KEY` (required): Your OpenAI API key
- `STT_BASE_URL`: Custom speech-to-text service URL
- `TTS_BASE_URL`: Custom text-to-speech service URL
- `TTS_VOICE`: Voice selection (alloy, nova, echo, fable, onyx, shimmer)
- `LIVEKIT_URL`: LiveKit server URL for room-based communication
- `VOICE_MCP_DEBUG`: Enable debug mode ("true" or "false")

See [docs/configuration.md](../docs/configuration.md) for complete documentation.