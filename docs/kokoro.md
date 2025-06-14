# Kokoro TTS Setup

Kokoro is a local text-to-speech engine that provides an OpenAI-compatible API.

## Quick Start

1. Start Kokoro service:
   ```bash
   make kokoro-start
   ```

2. Configure voice-mcp to use Kokoro:
   ```bash
   export TTS_BASE_URL=http://localhost:8880/v1
   export TTS_VOICE=af_nova  # or af_sky, am_adam, etc.
   ```

3. Or add to `.mcp.json`:
   ```json
   "voice-mcp": {
     "env": {
       "TTS_BASE_URL": "http://localhost:8880/v1",
       "TTS_VOICE": "af_nova"
     }
   }
   ```

## Available Voices

- `af_nova` - Female, similar to OpenAI's nova
- `af_sky` - Female, previously removed from OpenAI
- `af_bella` - Female
- `am_adam` - Male
- `am_echo` - Male

## Performance

Kokoro runs locally on your machine, so performance depends on your hardware. Typical generation times are 1-3 seconds for short phrases.