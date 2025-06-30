# Reply to Claude Code Issue #2189 - Text-to-Speech Output

**From:** @getvoicemode  
**To:** https://github.com/anthropics/claude-code/issues/2189  
**Subject:** Text-to-speech output feature request

---

Hey @rbinnun! 👋

Your TTS feature request is exactly what [Voice Mode](https://github.com/mbailey/voicemode) provides today - and much more!

## Voice Mode delivers:
- **Full TTS for Claude's responses** - Every response can be spoken aloud
- **Beyond system TTS** - High-quality voices from OpenAI or local Kokoro
- **Two-way conversations** - Not just TTS output, but full voice interactions

## Simple setup:

```bash
# Add to Claude Code
claude mcp add voice-mode --env OPENAI_API_KEY=your-key -- uvx voice-mode

# Start using TTS
claude converse
```

## Accessibility features you mentioned:
✅ Automatic reading of responses  
✅ On-demand triggering  
✅ Works while multitasking  
✅ No manual copying needed  

## Bonus capabilities:
- **Emotional speech** - Claude can speak with different tones
- **Multiple voices** - Choose from various voice options
- **Local option** - Use Kokoro TTS for fully offline operation
- **Cross-platform** - Works on Linux, macOS, and Windows (WSL)

Instead of piping to external tools, Voice Mode integrates directly with Claude Code through MCP, making it seamless and interactive.

Would this solve your accessibility and multitasking needs? Happy to help you get started!