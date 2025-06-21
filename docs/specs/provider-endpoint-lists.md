# Provider Endpoint Lists Specification

## Overview

This specification describes a system for configuring multiple TTS and STT endpoints as comma-separated lists, with automatic failover and provider auto-detection.

## Current State

- Single endpoint configuration via `TTS_BASE_URL` and `STT_BASE_URL`
- Manual provider specification required for non-default endpoints
- No automatic failover between multiple endpoints
- Provider registry exists but doesn't support multiple endpoints per provider type

## Proposed Changes

### 1. Environment Variables

Replace or supplement existing single-endpoint variables with list support:

```bash
# Comma-separated list of TTS endpoints (tried in order)
VOICEMODE_TTS_ENDPOINTS=http://studio:8880/v1,http://localhost:8880/v1,https://api.openai.com/v1

# Comma-separated list of STT endpoints (tried in order)
VOICEMODE_STT_ENDPOINTS=http://studio:8080/v1,http://localhost:2022/v1,https://api.openai.com/v1

# Keep standard service URLs without prefix for backward compatibility
TTS_BASE_URL=http://studio:8880/v1  # Single endpoint (legacy)
STT_BASE_URL=http://studio:8080/v1  # Single endpoint (legacy)
```

### 2. Auto-Detection Strategy

For each endpoint in the list:

1. **Health Check**: Verify endpoint is reachable
2. **Model Discovery**: Query `/v1/models` to list available models
3. **Voice Discovery**: For TTS, query available voices
4. **Provider Identification**: 
   - Check model names (e.g., "tts-1" suggests OpenAI compatibility)
   - Check voice names (e.g., "af_sky" suggests Kokoro)
   - Check endpoint URL patterns
   - Default to "openai-compatible" if uncertain

### 3. Implementation Design

#### Configuration Module Updates

```python
# In voicemode/config.py

def parse_endpoint_list(env_var: str, fallback: str) -> List[str]:
    """Parse comma-separated endpoint list from environment."""
    value = os.getenv(env_var, fallback)
    return [endpoint.strip() for endpoint in value.split(",") if endpoint.strip()]

# Parse endpoint lists
TTS_ENDPOINTS = parse_endpoint_list("VOICEMODE_TTS_ENDPOINTS", TTS_BASE_URL)
STT_ENDPOINTS = parse_endpoint_list("VOICEMODE_STT_ENDPOINTS", STT_BASE_URL)

# Backward compatibility with both old and standard names
if not os.getenv("VOICEMODE_TTS_ENDPOINTS"):
    if os.getenv("TTS_ENDPOINTS"):
        TTS_ENDPOINTS = parse_endpoint_list("TTS_ENDPOINTS", TTS_BASE_URL)
    elif os.getenv("TTS_BASE_URL"):
        TTS_ENDPOINTS = [TTS_BASE_URL]
        
if not os.getenv("VOICEMODE_STT_ENDPOINTS"):
    if os.getenv("STT_ENDPOINTS"):
        STT_ENDPOINTS = parse_endpoint_list("STT_ENDPOINTS", STT_BASE_URL)
    elif os.getenv("STT_BASE_URL"):
        STT_ENDPOINTS = [STT_BASE_URL]
```

#### Provider Registry Updates

```python
# In voicemode/providers.py

@dataclass
class EndpointInfo:
    """Information about a discovered endpoint."""
    url: str
    available: bool
    models: List[str]
    voices: List[str]
    provider_type: str  # "openai", "kokoro", "whisper", "unknown"
    last_checked: float
    response_time_ms: Optional[float] = None

class EndpointRegistry:
    """Manages multiple endpoints with auto-detection and failover."""
    
    def __init__(self):
        self.endpoints: Dict[str, List[EndpointInfo]] = {
            "tts": [],
            "stt": []
        }
        self.cache_duration = 300  # 5 minutes
    
    async def discover_endpoint(self, url: str, service_type: str) -> EndpointInfo:
        """Discover capabilities of an endpoint."""
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
            
            return EndpointInfo(
                url=url,
                available=True,
                models=models,
                voices=voices,
                provider_type=provider_type,
                last_checked=time.time(),
                response_time_ms=response_time
            )
            
        except Exception as e:
            logger.warning(f"Endpoint {url} discovery failed: {e}")
            return EndpointInfo(
                url=url,
                available=False,
                models=[],
                voices=[],
                provider_type="unknown",
                last_checked=time.time()
            )
    
    def _identify_provider(self, url: str, models: List[str], voices: List[str]) -> str:
        """Identify provider type from endpoint characteristics."""
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
    
    async def get_best_endpoint(self, service_type: str, 
                               preferred_provider: Optional[str] = None) -> Optional[EndpointInfo]:
        """Get the best available endpoint for a service type."""
        # Refresh endpoint info if needed
        await self._refresh_endpoints(service_type)
        
        available = [ep for ep in self.endpoints[service_type] if ep.available]
        
        if not available:
            return None
        
        # Filter by preferred provider if specified
        if preferred_provider:
            preferred = [ep for ep in available if ep.provider_type == preferred_provider]
            if preferred:
                available = preferred
        
        # Sort by response time (fastest first)
        available.sort(key=lambda ep: ep.response_time_ms or float('inf'))
        
        return available[0]
```

