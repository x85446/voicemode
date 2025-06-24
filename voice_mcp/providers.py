"""
Provider selection and management for voice-mcp.

This module provides compatibility layer and selection logic for voice providers,
working with the dynamic provider discovery system.
"""

import logging
from typing import Dict, Optional, List, Any, Tuple
from openai import AsyncOpenAI

from .config import TTS_VOICES, TTS_MODELS, TTS_BASE_URLS, OPENAI_API_KEY
from .provider_discovery import provider_registry, EndpointInfo

logger = logging.getLogger("voice-mcp")


async def get_tts_client_and_voice(
    voice: Optional[str] = None,
    model: Optional[str] = None,
    base_url: Optional[str] = None
) -> Tuple[AsyncOpenAI, str, str, EndpointInfo]:
    """
    Get TTS client with automatic selection based on preferences.
    
    Selection algorithm:
    1. If specific base_url requested, use it with specified/best voice and model
    2. If specific voice/model requested, iterate through TTS_BASE_URLS to find first
       healthy endpoint that supports them
    3. Otherwise, iterate through TTS_BASE_URLS and for each healthy endpoint:
       - Find first supported voice from TTS_VOICES
       - Find first supported model from TTS_MODELS
       - Use this combination
    
    Args:
        voice: Specific voice to use (optional)
        model: Specific model to use (optional)
        base_url: Specific base URL to use (optional)
    
    Returns:
        Tuple of (client, selected_voice, selected_model, endpoint_info)
    
    Raises:
        ValueError: If no suitable endpoint is found
    """
    # Ensure registry is initialized
    await provider_registry.initialize()
    
    # If specific base_url is requested, use it directly
    if base_url:
        logger.info(f"TTS Provider Selection: Using specific base URL: {base_url}")
        endpoint_info = provider_registry.registry["tts"].get(base_url)
        if not endpoint_info or not endpoint_info.healthy:
            raise ValueError(f"Requested base URL {base_url} is not available")
        
        selected_voice = voice or _select_voice_for_endpoint(endpoint_info)
        selected_model = model or _select_model_for_endpoint(endpoint_info)
        
        client = AsyncOpenAI(
            api_key=OPENAI_API_KEY,
            base_url=base_url
        )
        
        logger.info(f"  • Selected endpoint: {base_url}")
        logger.info(f"  • Selected voice: {selected_voice}")
        logger.info(f"  • Selected model: {selected_model}")
        
        return client, selected_voice, selected_model, endpoint_info
    
    # New algorithm: iterate through TTS_BASE_URLS in preference order
    logger.info(f"TTS Provider Selection: Checking endpoints in order: {TTS_BASE_URLS}")
    logger.info(f"  Preferred voices: {TTS_VOICES}")
    logger.info(f"  Preferred models: {TTS_MODELS}")
    
    for url in TTS_BASE_URLS:
        endpoint_info = provider_registry.registry["tts"].get(url)
        if not endpoint_info or not endpoint_info.healthy:
            logger.debug(f"  Skipping unhealthy endpoint: {url}")
            continue
        
        # If specific voice requested, check if this endpoint supports it
        if voice:
            if voice not in endpoint_info.voices:
                logger.debug(f"  Endpoint {url} doesn't support requested voice '{voice}'")
                continue
            selected_voice = voice
        else:
            # Find first preferred voice this endpoint supports
            selected_voice = None
            for preferred_voice in TTS_VOICES:
                if preferred_voice in endpoint_info.voices:
                    selected_voice = preferred_voice
                    break
            
            if not selected_voice:
                # No preferred voices available, use first available
                if endpoint_info.voices:
                    selected_voice = endpoint_info.voices[0]
                else:
                    logger.debug(f"  Endpoint {url} has no voices available")
                    continue
        
        # If specific model requested, check if this endpoint supports it
        if model:
            if model not in endpoint_info.models:
                logger.debug(f"  Endpoint {url} doesn't support requested model '{model}'")
                continue
            selected_model = model
        else:
            # Find first preferred model this endpoint supports
            selected_model = None
            for preferred_model in TTS_MODELS:
                if preferred_model in endpoint_info.models:
                    selected_model = preferred_model
                    break
            
            if not selected_model:
                # No preferred models available, use first available
                if endpoint_info.models:
                    selected_model = endpoint_info.models[0]
                else:
                    # Default to tts-1 if no models reported
                    selected_model = "tts-1"
        
        # We found a suitable endpoint with voice and model
        client = AsyncOpenAI(
            api_key=OPENAI_API_KEY,
            base_url=url
        )
        
        logger.info(f"  ✓ Selected endpoint: {url}")
        logger.info(f"  ✓ Selected voice: {selected_voice}")
        logger.info(f"  ✓ Selected model: {selected_model}")
        
        return client, selected_voice, selected_model, endpoint_info
    
    # No suitable endpoint found
    raise ValueError("No healthy TTS endpoints found that support requested voice/model preferences")


