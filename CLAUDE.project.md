# Claude Integration

## Primary Directive

ALWAYS read the following files CONVENTIONS.md at the start of any session:
- CONVENTIONS.md to understand the engineering conventions for this project.
- ai_docs/README.md to understand where to read and write information about external tools, libraries, protocols, etc

## Context-Aware Loading

Load specific convention modules based on the current work context:

- **Editing bash scripts**: Load `core/principles.md` + `languages/bash.md` + `interfaces/cli.md`
- **Python development**: Load `core/principles.md` + `languages/python.md` + `interfaces/cli.md`
- **Writing documentation**: Load `core/principles.md` + `core/documentation.md` + `languages/markdown.md`
- **General project work**: Load `CONVENTIONS.md` + `core/project-structure.md`

## Override System

Check for convention overrides in this order:
1. `conventions/` - Base conventions
2. `conventions-project/` - Project-specific overrides (if exists)
3. `conventions-local/` - Local personal overrides (if exists)

Later files override earlier ones for the same convention.

## Important Notes

- These conventions are personal preferences, not rigid rules
- Adapt suggestions to fit the specific project context
- When in doubt, ask for clarification rather than assume# Instructions for Claude

Read the following files:

- README.md
- ai_docs/README.md
- CONVENTIONS.md
- .repos.txt # List of 3rd party repos we may use

On startup, break the ice by asking a questions with your tools

## Voice Duration Guidelines

When using voice tools, ALWAYS set appropriate duration parameters based on expected response length:

### For `ask_voice_question`:
- Simple yes/no questions: use `duration=10` 
- Normal conversational responses: use `duration=20` (better than default 15)
- Open-ended questions: use `duration=30`
- Questions expecting detailed explanations: use `duration=45`
- Questions about stories or long explanations: use `duration=60`

### For `listen_for_speech`:
- Single words/commands: use `duration=5`
- Normal sentences: use `duration=10`
- Multiple sentences: use `duration=20`
- Long dictation: use `duration=30-60`

**IMPORTANT**: Always err on the side of longer duration. It's better to have silence at the end than to cut off the user mid-sentence.

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
