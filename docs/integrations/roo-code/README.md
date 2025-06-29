# Voice Mode Integration: Roo Code

> 🔗 **Official Website**: [RooCode.com](https://roocode.com/)  
> 📦 **Install**: Search "Roo Code" in VS Code Extensions  
> 🏷️ **Version Requirements**: VS Code 1.80+, Roo Code extension

## Overview

Roo Code (formerly Roo Cline) is an AI-powered VS Code extension that gives you a whole dev team of AI agents in your editor. Voice Mode enhances Roo Code by adding natural voice conversation capabilities through MCP.

## Prerequisites

- [ ] VS Code installed
- [ ] Python 3.10 or higher
- [ ] [uv](https://github.com/astral-sh/uv) package manager (`curl -LsSf https://astral.sh/uv/install.sh | sh`)
- [ ] OpenAI API key (or compatible service)
- [ ] System audio dependencies installed ([see main README](../../../README.md#system-dependencies))

## Quick Start

```bash
# Set your OpenAI API key
export OPENAI_API_KEY="your-openai-key"

# Roo Code will use uvx to run Voice Mode on-demand
# No separate installation needed!
```

## Installation Steps

### 1. Install Roo Code

1. Open VS Code
2. Go to Extensions (Ctrl/Cmd + Shift + X)
3. Search for "Roo Code"
4. Click Install
5. Reload VS Code when prompted

### 2. Configure Roo Code for Voice Mode

Roo Code supports MCP servers. Add Voice Mode to your configuration:

1. Open Roo Code settings in VS Code
2. Navigate to MCP Servers configuration
3. Add Voice Mode configuration

Or manually edit your VS Code settings:

**Add Voice Mode to MCP servers:**

```json
{
  "rooCode.mcpServers": {
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

**Note:** Using `uvx` means Voice Mode will be downloaded and run on-demand. No separate installation required!

### 3. Restart VS Code

After saving the configuration, restart VS Code for changes to take effect.

## Verification

1. **Check MCP Server Status:**
   - Open Roo Code panel (rocket icon in sidebar)
   - Look for MCP servers section
   - "voice-mode" should be listed as active

2. **Test Voice Mode:**
   - In Roo Code chat, type: "Let's have a voice conversation"
   - You should hear Roo speak and listen for your response
   - Try saying: "Hello, can you help me with this code?"

## Usage Examples

### Voice-Enabled Code Review
```
"Review this function and tell me what could be improved"
"Can you explain what this code does?"
"Help me refactor this to be more efficient"
```

### Voice Debugging Sessions
```
"This test is failing, can you help me debug it?"
"What might be causing this error?"
"Walk me through fixing this bug"
```

### Architecture Discussions
```
"Should I use a factory pattern here?"
"What's the best way to structure this module?"
"Let's discuss the architecture of this feature"
```

## Environment Variables

You can configure Voice Mode behavior with these environment variables:

**Option 1: Set in Roo Code config (shown above)**

**Option 2: Inherit from system**
```json
{
  "rooCode.mcpServers": {
    "voice-mode": {
      "command": "uvx",
      "args": ["voice-mode"]
      // No env section - inherits from system
    }
  }
}
```

### Advanced Configuration

```bash
# Use multiple TTS providers with fallback
export VOICEMODE_TTS_BASE_URLS="http://127.0.0.1:8880/v1,https://api.openai.com/v1"

# Prefer specific voices
export VOICEMODE_TTS_VOICES="af_sky,nova,alloy"

# Enable debug logging
export VOICEMODE_DEBUG="true"
```

## Troubleshooting

### Voice Mode Not Available
- Ensure Roo Code extension is fully installed and activated
- Check VS Code Developer Tools (Help → Toggle Developer Tools) for errors
- Verify `uvx` is installed: `which uvx`

### No Audio
- Grant VS Code microphone permissions in system settings
- Check system audio input/output devices
- Try running with debug: Add `"VOICEMODE_DEBUG": "true"` to env

### MCP Connection Failed
- Ensure Python 3.10+ is installed
- Try running `uvx voice-mode --help` in terminal
- Check Roo Code logs in VS Code Output panel

## Platform-Specific Notes

### macOS
- Grant microphone permissions: System Settings → Privacy & Security → Microphone → Code
- May need to restart VS Code after granting permissions

### Windows
- Best experience with WSL2
- Native Windows may require additional audio configuration

### Linux
- Ensure PulseAudio or PipeWire is running
- May need: `sudo usermod -a -G audio $USER`

## Advanced Configuration

### Using Local STT/TTS Services

For complete privacy, use local services:

```json
{
  "rooCode.mcpServers": {
    "voice-mode": {
      "command": "uvx",
      "args": ["voice-mode"],
      "env": {
        "VOICEMODE_TTS_BASE_URLS": "http://127.0.0.1:8880/v1,https://api.openai.com/v1",
        "VOICEMODE_STT_BASE_URLS": "http://127.0.0.1:2022/v1,https://api.openai.com/v1"
      }
    }
  }
}
```

### Using Different AI Models

Roo Code supports multiple AI models. Configure your preferred model in Roo Code settings, and Voice Mode will work with any model you choose.

## See Also

- 📚 [Voice Mode Documentation](../../../README.md)
- 🔧 [Configuration Reference](../../configuration.md)
- 🎤 [Local STT/TTS Setup](../../kokoro.md)
- 💬 [Roo Code GitHub](https://github.com/RooCodeInc/Roo-Code)
- 🐛 [Troubleshooting Guide](../../troubleshooting/README.md)
- 🚀 [Roo Code Documentation](https://roocode.com/docs)

---

**Need Help?** Join our [Discord community](https://discord.gg/Hm7dF3uCfG) or check [Roo Code issues](https://github.com/RooCodeInc/Roo-Code/issues)