async def get_stt_client(
    model: Optional[str] = None,
    base_url: Optional[str] = None
) -> Tuple[AsyncOpenAI, str, EndpointInfo]:
    """
    Get STT client with automatic selection.
    
    Args:
        model: Specific model to use (optional)
        base_url: Specific base URL to use (optional)
    
    Returns:
        Tuple of (client, selected_model, endpoint_info)
    
    Raises:
        ValueError: If no suitable endpoint is found
    """
    # Ensure registry is initialized
    await provider_registry.initialize()
    
    # If specific base_url is requested, use it directly
    if base_url:
        endpoint_info = provider_registry.registry["stt"].get(base_url)
        if not endpoint_info or not endpoint_info.healthy:
            raise ValueError(f"Requested base URL {base_url} is not available")
        
        selected_model = model or "whisper-1"  # Default STT model
        
        client = AsyncOpenAI(
            api_key=OPENAI_API_KEY,
            base_url=base_url
        )
        
        return client, selected_model, endpoint_info
    
    # Get any healthy STT endpoint
    healthy_endpoints = provider_registry.get_healthy_endpoints("stt")
    if not healthy_endpoints:
        raise ValueError("No healthy STT endpoints available")
    
    endpoint_info = healthy_endpoints[0]
    selected_model = model or "whisper-1"
    
    client = AsyncOpenAI(
        api_key=OPENAI_API_KEY,
        base_url=endpoint_info.url
    )
    
    return client, selected_model, endpoint_info


def _select_voice_for_endpoint(endpoint_info: EndpointInfo) -> str:
    """Select the best available voice for an endpoint."""
    # Try to find a preferred voice
    for voice in TTS_VOICES:
        if voice in endpoint_info.voices:
            return voice
    
    # Otherwise use first available voice
    if endpoint_info.voices:
        return endpoint_info.voices[0]
    
    # Fallback
    return "alloy"


def _select_model_for_endpoint(endpoint_info: EndpointInfo) -> str:
    """Select the best available model for an endpoint."""
    # Try to find a preferred model
    for model in TTS_MODELS:
        if model in endpoint_info.models:
            return model
    
    # Otherwise use first available model
    if endpoint_info.models:
        return endpoint_info.models[0]
    
    # Fallback
    return "tts-1"


# Compatibility functions for existing code

async def is_provider_available(provider_id: str, timeout: float = 2.0) -> bool:
    """Check if a provider is available (compatibility function)."""
    # This is now handled by the provider registry
    await provider_registry.initialize()
    
    # Map old provider IDs to base URLs
    provider_map = {
        "kokoro": "http://localhost:8880/v1",
        "openai": "https://api.openai.com/v1",
        "whisper-local": "http://localhost:2022/v1",
        "openai-whisper": "https://api.openai.com/v1"
    }
    
    base_url = provider_map.get(provider_id)
    if not base_url:
        return False
    
    # Check in appropriate registry
    service_type = "tts" if provider_id in ["kokoro", "openai"] else "stt"
    endpoint_info = provider_registry.registry[service_type].get(base_url)
    
    return endpoint_info.healthy if endpoint_info else False


def get_provider_by_voice(voice: str) -> Optional[Dict[str, Any]]:
    """Get provider info by voice (compatibility function)."""
    # Kokoro voices
    if voice.startswith(('af_', 'am_', 'bf_', 'bm_')):
        return {
            "id": "kokoro",
            "name": "Kokoro TTS",
            "type": "tts",
            "base_url": "http://localhost:8880/v1",
            "voices": ["af_sky", "af_sarah", "am_adam", "af_nicole", "am_michael"]
        }
    
    # OpenAI voices
    return {
        "id": "openai",
        "name": "OpenAI TTS",
        "type": "tts",
        "base_url": "https://api.openai.com/v1",
        "voices": ["alloy", "nova", "echo", "fable", "onyx", "shimmer"]
    }


def select_best_voice(provider: str, available_voices: Optional[List[str]] = None) -> Optional[str]:
    """Select the best available voice (compatibility function)."""
    if available_voices is None:
        # Get from registry if possible
        if provider == "kokoro":
            available_voices = ["af_sky", "af_sarah", "am_adam", "af_nicole", "am_michael"]
        else:
            available_voices = ["alloy", "nova", "echo", "fable", "onyx", "shimmer"]
    
    # Find first preferred voice that's available
    for voice in TTS_VOICES:
        if voice in available_voices:
            return voice
    
    # Return first available
    return available_voices[0] if available_voices else None