# Getting Started with VoiceMode

Welcome to VoiceMode! This tutorial will help you get up and running with voice conversations in your AI coding assistant.

## Prerequisites

- Python 3.10 or higher
- macOS or Linux (Windows support coming soon)
- Microphone access
- Either an OpenAI API key OR local voice services

## Installation

### Install VoiceMode

The easiest way to install VoiceMode is using uvx (recommended) or pip:

```bash
# Using uvx (recommended)
uvx voice-mode

# Or install globally with pip
pip install voice-mode

# Or install from source
git clone https://github.com/your-username/voice-mode
cd voice-mode
pip install -e .
```

### Configure Your MCP Client

Add VoiceMode to your MCP client configuration (e.g., Claude Desktop):

```json
{
  "mcpServers": {
    "voice-mode": {
      "command": "uvx",
      "args": ["voice-mode"],
      "env": {
        "OPENAI_API_KEY": "your-key-here"
      }
    }
  }
}
```

## Choose Your Setup

### Option 1: Cloud Setup (Easiest)

Use OpenAI's cloud services for both speech-to-text and text-to-speech:

```bash
# Add to your environment or MCP config
export OPENAI_API_KEY="sk-your-key-here"
```

That's it! VoiceMode will use OpenAI's services automatically.

### Option 2: Local Setup (Private)

Run everything locally for complete privacy:

```bash
# Install local services
voice-mode whisper install   # Speech-to-text
voice-mode kokoro install    # Text-to-speech

# Start services
voice-mode whisper start
voice-mode kokoro start
```

### Option 3: Hybrid Setup (Recommended)

Use local services with cloud fallback:

```bash
# Set OpenAI key for fallback
export OPENAI_API_KEY="sk-your-key-here"

# Install and start local services
voice-mode whisper install
voice-mode kokoro install
voice-mode whisper start
voice-mode kokoro start
```

## Your First Voice Conversation

### Using Claude Desktop

1. Open Claude Desktop
2. Start a new conversation
3. Use the voice command:
   ```
   /voice
   ```
4. Start speaking when you hear the chime
5. Claude will respond with voice

### Using the CLI

```bash
# Start an interactive voice session
voice-mode converse

# Or use in a script
echo "Hello, can you hear me?" | voice-mode transcribe
```

## Basic Configuration

VoiceMode creates a configuration file at `~/.voicemode/voicemode.env` on first run. You can customize:

```bash
# Select your preferred voice
export VOICEMODE_VOICES="nova,alloy"  # OpenAI voices
# or
export VOICEMODE_VOICES="af_sky"       # Kokoro voice

# Enable debug mode for troubleshooting
export VOICEMODE_DEBUG=true

# Save all audio files
export VOICEMODE_SAVE_ALL=true
```

## Installing Voice Services

### Whisper (Speech-to-Text)

```bash
# Quick install with default model
voice-mode whisper install

# Install with specific model
voice-mode whisper install --model base.en

# List available models
voice-mode whisper models

# Check status
voice-mode whisper status
```

Available models:
- `tiny` - Fastest, lowest quality (39 MB)
- `base` - Good balance (142 MB)
- `small` - Better quality (466 MB)
- `medium` - High quality (1.5 GB)
- `large-v2` - Best quality (2.9 GB, default)

### Kokoro (Text-to-Speech)

```bash
# Install Kokoro
voice-mode kokoro install

# Start the service
voice-mode kokoro start

# Check available voices
voice-mode kokoro voices
```

Popular voices:
- `af_sky` - Natural female voice (default)
- `am_adam` - Natural male voice
- `bf_emma` - British female
- `bm_george` - British male

### LiveKit (Room-Based Voice)

For multi-participant voice rooms:

```bash
# Install LiveKit server
voice-mode livekit install

# Start server and frontend
voice-mode livekit start
voice-mode frontend start

# Open web interface
voice-mode frontend open
```

Access at http://localhost:3000 (password: `voicemode123`)

## Shell Completion

Enable tab completion for VoiceMode commands:

### Bash
```bash
# Add to ~/.bashrc
eval "$(_VOICE_MODE_COMPLETE=bash_source voice-mode)"
```

### Zsh
```bash
# Add to ~/.zshrc
eval "$(_VOICE_MODE_COMPLETE=zsh_source voice-mode)"
```

### Fish
```bash
# Add to ~/.config/fish/config.fish
_VOICE_MODE_COMPLETE=fish_source voice-mode | source
```

## Project-Specific Configuration

Create a `.voicemode.env` file in your project directory:

```bash
# Project-specific voices for a game project
export VOICEMODE_VOICES="onyx,fable"
export VOICEMODE_TTS_SPEED=0.9

# Project-specific for a meditation app
export VOICEMODE_VOICES="nova"
export VOICEMODE_TTS_SPEED=0.8
export VOICEMODE_SILENCE_THRESHOLD=5.0
```

## Migration from Older Versions

If upgrading from voice-mcp or earlier versions:

### Environment Variables
All `VOICE_MODE_` variables are now `VOICEMODE_`:
- `VOICE_MODE_DEBUG` → `VOICEMODE_DEBUG`
- `VOICE_MODE_SAVE_AUDIO` → `VOICEMODE_SAVE_ALL`

### Directory Changes
- `~/voice-mcp_recordings/` → `~/.voicemode/recordings/`
- `~/voice-mcp_audio/` → `~/.voicemode/audio/`

### Configuration Files
Move from scattered configs to unified location:
```bash
# Old locations
~/.voice-mode/config.json
~/.config/voice-mode/settings.ini

# New location
~/.voicemode/voicemode.env
```

## Troubleshooting

### No Audio Input

1. Check microphone permissions
2. Verify audio device:
   ```bash
   voice-mode audio devices
   ```
3. Test recording:
   ```bash
   voice-mode audio test
   ```

### Service Connection Issues

```bash
# Check if services are running
voice-mode whisper status
voice-mode kokoro status

# View logs
voice-mode whisper logs
voice-mode kokoro logs

# Restart services
voice-mode whisper restart
voice-mode kokoro restart
```

### API Key Issues

```bash
# Verify API key is set
echo $OPENAI_API_KEY

# Test API connection
voice-mode test openai
```

### Debug Mode

Enable debug mode for detailed logging:

```bash
export VOICEMODE_DEBUG=true
voice-mode converse
```

This saves all audio files to `~/.voicemode/debug/` for analysis.

## Next Steps

- **[Development Setup](development-setup.md)** - Set up your development environment
- **[Configuration Guide](../guides/configuration.md)** - Detailed configuration options
- **[Selecting Voices](../guides/selecting-voices.md)** - Choose the perfect voice
- **[Service Setup Guides](../guides/)** - Deep dive into Whisper, Kokoro, and LiveKit

## Getting Help

- **Documentation**: https://docs.voicemode.io
- **GitHub Issues**: https://github.com/your-username/voice-mode/issues
- **Discord Community**: https://discord.gg/voicemode

Welcome to the world of voice-enabled AI coding! 🎙️