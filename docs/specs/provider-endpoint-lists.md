# Provider Base URL Lists Specification

## Overview

This specification describes a system for configuring multiple TTS and STT base URLs as comma-separated lists, with automatic failover and provider auto-detection.

## Current State

- Single base URL configuration via `TTS_BASE_URL` and `STT_BASE_URL`
- Manual provider specification required for non-default base URLs
- No automatic failover between multiple base URLs
- Provider registry exists but doesn't support multiple base URLs per provider type

## Variables to Remove

The following environment variables should be removed as part of this change:

### From config.py:
- `TTS_BASE_URL` - replaced by `VOICEMODE_TTS_BASE_URLS`
- `STT_BASE_URL` - replaced by `VOICEMODE_STT_BASE_URLS`
- `OPENAI_TTS_BASE_URL` - no longer needed with auto-detection
- `KOKORO_TTS_BASE_URL` - no longer needed with auto-detection
- `TTS_VOICE` - replaced by `VOICEMODE_TTS_VOICES`
- `TTS_MODEL` - replaced by `VOICEMODE_TTS_MODELS`
- `STT_MODEL` - model selection should be per-request or auto-detected
- `VOICEMODE_VOICES` - replaced by `VOICEMODE_TTS_VOICES`
- `TTS_AUDIO_FORMAT` - replaced by `VOICEMODE_TTS_FORMATS`
- `STT_AUDIO_FORMAT` - replaced by `VOICEMODE_STT_FORMATS`
- `AUDIO_FORMAT` - replaced by format-specific lists

### Keep These:
- `OPENAI_API_KEY` - still needed for authentication
- `LIVEKIT_*` variables - separate system, not affected

## Proposed Changes

### 1. Environment Variables

New environment variables (no backward compatibility):

```bash
# Comma-separated list of TTS base URLs (tried in order)
VOICEMODE_TTS_BASE_URLS=http://studio:8880/v1,http://localhost:8880/v1,https://api.openai.com/v1

# Comma-separated list of STT base URLs (tried in order)
VOICEMODE_STT_BASE_URLS=http://studio:8080/v1,http://localhost:2022/v1,https://api.openai.com/v1

# Comma-separated list of preferred TTS voices (tried in order of availability)
VOICEMODE_TTS_VOICES=af_sky,alloy,nova,shimmer

# Comma-separated list of preferred TTS models (tried in order of availability)
VOICEMODE_TTS_MODELS=gpt-4o-mini-tts,tts-1,tts-1-hd

# Comma-separated list of preferred TTS audio formats (tried in order of availability)
# Note: PCM streams best (no decoding needed), AAC/MP3 work well
VOICEMODE_TTS_FORMATS=pcm,mp3,aac,opus

# Comma-separated list of preferred STT audio formats (tried in order of availability)
VOICEMODE_STT_FORMATS=opus,mp3,wav

# Language for both TTS and STT (ISO 639-1 code)
VOICEMODE_LANGUAGE=en

# API key for authentication (still required)
OPENAI_API_KEY=sk-...
```

### 2. Auto-Detection Strategy

For each base URL in the list:

1. **Health Check**: Verify base URL is reachable
2. **Model Discovery**: Query `/v1/models` endpoint to list available models
3. **Voice Discovery**: For TTS, query available voices
4. **Provider Identification**: 
   - Check model names (e.g., "tts-1" suggests OpenAI compatibility)
   - Check voice names (e.g., "af_sky" suggests Kokoro)
   - Check base URL patterns
   - Default to "openai-compatible" if uncertain

### 3. Implementation Design

#### Configuration Module Updates

```python
# In voicemode/config.py

def parse_base_url_list(env_var: str, fallback: str) -> List[str]:
    """Parse comma-separated base URL list from environment."""
    value = os.getenv(env_var, fallback)
    return [url.strip() for url in value.split(",") if url.strip()]

# Parse base URL lists (no backward compatibility)
TTS_BASE_URLS = parse_base_url_list(
    "VOICEMODE_TTS_BASE_URLS", 
    "https://api.openai.com/v1"  # Default to OpenAI if not set
)
STT_BASE_URLS = parse_base_url_list(
    "VOICEMODE_STT_BASE_URLS", 
    "https://api.openai.com/v1"  # Default to OpenAI if not set
)

# Parse voice and model preferences
TTS_VOICES = parse_base_url_list(
    "VOICEMODE_TTS_VOICES",
    "nova,alloy"  # Default voices
)
TTS_MODELS = parse_base_url_list(
    "VOICEMODE_TTS_MODELS",
    "tts-1"  # Default model
)

# Parse format preferences
TTS_FORMATS = parse_base_url_list(
    "VOICEMODE_TTS_FORMATS",
    "pcm,opus,mp3"  # Default formats for TTS
)
STT_FORMATS = parse_base_url_list(
    "VOICEMODE_STT_FORMATS",
    "opus,mp3,wav"  # Default formats for STT
)

# Parse language preference
LANGUAGE = os.getenv("VOICEMODE_LANGUAGE", "en")
```

