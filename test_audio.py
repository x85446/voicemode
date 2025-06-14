#!/usr/bin/env python3
"""Test audio playback directly"""
import asyncio
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from voice_mcp.core import text_to_speech
from openai import AsyncOpenAI
import logging

logging.basicConfig(level=logging.DEBUG)

async def test_tts():
    # Create OpenAI clients
    openai_clients = {
        'tts': AsyncOpenAI(
            api_key=os.getenv("OPENAI_API_KEY"),
            base_url=os.getenv("TTS_BASE_URL", "https://api.openai.com/v1")
        )
    }
    
    print(f"Testing TTS with base URL: {os.getenv('TTS_BASE_URL', 'https://api.openai.com/v1')}")
    
    # Test text
    test_text = "Hello! This is a test of the text to speech system. Can you hear me clearly?"
    
    # Try TTS
    success = await text_to_speech(
        text=test_text,
        openai_clients=openai_clients,
        tts_model=os.getenv("TTS_MODEL", "tts-1"),
        tts_voice=os.getenv("TTS_VOICE", "nova"),
        tts_base_url=os.getenv("TTS_BASE_URL", "https://api.openai.com/v1"),
        debug=True
    )
    
    print(f"TTS Success: {success}")
    
    # Cleanup
    await openai_clients['tts']._client.aclose()

if __name__ == "__main__":
    asyncio.run(test_tts())