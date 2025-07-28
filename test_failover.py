#!/usr/bin/env python3
"""Test script to debug TTS failover issue"""

import asyncio
import os
import sys
import logging

# Add the project to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Set up logging to see all messages
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Import after setting up logging
from voice_mode.simple_failover import simple_tts_failover
from voice_mode.config import TTS_BASE_URLS, OPENAI_API_KEY

async def test_failover():
    print(f"Testing TTS failover...")
    print(f"TTS_BASE_URLS: {TTS_BASE_URLS}")
    print(f"OPENAI_API_KEY set: {'Yes' if OPENAI_API_KEY else 'No'}")
    print(f"OPENAI_API_KEY first 10 chars: {OPENAI_API_KEY[:10] if OPENAI_API_KEY else 'Not set'}")
    
    # Stop Kokoro first
    import subprocess
    print("\nStopping Kokoro...")
    subprocess.run(["systemctl", "--user", "stop", "voicemode-kokoro"], capture_output=True)
    
    # Wait a moment
    await asyncio.sleep(2)
    
    # Try TTS
    print("\nTrying TTS with failover...")
    success, metrics, config = await simple_tts_failover(
        text="Testing failover",
        voice="alloy",
        model="tts-1"
    )
    
    print(f"\nResult: success={success}")
    print(f"Config: {config}")
    if not success:
        print(f"Error: {config.get('error', 'Unknown error')}")
    
    # Restart Kokoro
    print("\nRestarting Kokoro...")
    subprocess.run(["systemctl", "--user", "start", "voicemode-kokoro"], capture_output=True)

if __name__ == "__main__":
    asyncio.run(test_failover())