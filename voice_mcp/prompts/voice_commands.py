"""Voice command prompts for guided interactions."""

from voice_mcp.server_new import mcp


@mcp.prompt()
async def voice_setup() -> str:
    """Guide for setting up voice services"""
    return """To set up voice services for voice-mcp:

1. **Environment Variables** (required):
   - OPENAI_API_KEY: Your OpenAI API key for TTS/STT services
   
2. **Optional Configuration**:
   - TTS_VOICE: Default voice (e.g., 'nova', 'alloy', 'af_sky')
   - TTS_MODEL: TTS model (e.g., 'tts-1', 'tts-1-hd', 'gpt-4o-mini-tts')
   - STT_MODEL: STT model (default: 'whisper-1')
   - VOICE_MCP_PREFER_LOCAL: Use local services when available (default: true)
   - VOICE_ALLOW_EMOTIONS: Enable emotional TTS (default: false)
   - VOICE_MCP_AUTO_START_KOKORO: Auto-start Kokoro TTS (default: false)

3. **Local Services** (optional):
   - Kokoro TTS: Run `kokoro_start()` for local TTS
   - LiveKit: Set LIVEKIT_URL for room-based voice chat

4. **Quick Test**:
   ```
   # Test basic TTS
   converse("Hello! Can you hear me?", wait_for_response=False)
   
   # Test conversation
   converse("What's your name?")
   ```

Use `voice_status()` to check current configuration and service status.
"""


@mcp.prompt()
async def emotional_speech_guide() -> str:
    """Guide for using emotional speech features"""
    return """To use emotional speech with voice-mcp:

**Requirements**:
1. Set `VOICE_ALLOW_EMOTIONS=true` in your environment
2. Use OpenAI API (emotional speech requires OpenAI's gpt-4o-mini-tts model)

**Usage Examples**:

```python
# Excitement
converse("We did it! This is amazing!", 
         tts_model="gpt-4o-mini-tts",
         tts_instructions="Sound extremely excited and celebratory")

# Sadness
converse("I'm sorry for your loss", 
         tts_model="gpt-4o-mini-tts",
         tts_instructions="Sound gentle and sympathetic")

# Urgency
converse("Watch out! Be careful!", 
         tts_model="gpt-4o-mini-tts",
         tts_instructions="Sound urgent and concerned")

# Humor
converse("That's the funniest thing I've heard all day!", 
         tts_model="gpt-4o-mini-tts",
         tts_instructions="Sound amused and playful")

# Whispering
converse("This is a secret", 
         tts_model="gpt-4o-mini-tts",
         tts_instructions="Whisper very quietly")
```

**Tips**:
- Be specific with emotional instructions
- Combine emotions with speaking style (e.g., "Sound excited but speak slowly")
- Cost: ~$0.02/minute for emotional speech
- Falls back to standard TTS if emotions are disabled
"""