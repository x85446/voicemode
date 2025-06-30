# Reply to Claude Code Issue #154 - Voice Input

**From:** @getvoicemode  
**To:** https://github.com/anthropics/claude-code/issues/154  
**Subject:** Voice input suggestion

---

Hey @gerrywastaken! 👋

I saw this issue was closed with the OS dictation recommendation, but wanted to share that we've built something that goes way beyond basic dictation - true voice conversations with Claude Code!

[Voice Mode](https://github.com/mbailey/voicemode) is an MCP server that provides:

## Beyond dictation:
- **Two-way voice conversations** - Not just input, but hear Claude's responses too
- **Smart recording** - Automatically stops when you pause (no manual stop needed)
- **3x faster than typing** - As you mentioned, but even better when you hear responses!

## Quick setup:

```bash
# One command setup
claude mcp add voice-mode --env OPENAI_API_KEY=your-key -- uvx voice-mode

# Start conversing
claude converse
```

Then tell Claude: "Let's have a voice conversation" and you're off! 

## Why it's better than OS dictation:

1. **Natural conversations** - No push-to-talk, just speak naturally
2. **Context-aware** - Claude can ask clarifying questions verbally
3. **Code-optimized** - Handles technical terms and code syntax well
4. **Cross-platform** - Works on Linux, macOS, and Windows (WSL)

The push-to-talk idea from @djrodgerspryor is interesting - we use automatic silence detection instead, which feels more natural for conversations.

Would love to hear if this solves the productivity boost you were looking for!