#!/usr/bin/env python3
"""
Test script to debug voice-mcp hanging/crashing issues

Run this with VOICE_MCP_DEBUG=true or VOICE_MCP_DEBUG=trace
"""

import asyncio
import os
import time
from pathlib import Path

# Set debug environment variable
os.environ["VOICE_MCP_DEBUG"] = "trace"

# Import after setting env var
from openai import AsyncOpenAI


async def test_converse_cycles():
    """Test multiple converse cycles to reproduce hanging"""
    
    # Initialize client
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("Error: OPENAI_API_KEY not set")
        return
    
    tts_base_url = os.getenv("TTS_BASE_URL", "https://api.openai.com/v1")
    print(f"Using TTS base URL: {tts_base_url}")
    
    client = AsyncOpenAI(api_key=api_key, base_url=tts_base_url)
    
    # Test multiple cycles
    for i in range(5):
        print(f"\n=== Cycle {i+1} ===")
        start = time.time()
        
        try:
            # Test TTS
            print("Testing TTS...")
            response = await client.audio.speech.create(
                model="tts-1",
                input=f"Test message number {i+1}",
                voice="nova",
                response_format="mp3"
            )
            
            print(f"Response size: {len(response.content)} bytes")
            
            # Save to file
            test_file = Path(f"/tmp/test_tts_{i+1}.mp3")
            with open(test_file, "wb") as f:
                f.write(response.content)
            print(f"Saved to: {test_file}")
            
            # Small delay between cycles
            await asyncio.sleep(1)
            
        except Exception as e:
            print(f"Error in cycle {i+1}: {e}")
            import traceback
            traceback.print_exc()
        
        elapsed = time.time() - start
        print(f"Cycle {i+1} completed in {elapsed:.2f}s")
    
    # Clean up
    await client.close()
    print("\nAll cycles completed")


async def check_logs():
    """Check debug and trace logs"""
    home = Path.home()
    
    debug_log = home / "voice_mcp_debug.log"
    trace_log = home / "voice_mcp_trace.log"
    
    if debug_log.exists():
        print(f"\n=== Debug log tail ({debug_log}) ===")
        lines = debug_log.read_text().splitlines()
        for line in lines[-20:]:
            print(line)
    
    if trace_log.exists():
        print(f"\n=== Trace log tail ({trace_log}) ===")
        lines = trace_log.read_text().splitlines()
        for line in lines[-20:]:
            print(line)


if __name__ == "__main__":
    print("Voice-MCP Debug Test Script")
    print("===========================")
    
    # Run tests
    asyncio.run(test_converse_cycles())
    
    # Check logs
    asyncio.run(check_logs())