# [DRAFT] No Speech Detected

<!-- Task: ~/tasks/voicemode_tool_playback_recordings/ --> 

## Symptoms

- Voice recording completes but returns "No speech detected"
- Recording runs for full duration (often 60-120 seconds) then times out
- STT processing takes unusually long (20-30+ seconds)
- Message appears even after clearly speaking into the microphone
- Timing shows long recording duration but no speech recognition

Example error:
```
No speech detected | Timing: ttfa 1.1s, gen 1.1s, play 16.9s, record 84.8s, stt 30.0s, total 132.8s
```

## Possible Causes

1. **Microphone not receiving audio** - Most common on first setup
2. **VAD (Voice Activity Detection) too aggressive** - Filtering out valid speech as noise
3. **Audio level too low** - Microphone gain or distance issues
4. **Wrong audio device selected** - System using different microphone
5. **Background noise interference** - VAD confused by ambient noise
6. **Silence detection triggered early** - Recording stopped before speech began

## Investigation

### 1. Find the Recorded Audio File

VoiceMode saves recordings in `~/.voicemode/audio/` organized by date:

```bash
# List recent recordings (STT input files)
ls -la ~/.voicemode/audio/$(date +%Y/%m)/*stt*.wav | tail -5

# Or find recordings from the last hour
find ~/.voicemode/audio -name "*stt*.wav" -mmin -60
```

### 2. Listen to the Recording

```bash
# Play the recording (macOS/Linux)
afplay ~/.voicemode/audio/2025/01/recording_stt_*.wav  # macOS
aplay ~/.voicemode/audio/2025/01/recording_stt_*.wav   # Linux

# Or use voicemode's play command
voicemode play ~/.voicemode/audio/2025/01/recording_stt_*.wav
```

### 3. Check What Was Actually Recorded

Listen for:
- Is there any audio at all? (completely silent = microphone issue)
- Is your voice audible? (too quiet = gain issue)
- Is there excessive background noise? (may confuse VAD)
- Does the recording cut off early? (silence detection too aggressive)

## Detailed Solutions

### Solution 1: Check Microphone Setup

1. **Verify microphone is working:**
   ```bash
   # List available audio devices
   voicemode diag devices

   # Test microphone directly
   voicemode converse --debug
   ```

2. **Check system audio settings:**
   - **macOS**: System Preferences → Sound → Input → Select correct microphone
   - **Windows**: Settings → System → Sound → Input → Choose your input device
   - **Linux**: `pavucontrol` or `alsamixer` to check input levels

3. **Test microphone with another application** to confirm it's working

### Solution 2: Adjust VAD Settings

1. **Reduce VAD aggressiveness** (make it less strict):
   ```bash
   # Set to less aggressive filtering (0-3, lower = less aggressive)
   export VOICEMODE_VAD_AGGRESSIVENESS=1

   # Or set in your MCP configuration
   ```

2. **Enable VAD debugging** to see what's happening:
   ```bash
   export VOICEMODE_VAD_DEBUG=true
   voicemode converse
   ```

   Look for output showing speech detection state changes.

3. **Disable silence detection temporarily:**
   ```python
   # The AI can use this parameter:
   converse("Message", disable_silence_detection=True)
   ```

### Solution 3: Increase Recording Parameters

1. **Extend minimum listening duration:**
   ```python
   # Give yourself more time before recording can stop
   converse("Message", min_listen_duration=5.0)
   ```

2. **Increase silence threshold** (wait longer after speech):
   ```bash
   export VOICEMODE_SILENCE_THRESHOLD_MS=1500  # 1.5 seconds
   ```

### Solution 4: Audio Level Issues

1. **Increase microphone gain:**
   - Check system audio settings
   - Move closer to microphone
   - Check if microphone has hardware gain control

2. **Test with manual recording:**
   ```bash
   # Record a test file
   voicemode record test.wav

   # Play it back to check volume
   voicemode play test.wav
   ```

### Solution 5: Environment Issues

1. **Reduce background noise:**
   - Move to quieter location
   - Use directional microphone
   - Enable noise suppression in system settings

2. **For noisy environments, increase VAD aggressiveness:**
   ```bash
   export VOICEMODE_VAD_AGGRESSIVENESS=3
   ```

## Prevention

### Best Practices

1. **Set up voice preferences** for consistent behavior:
   ```yaml
   # ~/.voicemode/preferences.yaml
   min_listen_duration: 3.0
   vad_aggressiveness: 2
   silence_threshold_ms: 1000
   ```

2. **Test your setup** after any system changes:
   ```bash
   voicemode test-audio
   ```

3. **Use appropriate settings for your environment:**
   - Quiet office: `VAD_AGGRESSIVENESS=1-2`
   - Noisy environment: `VAD_AGGRESSIVENESS=3`
   - Presentations/demos: `min_listen_duration=5.0`

### Configuration Checklist

- [ ] Correct microphone selected in system settings
- [ ] Microphone permissions granted (especially macOS)
- [ ] VAD aggressiveness appropriate for environment
- [ ] Minimum listen duration gives enough time to start speaking
- [ ] Silence threshold prevents premature cutoff

## Debug Information

When reporting this issue, include:

1. **Debug output:**
   ```bash
   export VOICEMODE_VAD_DEBUG=true
   voicemode converse --debug 2>&1 | tee debug.log
   ```

2. **System information:**
   ```bash
   voicemode diag info
   ```

3. **Event logs:**
   ```bash
   voicemode logs --tail 100 | grep -i "speech\|vad\|record"
   ```

## Related Issues

- [Audio Quality Issues](audio-quality.md) - Poor recognition accuracy
- [Microphone Access](../audio-devices/microphone-access.md) - Permission problems
- [Response Delays](response-delays.md) - Slow processing times
- [WSL2 Audio Setup](../audio-devices/wsl2-audio.md) - WSL-specific audio issues

## Technical Details

The "no speech detected" error occurs when:
1. Recording completes (by timeout or silence detection)
2. Audio is sent to STT service
3. STT service returns empty or no transcription
4. This typically means the VAD filtered out all audio as non-speech

The timing breakdown shows:
- `record`: Time spent recording audio
- `stt`: Time spent processing (often 30s timeout if no speech)
- `total`: End-to-end time for the entire operation