#### Integration with Existing Code

```python
# In voicemode/core.py

# Global endpoint registry
endpoint_registry = EndpointRegistry()

async def get_tts_client_with_failover(voice: Optional[str] = None) -> Tuple[AsyncOpenAI, str]:
    """Get TTS client with automatic failover."""
    # Try to detect preferred provider from voice
    preferred_provider = None
    if voice:
        provider_info = get_provider_by_voice(voice)
        if provider_info:
            preferred_provider = provider_info.id
    
    # Get best endpoint
    endpoint = await endpoint_registry.get_best_endpoint("tts", preferred_provider)
    
    if not endpoint:
        raise ValueError("No available TTS endpoints")
    
    # Create client for endpoint
    client = AsyncOpenAI(
        api_key=OPENAI_API_KEY,
        base_url=endpoint.url
    )
    
    return client, endpoint.provider_type
```

### 4. Voice Status Integration

Update the `voice_status` tool to show all configured endpoints:

```python
async def get_voice_status() -> str:
    """Get comprehensive voice service status."""
    status = ["Voice Service Status", "=" * 50, ""]
    
    # Show all configured endpoints
    status.append("TTS Endpoints:")
    for i, endpoint in enumerate(TTS_ENDPOINTS):
        info = await endpoint_registry.discover_endpoint(endpoint, "tts")
        symbol = "✅" if info.available else "❌"
        status.append(f"  {i+1}. {symbol} {endpoint}")
        if info.available:
            status.append(f"     Provider: {info.provider_type}")
            status.append(f"     Models: {', '.join(info.models[:3])}")
            status.append(f"     Response: {info.response_time_ms:.0f}ms")
    
    status.append("\nSTT Endpoints:")
    # Similar for STT...
    
    return "\n".join(status)
```

### 5. Benefits

1. **Automatic Failover**: If studio:8880 is down, automatically use localhost:8880
2. **Performance Optimization**: Always use the fastest available endpoint
3. **No Provider Hardcoding**: System discovers capabilities automatically
4. **Backward Compatible**: Single URL variables still work
5. **Future Proof**: Supports any OpenAI-compatible endpoint

### 6. Configuration Examples

#### Home + Cloud Fallback
```bash
VOICEMODE_TTS_ENDPOINTS=http://studio:8880/v1,https://api.openai.com/v1
```

#### Development Setup
```bash
VOICEMODE_TTS_ENDPOINTS=http://localhost:8880/v1,http://studio:8880/v1,https://api.openai.com/v1
VOICEMODE_STT_ENDPOINTS=http://localhost:2022/v1,https://api.openai.com/v1
```

#### Production with Multiple Regions
```bash
VOICEMODE_TTS_ENDPOINTS=https://tts-us-east.company.com/v1,https://tts-eu.company.com/v1,https://api.openai.com/v1
```

#### Using standard service URLs (backward compatible)
```bash
# These still work without prefix
TTS_BASE_URL=http://studio:8880/v1
STT_BASE_URL=http://studio:8080/v1
OPENAI_API_KEY=sk-...
```

### 7. Implementation Plan

1. **Phase 1**: Parse comma-separated environment variables
2. **Phase 2**: Implement endpoint discovery and caching
3. **Phase 3**: Add failover logic to TTS/STT functions
4. **Phase 4**: Update voice_status tool
5. **Phase 5**: Add metrics and monitoring
6. **Phase 6**: Documentation and examples

### 8. Future Enhancements

1. **Weighted Load Balancing**: Distribute requests across endpoints
2. **Geographic Routing**: Choose endpoint based on user location
3. **Circuit Breaker**: Temporarily disable failing endpoints
4. **Custom Health Checks**: Provider-specific health validation
5. **Endpoint Priorities**: Allow manual priority configuration