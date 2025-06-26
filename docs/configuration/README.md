# Voice Mode Configuration

This directory contains configuration documentation for Voice Mode.

## Quick Links

- **[Environment Variables](environment.md)** - Complete reference of all environment variables
- **[MCP Configuration](../configuration.md)** - Detailed guide for configuring Voice Mode with MCP hosts
- **[Integration Guides](../integrations/README.md)** - Platform-specific setup instructions

## Getting Started

### Minimal Configuration

For OpenAI services, you'll need an API key:

```bash
export OPENAI_API_KEY="your-api-key"
```

For local-only setups (Kokoro + Whisper), no API key is required!

### Common Configurations

**Enable all data saving:**
```bash
export VOICEMODE_SAVE_ALL=true
```

**Debug mode (auto-saves everything):**
```bash
export VOICEMODE_DEBUG=true
```

**Use only local services:**
```bash
export VOICEMODE_TTS_BASE_URLS="http://localhost:8880/v1"
export VOICEMODE_STT_BASE_URLS="http://localhost:2022/v1"
```

## Directory Structure

Voice Mode stores all data under `~/.voicemode/` by default:

```
~/.voicemode/
├── audio/          # Saved audio recordings
├── transcriptions/ # Saved transcriptions
├── logs/           # Event and debug logs
└── config/         # Configuration files
```

## Privacy

By default, Voice Mode prioritizes privacy:
- Audio recordings are NOT saved unless explicitly enabled
- Transcriptions are NOT saved unless explicitly enabled
- Only event logs are saved by default for debugging

To change this behavior, see the [Environment Variables](environment.md) reference.