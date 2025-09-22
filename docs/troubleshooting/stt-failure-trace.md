# STT Failure Call Stack Trace

## Current Behavior - Issue #62 Scenario

### Scenario 1: Local Whisper on Wrong Endpoint (WITH OpenAI API Key)

```
1. converse() - User speaks
   └─> record_audio_with_silence_detection()
       └─> Returns: audio_data (valid), speech_detected=True

2. speech_to_text(audio_data)
   └─> speech_to_text_with_failover(audio_data)
       └─> simple_stt_failover(audio_file)
           ├─> Attempt 1: localhost:2022 (Whisper)
           │   └─> AsyncOpenAI(base_url="http://localhost:2022")
           │       └─> client.audio.transcriptions.create()
           │           └─> ConnectionError: Connection refused
           │               (Whisper is on wrong endpoint, not /v1/audio/transcriptions)
           │
           ├─> Attempt 2: api.openai.com (OpenAI)
           │   └─> AsyncOpenAI(base_url="https://api.openai.com/v1")
           │       └─> client.audio.transcriptions.create()
           │           └─> Success OR AuthenticationError (if API key invalid)
           │
           └─> RETURNS: None (if all fail) OR {"text": "...", "provider": "openai"}

3. Back in converse():
   if stt_result is None:
       response_text = None  # Treated as "no speech"

4. User sees: "[no speech detected]" ❌ MISLEADING!
   Should see: "STT service connection failed: localhost:2022 - connection refused"
```

### Scenario 2: Local Whisper on Wrong Endpoint (NO OpenAI API Key)

```
1. converse() - User speaks
   └─> record_audio_with_silence_detection()
       └─> Returns: audio_data (valid), speech_detected=True

2. speech_to_text(audio_data)
   └─> speech_to_text_with_failover(audio_data)
       └─> simple_stt_failover(audio_file)
           │
           ├─> STT_BASE_URLS only contains localhost:2022
           │   (OpenAI URL not added because no API key)
           │
           ├─> Attempt 1: localhost:2022 (Whisper) - ONLY attempt
           │   └─> AsyncOpenAI(base_url="http://localhost:2022")
           │       └─> client.audio.transcriptions.create()
           │           └─> ConnectionError: Connection refused
           │
           └─> RETURNS: None (no fallback available)

3. Back in converse():
   if stt_result is None:
       response_text = None  # Treated as "no speech"

4. User sees: "[no speech detected]" ❌ MISLEADING!
   Should see: "STT service connection failed: localhost:2022 - connection refused (no fallback available)"
```

## Proposed Fix - Better Error Reporting

### Same Scenario with Fixed Code

```
1. converse() - User speaks
   └─> record_audio_with_silence_detection()
       └─> Returns: audio_data (valid), speech_detected=True

2. speech_to_text(audio_data)
   └─> speech_to_text_with_failover(audio_data)
       └─> simple_stt_failover(audio_file)
           ├─> Track: connection_errors = []
           ├─> Track: successful_but_empty = False
           │
           ├─> Attempt 1: localhost:2022 (Whisper)
           │   └─> AsyncOpenAI(base_url="http://localhost:2022")
           │       └─> client.audio.transcriptions.create()
           │           └─> ConnectionError: Connection refused
           │               └─> connection_errors.append({
           │                      "endpoint": "http://localhost:2022/v1/audio/transcriptions",
           │                      "error": "Connection refused",
           │                      "provider": "whisper"
           │                   })
           │
           ├─> Attempt 2: api.openai.com (if API key exists)
           │   └─> AsyncOpenAI(base_url="https://api.openai.com/v1")
           │       └─> client.audio.transcriptions.create()
           │           ├─> IF Success with empty text:
           │           │   └─> successful_but_empty = True
           │           └─> IF Error:
           │               └─> connection_errors.append({...})
           │
           └─> RETURNS:
               IF successful_but_empty:
                   {"text": "", "no_speech": True}
               ELSE IF all failed:
                   {"error_type": "connection_error",
                    "attempted_endpoints": connection_errors}

3. Back in converse():
   if "error_type" in stt_result and stt_result["error_type"] == "connection_error":
       # Build helpful error message
       errors = stt_result["attempted_endpoints"]
       error_msg = "STT service connection failed:\n"
       for attempt in errors:
           error_msg += f"  - {attempt['endpoint']}: {attempt['error']}\n"
       response_text = None
       return error_msg  # Return early with clear error

   elif "no_speech" in stt_result:
       response_text = None  # Genuine no speech

4. User sees HELPFUL error:
   "STT service connection failed:
    - http://localhost:2022/v1/audio/transcriptions: Connection refused
    - https://api.openai.com/v1/audio/transcriptions: Unauthorized (invalid API key)"
```

## Key Files to Modify

1. **voice_mode/simple_failover.py**
   - `simple_stt_failover()`: Return structured dict with error details

2. **voice_mode/tools/converse.py**
   - Lines 1798-1810: Handle error dict from STT
   - Lines 1780-1783: Only treat as "no speech" if genuine, not connection error

## Detection Logic

The fix needs to distinguish between:

1. **Connection/Auth Errors** (report to user):
   - ConnectionError, ConnectionRefusedError
   - AuthenticationError (401)
   - HTTPStatusError with specific codes

2. **Genuine "No Speech"** (silent recording):
   - Successful API call
   - Returns empty text or very short text
   - No connection errors

3. **Mixed Results** (at least one worked):
   - If ANY endpoint successfully connected and returned empty → "no speech"
   - Only report connection error if ALL endpoints failed to connect