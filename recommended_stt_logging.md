# Recommended STT Logging Additions

## Critical Missing Logs in simple_failover.py

### 1. STT Provider Attempt Logging (Line 142)
**Current:**
```python
logger.info(f"Trying STT endpoint: {base_url}")
```

**Recommended:**
```python
logger.info(f"Trying STT endpoint: {base_url}")
provider_type = detect_provider_type(base_url)
logger.info(f"STT provider selection: attempting {provider_type} at {base_url}")
```

### 2. STT Success Logging (Line 167)
**Current:**
```python
logger.info(f"STT succeeded with {base_url}")
```

**Recommended:**
```python
logger.info(f"STT succeeded with {provider_type} at {base_url}")
logger.info(f"STT transcription: {len(text)} characters transcribed")
```

### 3. STT Failure Logging (Line 172)
**Current:**
```python
logger.debug(f"STT failed for {base_url}: {e}")
```

**Recommended (change to warning/info level):**
```python
logger.warning(f"STT failed for {provider_type} at {base_url}: {e}")
if "openai.com" in base_url and "401" in str(e):
    logger.info("STT: Attempting fallback to OpenAI failed - check OPENAI_API_KEY")
```

### 4. Add OpenAI Fallback Detection
**Add after line 140 (before the loop):**
```python
# Log if we're attempting OpenAI as fallback
if len(STT_BASE_URLS) > 1 and "openai.com" in STT_BASE_URLS[-1]:
    logger.info("STT: Will attempt OpenAI API as fallback if local services fail")
```

## Additional Logging in providers.py

### get_stt_client() function (Line 176-215)
**Add more detailed logging:**
```python
async def get_stt_client(
    model: Optional[str] = None,
    base_url: Optional[str] = None
) -> Tuple[AsyncOpenAI, str, EndpointInfo]:
    # ... existing code ...

    # Add after line 178:
    logger.info(f"STT client selection starting...")

    # Add after line 181 (if specific base_url):
    if base_url:
        logger.info(f"STT: Using specific base URL: {base_url}")
        # ... existing code ...

    # Add after line 199 (when getting endpoints):
    endpoints = provider_registry.get_endpoints("stt")
    logger.info(f"STT: Found {len(endpoints)} available endpoints")
    for ep in endpoints:
        logger.debug(f"  - {ep.provider_type} at {ep.base_url}")

    # Add after line 203:
    endpoint_info = endpoints[0]
    logger.info(f"STT: Selected {endpoint_info.provider_type} at {endpoint_info.base_url}")
```

## Structured Logging Pattern

For consistency across TTS and STT, use this pattern:

```python
# At start of operation
logger.info(f"[OPERATION]: Starting [description]")
logger.debug(f"[OPERATION]: Config: [key details]")

# For each attempt
logger.info(f"[OPERATION]: Attempting with [provider] at [url]")

# On success
logger.info(f"[OPERATION]: ✓ Success with [provider] - [result summary]")

# On failure
logger.warning(f"[OPERATION]: Failed with [provider]: [error]")

# On fallback
logger.info(f"[OPERATION]: Falling back to [next provider]")
```

## Example Implementation for simple_stt_failover

```python
async def simple_stt_failover(
    audio_file,
    model: str = "whisper-1",
    **kwargs
) -> Optional[str]:
    """
    Simple STT failover - try each endpoint in order until one works.

    Returns:
        Transcribed text or None
    """
    last_error = None

    logger.info(f"STT: Starting transcription with {len(STT_BASE_URLS)} configured endpoints")

    # Check for OpenAI fallback configuration
    has_openai_fallback = any("openai.com" in url for url in STT_BASE_URLS)
    if has_openai_fallback and len(STT_BASE_URLS) > 1:
        logger.info("STT: OpenAI API configured as fallback option")

    # Try each STT endpoint in order
    for i, base_url in enumerate(STT_BASE_URLS, 1):
        try:
            # Detect provider type for better logging
            provider_type = detect_provider_type(base_url)
            logger.info(f"STT: Attempt {i}/{len(STT_BASE_URLS)} - {provider_type} at {base_url}")

            # Create client for this endpoint
            api_key = OPENAI_API_KEY if provider_type == "openai" else (OPENAI_API_KEY or "dummy-key-for-local")

            # Log if this is OpenAI and we're missing API key
            if provider_type == "openai" and not OPENAI_API_KEY:
                logger.warning("STT: Attempting OpenAI without API key - likely to fail")

            # Disable retries for local endpoints - they either work or don't
            max_retries = 0 if is_local_provider(base_url) else 2
            client = AsyncOpenAI(
                api_key=api_key,
                base_url=base_url,
                timeout=30.0,
                max_retries=max_retries
            )

            logger.debug(f"STT: Uploading audio to {provider_type}, model={model}")

            # Try STT with this endpoint
            transcription = await client.audio.transcriptions.create(
                model=model,
                file=audio_file,
                response_format="text"
            )

            text = transcription.strip() if isinstance(transcription, str) else transcription.text.strip()

            if text:
                logger.info(f"STT: ✓ Success with {provider_type} - transcribed {len(text)} characters")
                logger.debug(f"STT: Transcription preview: '{text[:50]}...'")
                return text
            else:
                logger.warning(f"STT: {provider_type} returned empty transcription")

        except Exception as e:
            last_error = str(e)
            error_type = type(e).__name__

            # Check for specific error types
            if "401" in str(e) or "unauthorized" in error_type.lower():
                if provider_type == "openai":
                    logger.error(f"STT: OpenAI authentication failed - check OPENAI_API_KEY")
                else:
                    logger.warning(f"STT: {provider_type} authentication failed")
            elif "connection" in error_type.lower() or "refused" in str(e).lower():
                logger.warning(f"STT: {provider_type} connection failed - service may be down")
            else:
                logger.warning(f"STT: {provider_type} failed with {error_type}: {e}")

            # If this was a local service and we have OpenAI fallback
            if i < len(STT_BASE_URLS) and provider_type in ["whisper", "local"]:
                next_url = STT_BASE_URLS[i]  # i is already 1-indexed
                next_provider = detect_provider_type(next_url)
                if next_provider == "openai":
                    logger.info(f"STT: Attempting OpenAI fallback after {provider_type} failure")

            # Continue to next endpoint
            continue

    # All endpoints failed
    logger.error(f"STT: All {len(STT_BASE_URLS)} endpoints failed")
    logger.error(f"STT: Last error: {last_error}")

    # Provide helpful error message
    if has_openai_fallback and not OPENAI_API_KEY:
        logger.error("STT: Consider setting OPENAI_API_KEY for cloud fallback")

    return None
```

## Testing the Logging

To verify the logging is working:

1. **Test with all services down:**
   ```bash
   # Stop local services
   VOICEMODE_STT_BASE_URLS="http://127.0.0.1:2022/v1,https://api.openai.com/v1" voicemode
   # Should see clear progression through endpoints
   ```

2. **Test with missing API key:**
   ```bash
   unset OPENAI_API_KEY
   # Should see specific message about API key for OpenAI attempts
   ```

3. **Test with debug enabled:**
   ```bash
   VOICEMODE_DEBUG=true voicemode
   # Should see detailed transcription previews and config details
   ```

## Benefits of These Changes

1. **Debugging**: Can immediately see which STT provider is being used
2. **Troubleshooting**: Clear indication when fallback occurs
3. **Monitoring**: Can grep logs for "STT:" to track all speech operations
4. **User Support**: Error messages guide users to solutions (set API key, start service)
5. **Performance**: Can identify slow providers from logs