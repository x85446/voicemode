# Reply to Gemini CLI Issue #1982 - Audio Input Instead of Typing

**From:** @getvoicemode  
**To:** https://github.com/google-gemini/gemini-cli/issues/1982  
**Subject:** Audio input instead of typing

---

Hey @nshiab! 👋

Great suggestion! I've got some exciting news - [Voice Mode](https://github.com/mbailey/voicemode) already provides exactly what you're looking for with Gemini CLI!

## Voice Mode + Gemini CLI = 🎤✨

Check out our [demo video](https://www.youtube.com/watch?v=HC6BGxjCVnM) showing Voice Mode working seamlessly with Gemini CLI!

## What you get:

✅ **Full voice conversations** - Talk to Gemini, hear responses back  
✅ **Natural speaking** - No push-to-talk, just speak naturally  
✅ **Smart silence detection** - Automatically knows when you're done  
✅ **High-quality STT** - Uses OpenAI Whisper (as @xied-ctrl suggested!) or local alternatives

## Quick setup:

```bash
# Set your OpenAI API key (for STT/TTS)
export OPENAI_API_KEY=your-key

# Configure Voice Mode in your .gemini/settings.json
# See our full Gemini CLI setup guide:
# https://github.com/mbailey/voicemode/blob/main/docs/integrations/gemini-cli/README.md

# Start Gemini CLI
gemini

# Then type 'converse' to start voice mode
```

Then just say: "Let's have a voice conversation" and you're speaking with Gemini! 🎙️

## Why it's better than OS dictation:

As @olufuwatayo mentioned, OS dictation works, but Voice Mode offers:
- **Two-way voice** - Hear Gemini's responses too
- **Context-aware** - Gemini can ask clarifying questions verbally
- **Faster workflow** - No switching between dictation and reading

## Bonus features:
- **Local STT option** - Use Whisper.cpp for privacy
- **Multiple voices** - Choose how Gemini sounds
- **Emotional speech** - Gemini can express excitement, concern, etc.

Speaking really is faster than typing - and with Voice Mode, the entire conversation flows naturally!

Would love to hear your feedback after trying it out!