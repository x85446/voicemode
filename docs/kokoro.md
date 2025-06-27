# Kokoro TTS Setup

Kokoro is a local text-to-speech engine that provides an OpenAI-compatible API.

## Quick Start

2. Configure voice-mode to use Kokoro:
   ```bash
   export VOICEMODE_TTS_BASE_URLS=http://127.0.0.1:8880/v1
   export VOICEMODE_TTS_VOICES=af_sky  # Default for Kokoro (or af_nova, am_adam, etc.)
   ```

3. Or add to `.mcp.json`:
   ```json
   "voice-mode": {
     "env": {
       "VOICEMODE_TTS_BASE_URLS": "http://127.0.0.1:8880/v1",
       "TTS_VOICE": "af_sky"
     }
   }
   ```

## Available Voices

- `af_sky` - Female, natural voice (default for Kokoro)
- `af_nova` - Female, similar to OpenAI's nova
- `af_sky` - Female, previously removed from OpenAI
- `af_bella` - Female
- `am_adam` - Male
- `am_echo` - Male

## Performance

Kokoro runs locally on your machine, so performance depends on your hardware. Typical generation times are 1-3 seconds for short phrases.
