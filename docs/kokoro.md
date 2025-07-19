# Kokoro TTS Setup

Kokoro is a local text-to-speech engine that provides an OpenAI-compatible API. Voice Mode can use it as an alternative to OpenAI's text-to-speech service.

## How Voice Mode Uses Kokoro

Voice Mode automatically checks for local TTS services before falling back to OpenAI:

1. **First**: Checks for Kokoro on `http://127.0.0.1:8880/v1`
2. **Fallback**: Uses OpenAI API (requires `OPENAI_API_KEY`)

## Setting Up Kokoro

1. Install and run Kokoro following the [official instructions](https://huggingface.co/hexgrad/Kokoro-82M)
2. Ensure it's running on port 8880 with the OpenAI-compatible API
3. Voice Mode will automatically detect and use it

No configuration needed - Voice Mode will use local Kokoro when available!

## Manual Configuration (Optional)

To use a different Kokoro endpoint or force its use:

```bash
export TTS_BASE_URL=http://127.0.0.1:8880/v1
export TTS_VOICE=af_sky  # Optional: specify voice
```

Or add to your MCP configuration:
```json
"voice-mode": {
  "env": {
    "TTS_BASE_URL": "http://127.0.0.1:8880/v1",
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
