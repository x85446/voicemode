#!/usr/bin/env python3
"""Test the full converse path to debug failover"""

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

async def test_converse_path():
    # Import after setting up logging
    from voice_mode.tools.converse import text_to_speech_with_failover
    from voice_mode.config import TTS_VOICES, TTS_MODELS, DEBUG, DEBUG_DIR, SAVE_AUDIO, AUDIO_DIR
    
    print(f"Testing converse path...")
    print(f"TTS_VOICES: {TTS_VOICES}")
    print(f"TTS_MODELS: {TTS_MODELS}")
    
    # Stop Kokoro first
    import subprocess
    print("\nStopping Kokoro...")
    subprocess.run(["systemctl", "--user", "stop", "voicemode-kokoro"], capture_output=True)
    
    # Wait a moment
    await asyncio.sleep(2)
    
    # Try the actual text_to_speech_with_failover function
    print("\nCalling text_to_speech_with_failover...")
    try:
        success, tts_metrics, tts_config = await text_to_speech_with_failover(
            message="Testing converse path",
            voice=None,  # Let it use default
            model=None,  # Let it use default
            instructions=None,
            audio_format=None,
            initial_provider=None
        )
        
        print(f"\nResult: success={success}")
        print(f"Metrics: {tts_metrics}")
        print(f"Config: {tts_config}")
    except Exception as e:
        print(f"\nException: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()
    
    # Restart Kokoro
    print("\nRestarting Kokoro...")
    subprocess.run(["systemctl", "--user", "start", "voicemode-kokoro"], capture_output=True)

if __name__ == "__main__":
    asyncio.run(test_converse_path())