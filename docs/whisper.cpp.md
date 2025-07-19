# Whisper.cpp STT Setup

Whisper.cpp is a local speech-to-text engine that provides an OpenAI-compatible API. Voice Mode can use it as an alternative to OpenAI's speech-to-text service.

## How Voice Mode Uses Whisper

Voice Mode automatically checks for local STT services before falling back to OpenAI:

1. **First**: Checks for Whisper.cpp on `http://127.0.0.1:2022/v1`
2. **Fallback**: Uses OpenAI API (requires `OPENAI_API_KEY`)

## Setting Up Whisper.cpp

### Installation

Install Whisper.cpp following the [official instructions](https://github.com/ggerganov/whisper.cpp).

### Running the OpenAI-Compatible Server

To run Whisper.cpp with an OpenAI-compatible API endpoint:

```bash
whisper-server \
  --model base.en \
  --host 127.0.0.1 \
  --port 2022 \
  --inference-path "/v1/audio/transcriptions" \
  --threads 4 \
  --processors 1 \
  --convert \
  --print-progress
```

Key options:
- `--model`: Model to use (tiny, base, small, medium, large)
- `--host`: Server host (default: 127.0.0.1)
- `--port`: Server port (Voice Mode expects 2022)
- `--inference-path`: OpenAI-compatible endpoint path
- `--threads`: Number of threads for processing
- `--processors`: Number of parallel processors
- `--convert`: Convert audio to required format automatically
- `--print-progress`: Show transcription progress

Voice Mode will automatically detect and use it when running on port 2022!

## Manual Configuration (Optional)

To use a different Whisper endpoint or force its use:

```bash
export STT_BASE_URL=http://127.0.0.1:2022/v1
```

Or add to your MCP configuration:
```json
"voice-mode": {
  "env": {
    "STT_BASE_URL": "http://127.0.0.1:2022/v1"
  }
}
```

## Model Selection

The Whisper model is automatically selected based on your hardware:
- **Mac (Apple Silicon)**: Uses optimized CoreML models
- **NVIDIA GPU**: Uses CUDA-accelerated models
- **CPU**: Uses optimized CPU models

## Performance

Local Whisper typically processes speech in 1-3 seconds depending on:
- Hardware (GPU/CPU)
- Model size
- Audio length

## Fully Local Setup

For completely offline voice processing, combine Whisper with Kokoro:

```bash
export STT_BASE_URL=http://127.0.0.1:2022/v1
export TTS_BASE_URL=http://127.0.0.1:8880/v1
export TTS_VOICE=af_sky
```