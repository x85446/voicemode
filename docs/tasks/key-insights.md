# Key Insights and Learnings

## Technical Insights

### Silence Detection Implementation
- WebRTC VAD requires specific chunk sizes (10, 20, or 30ms)
- Sample rate conversion may be needed (24kHz -> 16kHz for VAD)
- Chunked recording allows real-time processing without buffering entire audio
- VAD aggressiveness affects both false positives and false negatives
- Minimum recording duration prevents cutting off very short utterances
- Fallback to fixed duration ensures reliability when VAD fails
- LLMs can disable VAD per-interaction using disable_vad parameter
- Speech must be detected before silence can trigger stop (prevents early cutoff)

### MCP Server Architecture
- MCP servers are stateless - configuration via env vars only
- Server needs restart to pick up code changes
- Tools can call `startup_initialization()` for one-time setup

### Provider Management
- Local services (Kokoro, Whisper) can be MCP-managed or external
- Need to distinguish between "configured" vs "running" vs "available"
- Health endpoints vary between services (OpenAI uses /models, locals use /health)

### Error Handling
- Network issues (like in Warrandyte) only affect cloud services
- Local fallbacks are crucial for reliability
- Provider failover should be automatic and transparent

## Design Principles

### Cost Consciousness
- Emotional TTS costs money - needs explicit opt-in
- Show costs transparently in status displays
- Default to free/local options when possible

### User Control
- Let LLMs make emotion decisions (don't analyze in voice-mode)
- Provide clear documentation for LLM guidance
- Users should understand what's happening and why

### Progressive Enhancement
- Start with basic features, add complexity gradually
- MVP first, then iterate
- Keep backward compatibility

## Conversation Context
- Audio files now saved with timestamps
- Both TTS (synthesized) and STT (recorded) audio preserved
- Future: Link audio with transcriptions for full conversation history

## Environment Variables Summary
```bash
# Core
OPENAI_API_KEY=required
STT_BASE_URL=http://localhost:2022/v1
TTS_BASE_URL=http://localhost:8880/v1

# Features
VOICE_MODE_AUTO_START_KOKORO=true
VOICEMODE_ENABLE_SILENCE_DETECTION=true   # Default on for better UX
VOICEMODE_VAD_AGGRESSIVENESS=2          # 0-3, higher = more aggressive
VOICEMODE_SILENCE_THRESHOLD_MS=1000     # Stop after 1 second of silence
VOICEMODE_MIN_RECORDING_DURATION=0.5    # Min recording time in seconds
VOICE_ALLOW_EMOTIONS=true
VOICE_MODE_SAVE_AUDIO=true

# Future
VOICE_PROVIDERS=kokoro,openai
VOICE_PREFER_LOCAL=true
```