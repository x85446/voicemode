# Instructions for Claude

## Primary Directive

ALWAYS read the following files at the start of any session:
- README.md to understand the project
- GLOSSARY.md to understand key terms and concepts used in the project
- docs/tasks/README.md for an overview of work
- .conventions/CONVENTIONS.md to understand the engineering conventions for this project
- .ai_docs/README.md to understand where to read and write information about external tools, libraries, protocols, etc
- .repos.txt # List of 3rd party repos we may use
- docs/tasks/README.md # Current task list and recently completed work (take note of "The One Thing" - this is the most important task currently)
- docs/tasks/implementation-notes.md # Important implementation decisions and fixes
- docs/tasks/key-insights.md # Key learnings and design principles
- INSIGHTS.md # Index of important insights and design decisions from development

## Context-Aware Loading

Load specific convention modules based on the current work context:

- **Editing bash scripts**: Load `.conventions/core/principles.md` + `.conventions/languages/bash.md` + `.conventions/interfaces/cli.md`
- **Python development**: Load `.conventions/core/principles.md` + `.conventions/languages/python.md` + `.conventions/interfaces/cli.md`
- **Writing documentation**: Load `.conventions/core/principles.md` + `.conventions/core/documentation.md` + `.conventions/languages/markdown.md`
- **General project work**: Load `CONVENTIONS.md` + `.conventions/core/project-structure.md`

## Override System

Check for convention overrides in this order:
1. `.conventions/` - Base conventions
2. `.conventions-project/` - Project-specific overrides (if exists)
3. `.conventions-local/` - Local personal overrides (if exists)

Later files override earlier ones for the same convention.


## Voice Parameter Selection Guidelines

When using the voice tool (`converse`), DO NOT specify voice, model, or provider parameters unless:
- The user explicitly requests a specific voice/model/provider (e.g., "use nova voice", "speak with Kokoro")
- You need specific features (e.g., emotional TTS requires gpt-4o-mini-tts model)
- You're testing failover by trying a different provider after a failure
- You're debugging a specific configuration issue

**Why**: The system automatically selects the best available endpoint, voice, and model based on:
- Health status of endpoints (failing services are automatically skipped)
- Configured preferences (TTS_VOICES, TTS_MODELS, TTS_BASE_URLS)
- Feature requirements (e.g., emotional speech)

**Examples**:
```python
# ✅ Good - Let system auto-select
converse("How can I help you today?")

# ❌ Bad - Unnecessarily specifying parameters
converse("How can I help you today?", voice="af_sky", tts_provider="kokoro")

# ✅ Good - User requested specific voice
# User: "Can you speak with the nova voice?"
converse("Sure, I'm now using the nova voice", voice="nova")

# ✅ Good - Need emotional features
converse("I'm so excited!", tts_model="gpt-4o-mini-tts", tts_instructions="Sound very excited")
```

You can get the attention of the USER when he is not responding by using the converse tool

On startup, break the ice by asking a questions with your tools

## Task Management

When working on voice-mode features:
1. Check `docs/tasks/` directory for current work and plans
2. Key files in docs/tasks/:
   - `README.md` - Task list and completed features
   - `provider-registry-design.md` - Full provider registry architecture
   - `provider-registry-mvp.md` - MVP implementation plan
   - `emotional-tts-plan.md` - Emotional TTS feature design
   - `implementation-notes.md` - Completed work and decisions
   - `key-insights.md` - Important learnings

## Voice Stack Overview

The voice-mode project now has a complete local voice processing stack:

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

## Important Notes

- These conventions are personal preferences, not rigid rules
- Adapt suggestions to fit the specific project context
- When in doubt, ask for clarification rather than assume

# important-instruction-reminders
Do what has been asked; nothing more, nothing less.
NEVER create files unless they're absolutely necessary for achieving your goal.
ALWAYS prefer editing an existing file to creating a new one.
NEVER proactively create documentation files (*.md) or README files. Only create documentation files if explicitly requested by the User.

## OpenAI API Usage
- Use OpenAI API whenever possible as self hosted alternatives support it and we can use them by setting OPENAI_BASE_URL

## Kokoro TTS Management Prompts

### kokoro-start
When the user asks to "start kokoro", "enable kokoro", "turn on kokoro", "use local TTS", or similar:
- Use the `mcp__voice-mode__kokoro_start` tool
- The tool will start the Kokoro TTS service on port 8880
- Optional: specify a custom models directory path (defaults to ~/Models/kokoro)
- After starting, inform the user that Kokoro is now running and ready for local TTS

### kokoro-stop  
When the user asks to "stop kokoro", "disable kokoro", "turn off kokoro", or similar:
- Use the `mcp__voice-mode__kokoro_stop` tool
- The tool will gracefully terminate the Kokoro TTS service
- Inform the user that Kokoro has been stopped

### kokoro-status
When the user asks "is kokoro running?", "kokoro status", "check kokoro", or similar:
- Use the `mcp__voice-mode__kokoro_status` tool
- The tool will check if Kokoro is running and provide process details
- Report the status to the user including CPU/memory usage if available

## Git Workflow Reminders
- Review and update CHANGELOG before each git commit
