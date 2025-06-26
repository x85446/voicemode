# Script: Using voice-mode with Claude Code

## Cold Open (15 seconds)

**[Screen shows terminal with Claude Code already running]**

**You:** "Hey Claude, I'm working on some screencasts for VoiceMode. Can you help me organize these files?"

**Claude:** "Sure! Let me create a README file for the screencasts directory."

**[Screen shows file being created]**

**Claude:** "Done! I created a README with your planned videos and a publishing checklist."

**You:** "Perfect, thanks!"

**[Cut to title card]**

---

## Title Card (5 seconds)
**Text on screen:** Using voice-mode with Claude Code

---

## Intro (15 seconds)

**You:** "Want to have conversations like that with Claude while you code? Let me show you how to set it up in under a minute."

**[Show prerequisites briefly on screen:]**
- macOS or Linux (Windows with WSL)
- Claude Code installed
- Python 3.10+

---

## Installation (45 seconds)

**You:** "First, let's install Claude Code if you haven't already."

```bash
npm install -g @anthropics/claude-code
```

**You:** "Now we need uvx for Python tools."

```bash
# macOS
brew install uv

# or with pip
pip install uv
```

You: Add voice-mode to Claude's configuration

```shell
claude mcp add --scope user voice-mode uvx voice-mode
```

**You:** "Now just run Claude and use the converse command."

```bash
claude converse
```

---

## Demo 1: Natural Conversation (1 minute)

**You:** "What should we work on today?"

**Claude:** "Let me check your recent activity. I can see you have uncommitted changes in the docs folder. Would you like me to review them?"

**You:** "Yeah, can you check what's changed?"

**Claude:** "I'll run git status for you."

**[Shows git status output]**

**Claude:** "You have new screencast outlines. Should I create a git commit for these?"

**You:** "Sure, go ahead."

---

## Demo 2: Making Changes (1 minute)

**You:** "Can you add a section about prerequisites to the README?"

**Claude:** "I'll add that now. Let me update the screencasts README with prerequisites."

**[Shows file being edited]**

**Claude:** "I've added a prerequisites section listing Claude Code, Python 3.10+, and microphone access. Anything else you'd like me to add?"

---

## Closing (30 seconds)

**You:** "So what else should we show them?"

**Claude:** "We could show them the self-hosted option! Let me start Kokoro and switch voices."

**[Brief pause while Kokoro starts]**

**Claude (now in Sky voice):** "Now I'm using the Sky voice. This runs completely on your machine - no API calls, totally private."

**You:** "That's perfect for developers who want to keep everything local."

**You:** "That's VoiceMode - natural voice conversations with Claude while you code. It supports:"

**[Bullet points appear on screen:]**
- Self-hosted STT/TTS
- Remote access via LiveKit  
- Linux, macOS, and Windows
- Works with other AI coding tools

**You:** "Get it at github.com/mbailey/voicemode. Links in the description. Happy coding!"

**[End screen with GitHub URL]**
