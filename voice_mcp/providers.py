"""
Provider selection and management for voice-mcp.

This module provides compatibility layer and selection logic for voice providers,
working with the dynamic provider discovery system.
"""

import logging
from typing import Dict, Optional, List, Any, Tuple
from openai import AsyncOpenAI

from .config import TTS_VOICES, TTS_MODELS, OPENAI_API_KEY
from .provider_discovery import provider_registry, EndpointInfo

logger = logging.getLogger("voice-mcp")


async def get_tts_client_and_voice(
    voice: Optional[str] = None,
    model: Optional[str] = None,
    base_url: Optional[str] = None
) -> Tuple[AsyncOpenAI, str, str, EndpointInfo]:
    """
    Get TTS client with automatic selection based on preferences.
    
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
    
    # If specific voice is requested, find endpoint that supports it
    if voice:
        logger.info(f"TTS Provider Selection: Looking for endpoint with voice '{voice}'")
        endpoint_info = provider_registry.find_endpoint_with_voice(voice)
        if not endpoint_info:
            raise ValueError(f"No available endpoint supports voice '{voice}'")
        
        selected_model = model or _select_model_for_endpoint(endpoint_info)
        
        client = AsyncOpenAI(
            api_key=OPENAI_API_KEY,
            base_url=endpoint_info.url
        )
        
        logger.info(f"  • Selected endpoint: {endpoint_info.url}")
        logger.info(f"  • Selected voice: {voice}")
        logger.info(f"  • Selected model: {selected_model}")
        
        return client, voice, selected_model, endpoint_info
    
    # Otherwise, find first endpoint with a preferred voice
    logger.info(f"TTS Provider Selection: No specific voice requested, checking preferred voices: {TTS_VOICES}")
    for preferred_voice in TTS_VOICES:
        endpoint_info = provider_registry.find_endpoint_with_voice(preferred_voice)
        if endpoint_info:
            selected_model = model or _select_model_for_endpoint(endpoint_info)
            
            client = AsyncOpenAI(
                api_key=OPENAI_API_KEY,
                base_url=endpoint_info.url
            )
            
            logger.info(f"  • Selected endpoint: {endpoint_info.url}")
            logger.info(f"  • Selected voice: {preferred_voice}")
            logger.info(f"  • Selected model: {selected_model}")
            
            return client, preferred_voice, selected_model, endpoint_info
    
    # Last resort: use any available endpoint
    healthy_endpoints = provider_registry.get_healthy_endpoints("tts")
    if not healthy_endpoints:
        raise ValueError("No healthy TTS endpoints available")
    
    endpoint_info = healthy_endpoints[0]
    selected_voice = _select_voice_for_endpoint(endpoint_info)
    selected_model = model or _select_model_for_endpoint(endpoint_info)
    
    client = AsyncOpenAI(
        api_key=OPENAI_API_KEY,
        base_url=endpoint_info.url
    )
    
    return client, selected_voice, selected_model, endpoint_info


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