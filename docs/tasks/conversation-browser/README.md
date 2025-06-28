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

### Medium Priority  

- [ ] Search functionality
- [ ] Filter by project/date range
- [ ] Export conversations (markdown, JSON)
- [ ] Highlight matching audio/transcript pairs
- [ ] Show conversation duration/statistics

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