# Session Notes - 2025-08-21

## Voice Mode Performance Analysis

### Cycle Time Measurement Issue
- **Problem**: Metrics show "total" time of 7-8 seconds per exchange, but actual time between exchange starts is 15-16 seconds
- **Gap**: ~7-8 seconds of unaccounted time after each exchange completes
- **Likely causes**:
  - Silence at end of recording not captured in metrics
  - Delay between exchanges (LLM setup time?)
  - Time to make request to voice mode not captured
- **TODO**: Improve metrics to capture full cycle time including all overhead

### Timing Breakdown (from counting test)
- Consistent 15-16 second intervals between exchange starts
- Active processing time: ~7-8 seconds
- Overhead breakdown per exchange:
  - STT + LLM + TTS generation: ~2.2-2.9 seconds
  - Untracked time: ~7-8 seconds

## Issues to Fix

### 1. Quiet Chimes on Mac with Headphones
- **Problem**: Audio feedback chimes (start/stop recording) are very quiet when using headphones on Mac
- **Impact**: User can't hear when recording starts/stops
- **TODO**: Investigate audio output levels for feedback sounds on macOS with headphones

## Feature Requests

### 1. Interruption Support
- **Feature**: Allow user to interrupt TTS playback
- **Implementation approach**:
  - Start listening when playback begins
  - Detect voice activity during playback
  - Stop playback if user speaks
  - Switch to recording mode immediately
- **Benefits**: More natural conversation flow, reduced wait times

### 2. Silence Filtering
- **Feature**: Don't send silence to STT service
- **Benefits**:
  - Reduce STT processing time
  - Reduce bandwidth/API costs
  - Faster response times
- **Implementation**: Filter out silence periods before sending audio to STT

## Technical Achievements Today

### Successfully Configured Local Voice Stack
- Whisper running with large-v3-turbo model
- Core ML acceleration enabled and working
- Kokoro TTS running locally
- Full local processing pipeline operational

### Fixed Issues
- Resolved Whisper Core ML model loading issue by switching to large-v3-turbo
- Fixed metool package structure (completions vs completion directory naming)
- Created lidsleep utility using caffeinate (no admin password required)

## Performance Metrics (Local Processing)
- TTFA (Time to First Audio): ~2-3 seconds average
- STT Processing: ~0.7-2 seconds for short phrases
- Full exchange time (active): ~7-8 seconds
- Full cycle time (actual): ~15-16 seconds