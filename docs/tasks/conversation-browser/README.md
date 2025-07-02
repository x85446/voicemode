# Conversation Browser

Web-based interface for browsing voice-mode conversations and audio recordings.

## Overview

The conversation browser (`scripts/conversation_browser.py`) provides a Flask-based web interface to view and playback voice conversations recorded by voice-mode.

## Current Features

- [x] UV single-file script with Flask
- [x] Parse transcription files with metadata
- [x] Group conversations by date or project
- [x] Collapsible date/project groups
- [x] Audio playback integration
- [x] Simple 60-second caching
- [x] Project path in metadata

## Tasks

### High Priority

- [x] Group exchanges into conversations based on time gaps (5 minutes)
- [x] Show conversation summaries in collapsed view
- [x] Better terminology: "exchanges" vs "conversations"
- [ ] Audio playback controls for individual interactions
- [ ] Audio playback for full conversations
- [ ] Selection checkboxes for choosing which interactions to include
- [ ] Export selected audio as concatenated file (podcast/soundcloud format)

### Medium Priority  

- [ ] MCP tools to start/stop/restart conversation browser
- [ ] Configure browser port and auto-open settings
- [ ] Search functionality
- [ ] Filter by project/date range
- [ ] Export conversations (markdown, JSON)
- [ ] Highlight matching audio/transcript pairs
- [ ] Show conversation duration/statistics
- [ ] Timeline scrubber for audio playback
- [ ] Multi-format audio export (MP3, M4A, OGG)

### Low Priority

- [ ] Real-time updates (websocket/SSE)
- [ ] Conversation tagging/categorization
- [ ] Bulk operations (delete old conversations)
- [ ] Mobile-responsive design improvements
- [ ] Dark mode

## Implementation Notes

### Grouping Logic

Exchanges should be grouped into conversations when:
- Same project path
- Less than 5 minutes gap between exchanges
- Ordered chronologically within conversation

### Terminology

- **Exchange**: Single interaction (one STT or conversation file)
- **Conversation**: Group of related exchanges
- **Session**: All conversations in a time period

### Audio Export Design

#### Playback Features
- Play button on each interaction (plays individual audio)
- Play button on conversation header (plays all selected interactions)
- Checkbox selection system with "select all" at conversation level
- Sequential playback using HTML5 audio API

#### Export Implementation
- Use ffmpeg to concatenate WAV files
- Process: decode headers → concatenate PCM data → encode to target format
- Support multiple output formats (WAV, MP3, M4A for podcasts)
- Add metadata (title, date, participants) to exported files

#### Export Directory Structure
```
~/.voicemode/
├── audio/              # Raw recordings (existing)
├── exports/            # All exported content
│   ├── podcasts/       # Podcast-ready files (MP3 + RSS)
│   ├── soundcloud/     # SoundCloud-optimized exports
│   ├── youtube/        # Audio with video placeholder
│   └── raw/            # Simple concatenated audio files
└── transcripts/        # Conversation logs (existing)
```

#### Platform Integration
- **Podcast Platforms**: Generate RSS feed + MP3s with ID3 tags for Anchor/Spotify/Apple
- **SoundCloud**: Direct upload API integration with proper metadata
- **YouTube**: Create video file with waveform visualization or static image
- **Local Files**: Simple MP3/M4A exports for sharing

#### MCP Integration
- New tools: `start_conversation_browser`, `stop_conversation_browser`, `browser_status`
- Parameters: port number, auto-open browser, background mode
- Browser runs as separate process managed by MCP server
- Status includes: running state, port, number of active sessions