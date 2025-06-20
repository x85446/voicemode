# Voice MCP Configuration Guide

This guide covers how to configure voice-mode for various MCP hosts and installation methods.

## Table of Contents

- [Claude Code](#claude-code)
- [Claude Desktop](#claude-desktop)
- [LiveKit Configuration](#livekit-configuration)
- [Configuration Options](#configuration-options)
- [Environment Variables](#environment-variables)

## Claude Code

Claude Code uses the `claude mcp add` command to configure MCP servers.

### Installation Methods

#### Using uvx (Recommended)

```bash
export OPENAI_API_KEY=your-openai-key
claude mcp add voice-mode uvx voice-mode
```

#### Using pip install

```bash
export OPENAI_API_KEY=your-openai-key
pip install voice-mode
claude mcp add voice-mode voice-mode
```

## Claude Desktop

Claude Desktop configuration files are located at:
- **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`
- **Linux**: `~/.config/Claude/claude_desktop_config.json`

### Installation Methods

#### Using uvx (Recommended)

No installation required - runs directly:

```json
{
  "mcpServers": {
    "voice-mode": {
      "command": "uvx",
      "args": ["voice-mode"],
      "env": {
        "OPENAI_API_KEY": "your-openai-key"
      }
    }
  }
}
```

[Download config](../config-examples/claude-desktop/uvx.json)

#### Using pip install

If you've installed voice-mode globally:

```json
{
  "mcpServers": {
    "voice-mode": {
      "command": "voice-mode",
      "env": {
        "OPENAI_API_KEY": "your-openai-key"
      }
    }
  }
}
```

[Download config](../config-examples/claude-desktop/pip-install.json)

#### Using python -m

If you've installed via pip and prefer module execution:

```json
{
  "mcpServers": {
    "voice-mode": {
      "command": "python",
      "args": ["-m", "voice_mcp"],
      "env": {
        "OPENAI_API_KEY": "your-openai-key"
      }
    }
  }
}
```

[Download config](../config-examples/claude-desktop/python-m.json)

#### With LiveKit Support

Add LiveKit configuration to any of the above:

```json
{
  "mcpServers": {
    "voice-mode": {
      "command": "uvx",
      "args": ["voice-mode"],
      "env": {
        "OPENAI_API_KEY": "your-openai-key",
        "LIVEKIT_URL": "wss://your-app.livekit.cloud",
        "LIVEKIT_API_KEY": "your-api-key",
        "LIVEKIT_API_SECRET": "your-api-secret"
      }
    }
  }
}
```

[Download config](../config-examples/claude-desktop/livekit.json)

## LiveKit Configuration

LiveKit enables room-based voice communication instead of using the local microphone. This is perfect for accessing voice-mode from your phone, tablet, or any remote device.

**📖 For detailed setup instructions, see the [LiveKit Integration Guide](livekit/README.md)**

### Quick Configuration

For [LiveKit Cloud](livekit/cloud-setup.md) (recommended):

```bash
export LIVEKIT_URL="wss://your-project.livekit.cloud"
export LIVEKIT_API_KEY="your-api-key"
export LIVEKIT_API_SECRET="your-api-secret"
```

For [self-hosted LiveKit](livekit/local-setup.md):

```bash
export LIVEKIT_URL="ws://localhost:7880"
export LIVEKIT_API_KEY="devkey"
export LIVEKIT_API_SECRET="secret"
```

### Transport Selection

When LiveKit is configured, voice-mode can automatically select the best transport:

- **`transport: "auto"`** (default) - Try LiveKit first, fall back to local microphone
- **`transport: "livekit"`** - Force LiveKit transport
- **`transport: "local"`** - Force local microphone

## Configuration Options

### Required Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `OPENAI_API_KEY` | OpenAI API key for STT/TTS | Required |

### Optional Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `STT_BASE_URL` | Base URL for STT service | `https://api.openai.com/v1` |
| `TTS_BASE_URL` | Base URL for TTS service | `https://api.openai.com/v1` |
| `TTS_VOICE` | Voice for text-to-speech | `alloy` |
| `TTS_MODEL` | TTS model to use | `tts-1` |
| `STT_MODEL` | STT model to use | `whisper-1` |
| `VOICE_MCP_PREFER_LOCAL` | Prefer local providers when available | `true` |
| `LIVEKIT_URL` | LiveKit server URL | None |
| `LIVEKIT_API_KEY` | LiveKit API key | None |
| `LIVEKIT_API_SECRET` | LiveKit API secret | None |
| `VOICE_MCP_DEBUG` | Enable debug mode | `false` |

### Available TTS Voices

- `alloy` (default) - Natural, conversational
- `nova` - Warm and friendly
- `alloy` - Neutral and balanced
- `echo` - Warm and engaging
- `fable` - Expressive storyteller
- `onyx` - Deep and authoritative
- `shimmer` - Clear and energetic

### Local Service Configuration

For self-hosted STT/TTS services:

```bash
# Local Whisper STT
export STT_BASE_URL="http://localhost:2022/v1"

# Local Kokoro TTS
export TTS_BASE_URL="http://localhost:8880/v1"
export TTS_VOICE="af_sky"
```

### Automatic Provider Selection

When `VOICE_MCP_PREFER_LOCAL=true` (default), voice-mode automatically uses local services when available:

- **Kokoro TTS** at `localhost:8880` - Used automatically if running
- **Whisper.cpp** at `localhost:2022` - Used automatically if running
- Falls back to OpenAI services if local providers are not available

This means you can simply start Kokoro or Whisper.cpp and voice-mode will use them without any configuration changes!

### API Routing and Proxies

Since voice-mode uses the OpenAI SDK, you can redirect all API traffic through a custom router using the standard `OPENAI_BASE_URL` environment variable:

```bash
# Route all OpenAI API calls through your proxy
export OPENAI_BASE_URL="https://router.example.com/v1"
export OPENAI_API_KEY="your-key"
```

The OpenAI SDK automatically uses this base URL for all API calls - no voice-mode specific configuration needed!

This enables:
- **Cost optimization** - Route to cheaper providers based on request type
- **Fallback handling** - Automatically switch to backup services
- **Load balancing** - Distribute requests across multiple endpoints
- **Custom logic** - Add authentication, caching, or transformation layers

For provider-specific routing (e.g., different endpoints for STT vs TTS), you can still use:
```bash
export STT_BASE_URL="http://localhost:2022/v1"  # Whisper
export TTS_BASE_URL="http://localhost:8880/v1"  # Kokoro
```

See [OpenAI API Routing Guide](openai-api-routing.md) for proxy implementation examples.

## Troubleshooting

### Common Issues

1. **No microphone access**: Ensure your terminal/application has microphone permissions
2. **Container audio issues**: May need to adjust device paths for your system
3. **LiveKit connection failed**: Verify URL and credentials

### Debug Mode

Enable verbose logging and audio file saving:

```bash
export VOICE_MCP_DEBUG=true
```

Audio files are saved to: `~/voice-mode_recordings/`
