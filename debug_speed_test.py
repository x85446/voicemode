#!/usr/bin/env python3
"""Debug why speed parameter isn't affecting playback."""

import asyncio
from voice_mode.tools.converse import converse
import time

async def test_speed_with_timing():
    """Test speed and measure actual playback time."""
    
    test_message = "The quick brown fox jumps over the lazy dog. This is a test of speech speed control."
    
    print("Testing Voice Mode speed with timing measurements...")
    print("=" * 60)
    
    for speed in [0.5, 1.0, 2.0, 4.0]:
        print(f"\nTesting speed {speed}x...")
        
        # Use the converse tool directly but without waiting for response
        start = time.time()
        result = await converse.fn(
            message=test_message,
            wait_for_response=False,
            tts_provider="kokoro",
            voice="af_sky",
            speed=speed
        )
        elapsed = time.time() - start
        
        print(f"  Result: {result}")
        print(f"  Total time: {elapsed:.2f}s")
        
        # Wait a bit between tests
        await asyncio.sleep(2)

if __name__ == "__main__":
    asyncio.run(test_speed_with_timing())