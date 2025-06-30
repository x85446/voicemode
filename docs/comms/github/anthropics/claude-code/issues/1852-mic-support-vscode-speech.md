# Reply to Claude Code Issue #1852 - Mic Support via VS Code Speech

**From:** @getvoicemode  
**To:** https://github.com/anthropics/claude-code/issues/1852  
**Subject:** Add Mic support via VS Code Speech

---

Hey @spirefyio and @yoniholmes! 👋

Great news - [Voice Mode](https://github.com/mbailey/voicemode) provides the dictation capabilities you're looking for, and it works directly with Claude Code (no VS Code needed)!

## Why Voice Mode is perfect for your needs:

✅ **Native mic support** - Works directly in Claude Code  
✅ **Fast dictation** - Just speak naturally, no manual start/stop  
✅ **RSI-friendly** - Reduce typing strain (great point @yoniholmes!)  
✅ **Smart editing** - Say "Let's have a voice conversation" and iterate verbally

## Quick setup:

```bash
# One-time installation
claude mcp add voice-mode --env OPENAI_API_KEY=your-key -- uvx voice-mode

# Start dictating
claude converse
```

## Key advantages over VS Code Speech:

1. **Integrated experience** - No switching between apps
2. **Two-way voice** - Hear Claude's responses too
3. **Natural pauses** - Silence detection handles when you stop speaking
4. **Cross-platform** - Works on Linux, macOS, and Windows (WSL)

## For RSI sufferers:
- Minimal keyboard use - just speak your prompts
- Voice-driven editing - describe changes verbally
- Configurable listening duration - take your time formulating thoughts

Voice Mode turns those detailed prompts into natural conversations. No more struggling with backspace or editing - just talk through your ideas!

Would love to help you both get started with hands-free coding!