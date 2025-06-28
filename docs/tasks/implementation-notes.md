# Implementation Notes and Decisions

## Completed Features

### 0. Silence Detection (2025-06-26) - UPDATED 2025-06-27
- Implemented WebRTC VAD-based silence detection for automatic recording stop
- Added configurable environment variables:
  - `VOICEMODE_ENABLE_SILENCE_DETECTION` (default: true for better UX)
  - `VOICEMODE_VAD_AGGRESSIVENESS` (0-3, default: 2)
  - `VOICEMODE_SILENCE_THRESHOLD_MS` (default: 1000ms - increased from 800ms)
  - `VOICEMODE_MIN_RECORDING_DURATION` (default: 0.5s)
- Created `record_audio_with_silence_detection()` function
- Automatic fallback to fixed duration if VAD unavailable or errors occur
- Added comprehensive test suite and manual testing tools
- Full documentation in docs/silence-detection.md
- **NEW**: Added `disable_vad` parameter to converse() for LLM control
- **NEW**: VAD requires speech detection before silence can trigger stop

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

### 4. Exchange/Conversation Terminology Update (2025-06-29)
- Updated terminology throughout the codebase:
  - "Exchange": A single call-and-response interaction (user utterance + assistant response)
  - "Conversation": A group of related exchanges with < 5 minute gaps
- Updated GLOSSARY.md with clear definitions
- Modified conversation_browser.py to use correct terminology

### 5. JSONL Conversation Logging (2025-06-29)
- Implemented comprehensive JSONL logging system in conversation_logger.py
- Each utterance logged as a separate JSON line with:
  - Conversation ID (format: conv_YYYYMMDD_HHMMSS_suffix)
  - Timestamp, type (STT/TTS), text, and metadata
  - Schema versioning for future compatibility
- Handles conversation continuity across voice-mode restarts
- Correctly handles midnight log file rollover
- Integrated into conversation.py for automatic logging

### 6. Audio File Naming with Conversation IDs (2025-06-29)
- Updated audio file naming format: `timestamp_convID_type.extension`
- Example: `20250629_001718_lhzgg4_tts.mp3`
- Modified get_debug_filename() and save_debug_file() to accept conversation_id
- Updated all TTS and STT code paths to pass conversation ID
- Makes it easy to associate audio files with their conversations

### 7. Conversation Browser Improvements (2025-06-29)
- Fixed Jinja2 template syntax error (can't have elif after else)
- Fixed date sorting to show newest dates first
- Added conversation grouping view
- Browser now reads from both JSONL logs and legacy transcription files
- Supports three view modes: Date, Project, and Conversation

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