#!/usr/bin/env python3
"""Test streaming audio functionality."""

import asyncio
import os
import sys
from pathlib import Path

# Add the parent directory to the path
sys.path.insert(0, str(Path(__file__).parent))

from voice_mcp.config import OPENAI_API_KEY, TTS_BASE_URL, TTS_MODEL, TTS_VOICE
from voice_mcp.core import get_openai_clients, text_to_speech


async def test_streaming():
    """Test the streaming TTS functionality."""
    print("Testing streaming audio playback...")
    print(f"TTS Base URL: {TTS_BASE_URL}")
    
    # Use appropriate voice based on TTS provider
    if "8880" in TTS_BASE_URL:
        # Kokoro voice
        voice = "af_sky"
        print("Detected Kokoro TTS, using voice: af_sky")
    else:
        # OpenAI voice
        voice = TTS_VOICE
    
    print(f"TTS Model: {TTS_MODEL}")
    print(f"TTS Voice: {voice}")
    
    # Get OpenAI clients
    clients = get_openai_clients(
        api_key=OPENAI_API_KEY,
        stt_base_url="https://api.openai.com/v1",  # Not used in this test
        tts_base_url=TTS_BASE_URL
    )
    
    # Test text
    test_text = "Testing streaming audio playback. The quick brown fox jumps over the lazy dog."
    
    # Run TTS with streaming
    success, metrics = await text_to_speech(
        text=test_text,
        openai_clients=clients,
        tts_model=TTS_MODEL,
        tts_voice=voice,
        tts_base_url=TTS_BASE_URL,
        debug=True
    )
    
    print(f"\nSuccess: {success}")
    if metrics:
        print(f"TTFA: {metrics.get('ttfa', 0):.3f}s")
        print(f"Generation time: {metrics.get('generation', 0):.3f}s")
        print(f"Playback time: {metrics.get('playback', 0):.3f}s")
    
    # Close clients
    for client in clients.values():
        if hasattr(client, '_client'):
            await client._client.aclose()


if __name__ == "__main__":
    # Set streaming enabled
    os.environ["VOICEMODE_STREAMING_ENABLED"] = "true"
    # Use MP3 for testing as Kokoro doesn't support Opus well
    os.environ["VOICEMODE_TTS_AUDIO_FORMAT"] = "mp3"
    
    asyncio.run(test_streaming())