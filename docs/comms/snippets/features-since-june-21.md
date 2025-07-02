# Major Features Added Since June 21st

Since you last looked at VoiceMode on June 21st, we've shipped some game-changing improvements:

## 🚀 Key Features

1. **Automatic Silence Detection** - Reduced response time from 20s to ~1s for short responses
   - Uses WebRTC VAD to detect when you stop speaking
   - No more waiting for fixed recording durations
   - Configurable sensitivity and thresholds

2. **Live Statistics Dashboard** - Real-time performance tracking
   - See TTFA (Time To First Audio), generation times, and total turnaround
   - Track success rates and provider usage
   - Export metrics for analysis

3. **Automatic Provider Failover** - Never lose voice capability
   - Seamlessly switches between providers when one fails
   - Supports local (Kokoro/Whisper) and cloud (OpenAI) services
   - No manual intervention needed

4. **No More Microphone Flickering** (macOS)
   - Changed to continuous recording stream
   - Prevents UI indicator from constantly turning on/off
   - More responsive recording starts

5. **Audio Format Improvements**
   - PCM as default for zero-latency streaming
   - Support for multiple formats (MP3, WAV, FLAC, AAC, Opus)
   - Format-specific quality settings

6. **Voice-First Provider Selection**
   - Automatically selects the right provider based on voice preference
   - Kokoro selected automatically when using af_sky voice
   - Smarter model selection respecting provider capabilities

## Try It Out

These features make VoiceMode significantly more responsive and reliable than when you first saw it. The silence detection alone transforms the experience - conversations feel natural instead of waiting for timeouts.