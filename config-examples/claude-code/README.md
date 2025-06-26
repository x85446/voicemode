# Claude Code Configuration

Claude Code uses the `claude mcp add` command to configure MCP servers. Unlike Claude Desktop, it doesn't use JSON configuration files.

## Setup Commands

### Using uvx (Recommended)

```bash
export OPENAI_API_KEY=your-openai-key
claude mcp add voice-mode uvx voice-mode
```

### Using pip install

```bash
export OPENAI_API_KEY=your-openai-key
pip install voicemode
claude mcp add voice-mode voicemode
```

### Using Docker

```bash
export OPENAI_API_KEY=your-openai-key
claude mcp add voice-mode docker run -e OPENAI_API_KEY ghcr.io/mbailey/voicemode:latest
```

### Using Podman

```bash
export OPENAI_API_KEY=your-openai-key
claude mcp add voice-mode podman run -e OPENAI_API_KEY ghcr.io/mbailey/voicemode:latest
```

## With LiveKit Support

Set additional environment variables before running the claude mcp add command:

```bash
export OPENAI_API_KEY=your-openai-key
export LIVEKIT_URL=wss://your-app.livekit.cloud
export LIVEKIT_API_KEY=your-api-key
export LIVEKIT_API_SECRET=your-api-secret
claude mcp add voice-mode uvx voice-mode
```

## Usage

After adding voice-mode, start Claude Code:

```bash
claude
```

Then try: *"Let's have a voice conversation"*