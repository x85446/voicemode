# Whisper.cpp STT Setup

Whisper.cpp is a local speech-to-text engine that provides an OpenAI-compatible API.

## Quick Start

1. Start Whisper service:
   ```bash
   make whisper-start
   ```

2. Configure voice-mcp to use local Whisper:
   ```bash
   export STT_BASE_URL=http://localhost:2022/v1
   ```

3. Or add to `.mcp.json`:
   ```json
   "voice-mcp": {
     "env": {
       "STT_BASE_URL": "http://localhost:2022/v1"
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
export STT_BASE_URL=http://localhost:2022/v1
export TTS_BASE_URL=http://localhost:8880/v1
export TTS_VOICE=af_sky
```