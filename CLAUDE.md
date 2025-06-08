# Instructions for Claude

Read the following files:

- README.md
- ai_docs/README.md
- CONVENTIONS.md
- external/repos.txt # List of 3rd party repos we may use

You can get the attention of the USER when he is not responding by using tools from livekit-voice-mcp:ask_voice_question

On startup, break the ice by asking a questions with your tools

## Voice Stack Overview

The voice-mcp project now has a complete local voice processing stack:

### Services
- **Whisper.cpp STT** (Port 2022): Local speech-to-text with OpenAI-compatible API
- **Kokoro TTS** (Port 8880): Local text-to-speech with OpenAI-compatible API  
- **LiveKit** (Port 7880): Real-time voice orchestration
- **Voice Frontend** (Port 3001): User interface for voice interactions

### Key Commands
- `mt sync` - Download external repositories
- `make install` - Install and build all components
- `make dev` - Start complete voice stack
- `make whisper-start/stop` - Manage Whisper STT
- `make kokoro-start/stop` - Manage Kokoro TTS

### Architecture Notes
- Whisper runs as native binary (no container) for performance
- Kokoro runs in container for dependency isolation
- Both services expose OpenAI-compatible APIs
- Automatic fallback from local to cloud services
- Hardware detection for optimal model selection

# important-instruction-reminders
Do what has been asked; nothing more, nothing less.
NEVER create files unless they're absolutely necessary for achieving your goal.
ALWAYS prefer editing an existing file to creating a new one.
NEVER proactively create documentation files (*.md) or README files. Only create documentation files if explicitly requested by the User.

## OpenAI API Usage
- Use OpenAI API whenever possible as self hosted alternatives support it and we can use them by setting OPENAI_BASE_URL
