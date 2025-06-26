#!/usr/bin/env python3
"""Test script for TTS model selection in voice-mcp"""

import asyncio
from voice_mode.core import get_openai_clients, text_to_speech
from voice_mode.server import get_tts_config
import os

async def test_tts_models():
    """Test different TTS models with OpenAI provider"""
    
    # Setup
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    if not OPENAI_API_KEY:
        print("❌ OPENAI_API_KEY environment variable not set")
        return
    
    TTS_BASE_URL = os.getenv("TTS_BASE_URL", "https://api.openai.com/v1")
    STT_BASE_URL = os.getenv("STT_BASE_URL", "https://api.openai.com/v1")
    
    # Initialize clients
    openai_clients = get_openai_clients(OPENAI_API_KEY, STT_BASE_URL, TTS_BASE_URL)
    
    # Test different models
    test_cases = [
        {
            "name": "Default model (tts-1)",
            "provider": "openai",
            "voice": "nova",
            "model": None,
            "instructions": None,
            "text": "Testing default TTS model."
        },
        {
            "name": "TTS-1 HD model",
            "provider": "openai", 
            "voice": "nova",
            "model": "tts-1-hd",
            "instructions": None,
            "text": "Testing TTS one HD model for higher quality."
        },
        {
            "name": "GPT-4o-mini-tts with coral voice",
            "provider": "openai",
            "voice": "coral",
            "model": "gpt-4o-mini-tts",
            "instructions": None,
            "text": "Testing GPT four o mini TTS model with coral voice."
        },
        {
            "name": "GPT-4o-mini-tts with cheerful instructions",
            "provider": "openai",
            "voice": "coral",
            "model": "gpt-4o-mini-tts",
            "instructions": "Speak in a cheerful and energetic tone",
            "text": "Today is a wonderful day to build something people love!"
        },
        {
            "name": "GPT-4o-mini-tts with serious instructions",
            "provider": "openai",
            "voice": "coral",
            "model": "gpt-4o-mini-tts",
            "instructions": "Speak in a serious and professional tone",
            "text": "The quarterly financial report shows significant growth."
        }
    ]
    
    for test in test_cases:
        print(f"\n🧪 Testing: {test['name']}")
        print(f"   Provider: {test['provider']}")
        print(f"   Model: {test['model'] or 'default'}")
        print(f"   Voice: {test['voice']}")
        if test.get('instructions'):
            print(f"   Instructions: {test['instructions']}")
        
        try:
            # Get TTS config
            tts_config = get_tts_config(test['provider'], test['voice'], test['model'], test.get('instructions'))
            print(f"   Config: model={tts_config['model']}, voice={tts_config['voice']}")
            
            # Test TTS
            success = await text_to_speech(
                text=test['text'],
                openai_clients=openai_clients,
                tts_model=tts_config['model'],
                tts_base_url=tts_config['base_url'],
                tts_voice=tts_config['voice'],
                debug=True,
                debug_dir=None,
                client_key=tts_config.get('client_key', 'tts'),
                instructions=tts_config.get('instructions')
            )
            
            if success:
                print("   ✅ Success!")
            else:
                print("   ❌ Failed")
                
        except Exception as e:
            print(f"   ❌ Error: {e}")
    
    # Cleanup
    for client_name, client in openai_clients.items():
        if hasattr(client, '_client'):
            await client._client.aclose()

if __name__ == "__main__":
    asyncio.run(test_tts_models())