#### Provider Registry Updates

```python
# In voicemode/providers.py

@dataclass
class BaseUrlInfo:
    """Information about a discovered base URL."""
    url: str
    available: bool
    models: List[str]
    voices: List[str]
    provider_type: str  # "openai", "kokoro", "whisper", "unknown"
    last_checked: float
    response_time_ms: Optional[float] = None

class BaseUrlRegistry:
    """Manages multiple base URLs with auto-detection and failover."""
    
    def __init__(self):
        self.base_urls: Dict[str, List[BaseUrlInfo]] = {
            "tts": [],
            "stt": []
        }
        self.cache_duration = 300  # 5 minutes
    
    async def discover_base_url(self, url: str, service_type: str) -> BaseUrlInfo:
        """Discover capabilities of a base URL."""
        start_time = time.time()
        
        try:
            # Create client for endpoint
            client = AsyncOpenAI(
                api_key=OPENAI_API_KEY or "dummy",
                base_url=url
            )
            
            # Try to list models
            models = []
            voices = []
            try:
                model_response = await client.models.list()
                models = [model.id for model in model_response.data]
            except:
                pass
            
            # For TTS, try to detect available voices
            if service_type == "tts" and models:
                # Try a mini TTS request to see what voices work
                # Or parse from model metadata if available
                voices = await self._detect_voices(client, models[0])
            
            # Identify provider type
            provider_type = self._identify_provider(url, models, voices)
            
            response_time = (time.time() - start_time) * 1000
            
            return BaseUrlInfo(
                url=url,
                available=True,
                models=models,
                voices=voices,
                provider_type=provider_type,
                last_checked=time.time(),
                response_time_ms=response_time
            )
            
        except Exception as e:
            logger.warning(f"Base URL {url} discovery failed: {e}")
            return BaseUrlInfo(
                url=url,
                available=False,
                models=[],
                voices=[],
                provider_type="unknown",
                last_checked=time.time()
            )
    
    def _identify_provider(self, url: str, models: List[str], voices: List[str]) -> str:
        """Identify provider type from base URL characteristics."""
        # URL-based detection
        if "openai.com" in url:
            return "openai"
        if ":8880" in url:  # Common Kokoro port
            return "kokoro"
        if ":2022" in url:  # Common Whisper port
            return "whisper"
        
        # Model-based detection
        if "tts-1" in models or "whisper-1" in models:
            return "openai"
        
        # Voice-based detection
        kokoro_voices = {"af_sky", "af_sarah", "am_adam", "af_nicole", "am_michael"}
        if any(voice in kokoro_voices for voice in voices):
            return "kokoro"
        
        return "unknown"
    
    async def get_best_base_url(self, service_type: str, 
                               preferred_provider: Optional[str] = None) -> Optional[BaseUrlInfo]:
        """Get the best available base URL for a service type."""
        # Refresh base URL info if needed
        await self._refresh_base_urls(service_type)
        
        available = [url for url in self.base_urls[service_type] if url.available]
        
        if not available:
            return None
        
        # Filter by preferred provider if specified
        if preferred_provider:
            preferred = [url for url in available if url.provider_type == preferred_provider]
            if preferred:
                available = preferred
        
        # Sort by response time (fastest first)
        available.sort(key=lambda url: url.response_time_ms or float('inf'))
        
        return available[0]
```

#### Integration with Existing Code

```python
# In voicemode/core.py

# Global base URL registry
base_url_registry = BaseUrlRegistry()

async def get_tts_client_with_failover(voice: Optional[str] = None, 
                                      model: Optional[str] = None) -> Tuple[AsyncOpenAI, str, str, str]:
    """Get TTS client with automatic failover and voice/model selection.
    
    Returns:
        Tuple of (client, provider_type, selected_voice, selected_model)
    """
    # Get best base URL that supports the requested voice/model
    best_match = None
    
    for base_url_info in await base_url_registry.get_all_available("tts"):
        # Check if this base URL supports our preferred voices/models
        voice_match = voice if voice in base_url_info.voices else None
        model_match = model if model in base_url_info.models else None
        
        # If no specific voice/model requested, find first match from preferences
        if not voice_match:
            for preferred_voice in TTS_VOICES:
                if preferred_voice in base_url_info.voices:
                    voice_match = preferred_voice
                    break
        
        if not model_match:
            for preferred_model in TTS_MODELS:
                if preferred_model in base_url_info.models:
                    model_match = preferred_model
                    break
        
        # If we found compatible voice and model, use this base URL
        if voice_match and model_match:
            best_match = (base_url_info, voice_match, model_match)
            break
    
    if not best_match:
        raise ValueError("No TTS base URL found with compatible voices/models")
    
    base_url_info, selected_voice, selected_model = best_match
    
    # Create client for base URL
    client = AsyncOpenAI(
        api_key=OPENAI_API_KEY,
        base_url=base_url_info.url
    )
    
    return client, base_url_info.provider_type, selected_voice, selected_model
```

