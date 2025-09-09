# Getting Started with VoiceMode

VoiceMode brings voice conversations to AI coding assistants. It works as both an MCP server for Claude Code and as a standalone CLI tool.

## What is VoiceMode?

VoiceMode provides:
- **MCP Server**: Adds voice tools to Claude Code - no installation needed
- **CLI Tool**: Use VoiceMode's tools directly from your terminal
- **Local Services**: Optional privacy-focused speech processing

## Quick Start: Using with Claude Code

The fastest way to get started is using VoiceMode with Claude Code.

### Option 1: Universal Installer (Recommended)

The easiest way - installs UV and all dependencies automatically:

```bash
# macOS (no sudo needed)
curl -sSf https://voicemode.sh | sh

# Linux (may need sudo for system packages)
curl -sSf https://voicemode.sh | sh
```

This installer will:
- Install UV package manager
- Install system dependencies (Node.js, FFmpeg, PortAudio, etc.)
- Set up your environment for VoiceMode

### Option 2: Manual UV Installation

If you prefer to install UV manually:

```bash
# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Or with pip (if available)
pip install uv
```

**Note**: You'll also need these system dependencies:
- **macOS**: Node.js, PortAudio, FFmpeg (`brew install node portaudio ffmpeg`)
- **Linux**: Node.js, PortAudio, FFmpeg, ALSA libraries

Learn more: [UV Installation Guide](https://docs.astral.sh/uv/getting-started/installation/)

### 1. Add VoiceMode to Claude

```bash
claude mcp add --user voicemode --refresh
```

### 2. Configure Your API Key

Edit your Claude MCP configuration to add your OpenAI API key:

```bash
# Open your MCP configuration
claude mcp edit --user

# Add your API key to the voice-mode server:
{
  "mcpServers": {
    "voice-mode": {
      "command": "uvx",
      "args": ["voice-mode"],
      "env": {
        "OPENAI_API_KEY": "sk-your-api-key-here"
      }
    }
  }
}
```

### 3. Verify Installation

```bash
# Check that VoiceMode is connected
claude mcp list
```

You should see `voice-mode` in the list of connected servers.

### 4. Start Using Voice

In Claude Code, simply type:
```
/voice
```

Speak when you hear the chime, and Claude will respond with voice!

## Alternative: Using as a CLI Tool

If you want to use VoiceMode from the command line:

### Installation

```bash
# Install with pip
pip install voice-mode

# Or install from source
git clone https://github.com/mbailey/voicemode
cd voicemode
pip install -e .
```

### Basic Usage

```bash
# Set your API key
export OPENAI_API_KEY="sk-your-api-key-here"

# Start a voice conversation
voice-mode converse

# Transcribe audio
echo "Hello world" | voice-mode transcribe
```

## Setting Up Local Services (Optional)

For complete privacy, you can run voice services locally instead of using OpenAI.

### Quick Setup

```bash
# Install local services
voice-mode whisper install   # Speech-to-text
voice-mode kokoro install    # Text-to-speech

# Start services
voice-mode whisper start
voice-mode kokoro start
```

VoiceMode will automatically detect and use these local services when available.

Learn more: [Whisper Setup Guide](../guides/whisper-setup.md) | [Kokoro Setup Guide](../guides/kokoro-setup.md)

## Configuration

VoiceMode works out of the box with sensible defaults. To customize:

### Select Your Voice

```bash
# OpenAI voices
export VOICEMODE_VOICES="nova,shimmer"

# Or Kokoro voices (if using local TTS)
export VOICEMODE_VOICES="af_sky,am_adam"
```

Available OpenAI voices: alloy, echo, fable, onyx, nova, shimmer

### Project-Specific Settings

Create `.voicemode.env` in your project:

```bash
# Example for a game project
export VOICEMODE_VOICES="onyx"
export VOICEMODE_TTS_SPEED=1.2
```

Learn more: [Configuration Guide](../guides/configuration.md)

## Troubleshooting

### Voice Not Working in Claude?

1. **Check MCP connection**:
   ```bash
   claude mcp list
   ```
   
2. **Verify API key** is set in your MCP configuration

3. **Test with debug mode**:
   Add to your MCP config:
   ```json
   "env": {
     "OPENAI_API_KEY": "sk-...",
     "VOICEMODE_DEBUG": "true"
   }
   ```

### No Audio Input?

```bash
# List audio devices
voice-mode audio devices

# Test recording
voice-mode audio test
```

### Service Issues?

```bash
# Check service status
voice-mode whisper status
voice-mode kokoro status

# View logs
voice-mode logs --tail 50
```

## Next Steps

- **[Configuration Guide](../guides/configuration.md)** - Customize VoiceMode
- **[Development Setup](development-setup.md)** - Contribute to VoiceMode
- **[Service Guides](../guides/)** - Set up Whisper, Kokoro, or LiveKit
- **[CLI Reference](../reference/cli.md)** - All available commands

## Getting Help

- **GitHub Issues**: [github.com/mbailey/voicemode/issues](https://github.com/mbailey/voicemode/issues)
- **Discord**: Join our community for support

Welcome to voice-enabled AI coding! 🎙️