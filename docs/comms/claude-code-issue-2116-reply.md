# Reply to Claude Code Issue #2116 - Voice Mode

**From:** @getvoicemode  
**To:** https://github.com/anthropics/claude-code/issues/2116  
**Subject:** Voice Mode feature request

---

Hey @nullbio! 👋

Great timing on this issue! I'm the developer of [Voice Mode](https://github.com/mbailey/voicemode), an MCP server that already provides exactly what you're looking for - natural voice conversations with Claude Code.

## What Voice Mode offers today:

✅ **Voice conversations** - Speak to Claude and hear responses back  
✅ **Configurable STT/TTS** - Works with OpenAI, local Whisper.cpp, and other OpenAI-compatible services  
✅ **Smart silence detection** - Automatically stops recording when you pause (no manual stop needed!)  
✅ **Multiple transports** - Local microphone or LiveKit for room-based communication  
✅ **Emotional TTS** - Using OpenAI's gpt-4o-mini-tts model for expressive speech (as @nullbio suggested!)

## Quick setup:

```bash
# Install with Claude Code
claude mcp add voice-mode --env OPENAI_API_KEY=your-key -- uvx voice-mode

# Start talking
claude converse
```

Then just tell Claude: "Let's have a voice conversation" and you're talking! 🎤

## Recent improvements:

We just added `min_listen_duration` parameter to prevent premature cutoffs - perfect for when you need thinking time before speaking. The system adapts to your speaking patterns.

## Local/private options:

As @gwpl suggested, we support fully local processing:
- **Whisper.cpp** for local STT (no cloud needed)
- **Kokoro** for local TTS with multiple voices
- All with the same OpenAI-compatible API

Check out our [demo video](https://www.youtube.com/watch?v=cYdwOD_-dQc) to see it in action! (Fun fact: it's unscripted and Claude helped edit it using whisper.cpp transcripts + ffmpeg!)

Would love your feedback on what features would make this even better for reducing typing fatigue. The emotional tone detection is already partially there with our TTS instructions feature - what other aspects would help?