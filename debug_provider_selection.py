#!/usr/bin/env python3
"""Debug script to check provider selection in real-time."""

import asyncio
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from voice_mode.config import TTS_VOICES, TTS_BASE_URLS, TTS_MODELS
from voice_mode.providers import get_tts_client_and_voice
from voice_mode.provider_discovery import provider_registry

async def debug_selection():
    print("=== Provider Selection Debug ===")
    print(f"TTS_VOICES from config: {TTS_VOICES}")
    print(f"TTS_BASE_URLS from config: {TTS_BASE_URLS}")
    print(f"TTS_MODELS from config: {TTS_MODELS}")
    
    # Initialize registry
    await provider_registry.initialize()
    
    print("\n=== Registry State ===")
    for url, info in provider_registry.registry["tts"].items():
        print(f"{url}:")
        print(f"  Provider: {info.provider_type}")
        print(f"  Healthy: {info.healthy}")
        print(f"  Voices: {info.voices[:3]}...")
        print(f"  Models: {info.models}")
    
    print("\n=== Provider Selection Test ===")
    try:
        client, voice, model, endpoint = await get_tts_client_and_voice()
        print(f"Selected endpoint: {endpoint.base_url}")
        print(f"Provider type: {endpoint.provider_type}")
        print(f"Voice: {voice}")
        print(f"Model: {model}")
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(debug_selection())