# Implementation Notes and Decisions

## Completed Features

### 1. Unified Voice Service Status Tool
- Created comprehensive `voice_status()` tool that checks all services in parallel
- Shows STT, TTS, LiveKit, and audio device status
- Includes smart recommendations based on availability
- Fixed health check endpoints:
  - Whisper.cpp uses `/health` (not `/v1/health`)
  - Kokoro also uses `/health` (not `/v1/health`)

### 2. Auto-start Functionality
- Added `VOICE_MODE_AUTO_START_KOKORO` environment variable
- Automatically starts Kokoro on first tool use if not running
- Checks if service is already running externally to avoid conflicts
- Integrated into `startup_initialization()` function

### 3. Emotional TTS Support
- Added `VOICE_ALLOW_EMOTIONS` environment variable for cost control
- Implemented validation to prevent unexpected API charges
- Enhanced documentation with emotion examples
- Added emotion status display in voice_status
- Fixed bug: Always create OpenAI TTS client (don't rely on URL comparison)

## Key Architecture Decisions

### Provider Registry Design
- Start simple with just Kokoro, OpenAI, and Whisper
- Each provider has metadata: cost, latency, privacy, features, quality
- Model-aware: providers can have multiple models with different tradeoffs
- Same model can perform differently across providers (e.g., Whisper on Groq vs local)

### Configuration Philosophy
- Maintain backward compatibility with existing env vars
- Add new unified configuration options gradually
- Provider selection based on requirements and user preferences
- Automatic fallback chains for reliability

### Audio Recording Feature
- Saves to `~/voice-mode_audio/` when `VOICE_MODE_SAVE_AUDIO=true`
- Future: Add transcription saving to `~/voice-mode/transcriptions/`
- Keep audio and text in separate directories for organization

## Bugs Fixed
1. OpenAI TTS client initialization when TTS_BASE_URL != OpenAI
2. Health check endpoints for local services (remove /v1 prefix)

## Future Work (See individual plan files)
- Provider registry implementation (provider-registry-mvp.md)
- Transcription saving feature
- Cost tracking and reporting
- Provider capability matrix display