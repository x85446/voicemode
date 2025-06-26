# Voice Mode Integration Guides

This directory contains beginner-friendly, step-by-step integration guides for setting up Voice Mode with various AI coding assistants and development tools. Each guide assumes no prior experience with the tool and walks you through from installation to your first voice conversation.

## Available Integrations

### AI Coding Assistants

- 🤖 **[Claude Code](claude-code/README.md)** - Anthropic's official CLI for Claude
- 🖥️ **[Claude Desktop](claude-desktop/README.md)** - Claude's desktop application
- 🌟 **[Gemini CLI](gemini-cli/README.md)** - Google's Gemini command-line interface
- 🦘 **[Roo Code](roo-code/README.md)** - Roo Coder assistant
- ⚡ **[Cursor](cursor/README.md)** - The AI-first code editor
- 💻 **[VS Code](vscode/README.md)** - Visual Studio Code with MCP support
- 🔧 **[Cline](cline/README.md)** - Autonomous coding agent for VS Code
- ⚡ **[Zed](zed/README.md)** - High-performance, multiplayer code editor
- 🏄 **[Windsurf](windsurf/README.md)** - The IDE that writes code for you
- 🔄 **[Continue](continue/README.md)** - Open-source AI code assistant

## 🤝 Community Help Needed

> **Note**: These integration guides were created based on documentation and API specifications. We haven't yet tested installing and configuring each desktop application firsthand. If you're familiar with any of these tools, we'd greatly appreciate your review and feedback!
> 
> **How you can help:**
> - Test the integration steps with your tool
> - Submit issues for any inaccuracies or missing steps
> - Open PRs with improvements or corrections
> - Share tips that would help newcomers
>
> These guides are written for complete beginners - someone who has never used the tool before. Each guide should walk through everything from installation to first voice conversation.

## Quick Start

1. **Choose your tool** from the list above
2. **Follow the integration guide** specific to your tool
3. **Configure Voice Mode** with your OpenAI API key
4. **Start talking** to your AI assistant!

## Universal Requirements

All integrations require:
- Python 3.10 or higher
- [uv](https://github.com/astral-sh/uv) package manager
- OpenAI API key (or compatible service)
- System audio dependencies (see tool-specific guides)

## Creating New Integration Guides

To add a new integration guide:

1. Copy the [TEMPLATE.md](TEMPLATE.md) file
2. Create a new directory for your tool (e.g., `new-tool/`)
3. Save the template as `README.md` in that directory
4. Fill in all the placeholders with tool-specific information
5. Add screenshots or example configs if helpful
6. Update this README.md to include the new integration

## Integration Features

Voice Mode adds these capabilities to your development tools:

- 🎙️ **Natural voice conversations** - Speak your questions and hear responses
- 🚀 **Real-time interaction** - Code changes happen as you talk
- 🔒 **Privacy options** - Use local STT/TTS services for offline operation
- 🌐 **Room-based collaboration** - Share voice sessions via LiveKit
- 📊 **Performance metrics** - Track conversation statistics

## Need Help?

- 📚 Check the [main documentation](../../README.md)
- 🔧 Review [configuration options](../configuration.md)
- 💬 Join our [Discord community](https://discord.gg/gVHPPK5U)
- 🐛 See [troubleshooting guides](../troubleshooting/)
- 🔨 [Report issues or contribute improvements](https://github.com/mbailey/voicemode/issues)