# Converse Command Code Path Analysis

## Issue
The conversation logs show `provider_url: "http://127.0.0.1:2022/v1"` (local Whisper) even when Whisper is stopped and OpenAI was actually used. The terminal output shows retries to `/audio/transcriptions`.

## Code Flow Trace

### 1. Entry Point: CLI Command
`voicemode converse` → `voice_mode/cli.py`

### 2. Converse Function Call Stack

```python
# CLI Entry
voice_mode/cli.py:converse_command()
    ↓
# Core converse implementation
voice_mode/core.py:converse()
    ↓
# Gets STT configuration
voice_mode/tools/converse.py:get_stt_config()
    ↓
# Provider selection
voice_mode/providers.py:get_stt_client()
    ↓
# Provider discovery
voice_mode/provider_discovery.py:ProviderRegistry.get_healthy_endpoints()
```

## Key Problem Areas

### 1. Provider Registry Caching
The `ProviderRegistry` likely caches endpoint health status and doesn't immediately detect when Whisper stops.

### 2. STT Config Fallback Logic
```python
# In voice_mode/tools/converse.py:get_stt_config()
try:
    client, selected_model, endpoint_info = await get_stt_client()
    return {
        'client': client,
        'base_url': endpoint_info.base_url,  # Still shows Whisper URL
        'provider': endpoint_info.base_url,
        'provider_type': endpoint_info.provider_type
    }
except Exception as e:
    # Fallback to OpenAI
    logger.warning(f"Falling back to OpenAI API for STT")
    return {
        'base_url': 'https://api.openai.com/v1',
        'is_fallback': True,
        'fallback_reason': str(e)
    }
```

### 3. The Real Issue: Client Object vs URL
The problem is that `get_stt_client()` returns a client object configured with Whisper's URL, but when that fails, the **client internally** retries with OpenAI (via the API key), while the metadata still shows the original Whisper URL.

## Evidence from Output

1. **Retry logs**: `Retrying request to /audio/transcriptions` - This is the OpenAI client retrying
2. **URL in logs**: Still shows `127.0.0.1:2022` because that's what the client was configured with
3. **No fallback fields**: `is_fallback` and `fallback_reason` are missing, meaning the exception wasn't caught at the config level

## Root Cause

The OpenAI client library itself is doing the fallback internally when the local endpoint fails, but this happens **after** the configuration is set. The actual flow:

1. `get_stt_client()` returns a client pointing to Whisper (127.0.0.1:2022)
2. Client tries to connect to Whisper - fails
3. OpenAI client library sees API key is set and retries against api.openai.com
4. Success - but metadata still shows original Whisper config

## Solution Needed

1. **Health check before returning client**: Verify endpoint is actually reachable
2. **Catch connection errors earlier**: Don't rely on OpenAI client's internal retry
3. **Update provider registry**: Force refresh when endpoints fail
4. **Fix logging**: Log the actual provider used, not just the configured one

## Code Path for Fix

```python
# Need to modify:
1. voice_mode/providers.py:get_stt_client()
   - Add actual connection test before returning

2. voice_mode/provider_discovery.py:ProviderRegistry
   - Don't cache failed endpoints
   - Refresh on each call or have shorter TTL

3. voice_mode/tools/converse.py
   - Catch connection errors and properly fallback
   - Update metadata after actual provider is determined
```

## Test Commands

```bash
# Stop Whisper
voicemode whisper stop

# Test with debug to see actual provider
VOICEMODE_DEBUG=1 voicemode converse

# Check what's actually happening
curl -X POST http://127.0.0.1:2022/v1/audio/transcriptions
# Should fail with connection refused
```

## Next Steps

1. Fix provider health checking to be real-time
2. Catch connection failures before OpenAI client retries
3. Update logging to show actual provider used, not configured provider
4. Consider removing OpenAI client's auto-retry or make it explicit