### 4. Voice Status Integration

Update the `voice_status` tool to show all configured base URLs:

```python
async def get_voice_status() -> str:
    """Get comprehensive voice service status."""
    status = ["Voice Service Status", "=" * 50, ""]
    
    # Show all configured base URLs
    status.append("TTS Base URLs:")
    for i, base_url in enumerate(TTS_BASE_URLS):
        info = await base_url_registry.discover_base_url(base_url, "tts")
        symbol = "✅" if info.available else "❌"
        status.append(f"  {i+1}. {symbol} {base_url}")
        if info.available:
            status.append(f"     Provider: {info.provider_type}")
            status.append(f"     Models: {', '.join(info.models[:3])}")
            status.append(f"     Response: {info.response_time_ms:.0f}ms")
    
    status.append("\nSTT Base URLs:")
    # Similar for STT...
    
    return "\n".join(status)
```

### 5. Benefits

1. **Automatic Failover**: If studio:8880 is down, automatically use localhost:8880
2. **Performance Optimization**: Always use the fastest available base URL
3. **No Provider Hardcoding**: System discovers capabilities automatically
4. **Simplified Configuration**: No legacy variables to maintain
5. **Future Proof**: Supports any OpenAI-compatible base URL

### 6. Configuration Examples

#### Home + Cloud Fallback
```bash
VOICEMODE_TTS_BASE_URLS=http://studio:8880/v1,https://api.openai.com/v1
VOICEMODE_TTS_VOICES=af_sky,nova,alloy
VOICEMODE_TTS_MODELS=tts-1
VOICEMODE_TTS_FORMATS=pcm,opus
VOICEMODE_LANGUAGE=en
```

#### Development Setup
```bash
VOICEMODE_TTS_BASE_URLS=http://localhost:8880/v1,http://studio:8880/v1,https://api.openai.com/v1
VOICEMODE_STT_BASE_URLS=http://localhost:2022/v1,https://api.openai.com/v1
VOICEMODE_TTS_VOICES=af_sky,af_sarah,nova,shimmer
VOICEMODE_TTS_MODELS=tts-1,tts-1-hd
VOICEMODE_TTS_FORMATS=pcm,opus,mp3
VOICEMODE_STT_FORMATS=opus,mp3,wav
VOICEMODE_LANGUAGE=en
```

#### Production with Multiple Regions
```bash
VOICEMODE_TTS_BASE_URLS=https://tts-us-east.company.com/v1,https://tts-eu.company.com/v1,https://api.openai.com/v1
VOICEMODE_TTS_VOICES=nova,alloy,echo,fable,onyx,shimmer
VOICEMODE_TTS_MODELS=tts-1,tts-1-hd,gpt-4o-mini-tts
VOICEMODE_TTS_FORMATS=opus,mp3,aac
VOICEMODE_STT_FORMATS=opus,mp3
VOICEMODE_LANGUAGE=en
```

#### Minimal Configuration (uses OpenAI by default)
```bash
# Only API key required for default OpenAI usage
OPENAI_API_KEY=sk-...
# Defaults to OpenAI API with nova,alloy voices and tts-1 model
```

### 7. Implementation Plan

1. **Phase 1**: Parse comma-separated environment variables
2. **Phase 2**: Implement base URL discovery and caching
3. **Phase 3**: Add failover logic to TTS/STT functions
4. **Phase 4**: Update voice_status tool
5. **Phase 5**: Add metrics and monitoring
6. **Phase 6**: Documentation and examples

### 8. Future Enhancements

1. **Weighted Load Balancing**: Distribute requests across base URLs
2. **Geographic Routing**: Choose base URL based on user location
3. **Circuit Breaker**: Temporarily disable failing base URLs
4. **Custom Health Checks**: Provider-specific health validation
5. **Base URL Priorities**: Allow manual priority configuration
