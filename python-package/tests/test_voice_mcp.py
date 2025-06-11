#!/usr/bin/env python
"""
Automated tests for voice-mcp MCP server.

Tests cover:
- Tool functionality (mocked audio I/O)
- Error handling
- Configuration management
- Transport selection logic
"""

import asyncio
import os
import tempfile
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock, patch
import pytest
import numpy as np
from fastmcp import Client

# Import the voice-mcp module components
import sys
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))


@pytest.fixture
def mock_openai_clients():
    """Mock OpenAI clients for STT and TTS"""
    stt_client = MagicMock()
    tts_client = MagicMock()
    
    # Mock STT response
    stt_response = MagicMock()
    stt_response.text = "Test transcription"
    stt_client.audio.transcriptions.create = AsyncMock(return_value=stt_response)
    
    # Mock TTS response
    tts_response = MagicMock()
    tts_response.content = b"fake audio data"
    tts_client.audio.speech.create = AsyncMock(return_value=tts_response)
    
    return {'stt': stt_client, 'tts': tts_client}


@pytest.fixture
def mock_audio_functions():
    """Mock audio recording and playback functions"""
    # Mock sounddevice functions
    with patch('sounddevice.rec') as mock_rec, \
         patch('sounddevice.play') as mock_play, \
         patch('sounddevice.wait') as mock_wait, \
         patch('sounddevice.query_devices') as mock_query:
        
        # Mock recording - return fake audio data
        mock_rec.return_value = np.array([[100], [200], [300]], dtype=np.int16)
        mock_query.return_value = [
            {'name': 'Test Input', 'max_input_channels': 2, 'max_output_channels': 0},
            {'name': 'Test Output', 'max_input_channels': 0, 'max_output_channels': 2}
        ]
        
        yield {
            'rec': mock_rec,
            'play': mock_play,
            'wait': mock_wait,
            'query': mock_query
        }


@pytest.fixture
async def voice_mcp_server(mock_openai_clients, mock_audio_functions):
    """Create a voice-mcp server instance with mocked dependencies"""
    # Set required environment variables
    os.environ['OPENAI_API_KEY'] = 'test-key'
    os.environ['VOICE_MCP_DEBUG'] = 'false'
    
    # Import and configure the server
    with patch('voice_mcp.scripts.voice-mcp.get_openai_clients', return_value=mock_openai_clients):
        # Import the script module
        import importlib.util
        spec = importlib.util.spec_from_file_location(
            "voice_mcp_script",
            Path(__file__).parent.parent / "src" / "voice_mcp" / "scripts" / "voice-mcp"
        )
        voice_mcp_module = importlib.util.module_from_spec(spec)
        
        # Patch audio-related imports before loading
        with patch.object(voice_mcp_module, 'sd', mock_audio_functions), \
             patch.object(voice_mcp_module, 'write') as mock_write:
            
            spec.loader.exec_module(voice_mcp_module)
            
            # Return the configured MCP server
            return voice_mcp_module.mcp


class TestVoiceMCPTools:
    """Test voice-mcp tool functionality"""
    
    @pytest.mark.asyncio
    async def test_speak_text(self, voice_mcp_server):
        """Test text-to-speech functionality"""
        async with Client(voice_mcp_server) as client:
            result = await client.call_tool("speak_text", {"text": "Hello, world!"})
            assert "successfully" in result[0].text.lower()
    
    @pytest.mark.asyncio
    async def test_listen_for_speech(self, voice_mcp_server):
        """Test speech-to-text functionality"""
        async with Client(voice_mcp_server) as client:
            result = await client.call_tool("listen_for_speech", {"duration": 1.0})
            assert "Test transcription" in result[0].text
    
    @pytest.mark.asyncio
    async def test_ask_voice_question_local(self, voice_mcp_server):
        """Test voice question with local transport"""
        async with Client(voice_mcp_server) as client:
            result = await client.call_tool(
                "ask_voice_question",
                {
                    "question": "What is your name?",
                    "transport": "local",
                    "duration": 2.0
                }
            )
            assert "Test transcription" in result[0].text
    
    @pytest.mark.asyncio
    async def test_check_audio_devices(self, voice_mcp_server):
        """Test audio device listing"""
        async with Client(voice_mcp_server) as client:
            result = await client.call_tool("check_audio_devices", {})
            assert "Input Devices" in result[0].text
            assert "Output Devices" in result[0].text
            assert "Test Input" in result[0].text
            assert "Test Output" in result[0].text


class TestErrorHandling:
    """Test error handling scenarios"""
    
    @pytest.mark.asyncio
    async def test_tts_api_error(self, voice_mcp_server, mock_openai_clients):
        """Test handling of TTS API errors"""
        # Make TTS fail
        mock_openai_clients['tts'].audio.speech.create.side_effect = Exception("API Error")
        
        async with Client(voice_mcp_server) as client:
            result = await client.call_tool("speak_text", {"text": "Test"})
            assert "Failed" in result[0].text or "Error" in result[0].text
    
    @pytest.mark.asyncio
    async def test_stt_api_error(self, voice_mcp_server, mock_openai_clients):
        """Test handling of STT API errors"""
        # Make STT fail
        mock_openai_clients['stt'].audio.transcriptions.create.side_effect = Exception("API Error")
        
        async with Client(voice_mcp_server) as client:
            result = await client.call_tool("listen_for_speech", {"duration": 1.0})
            assert "Error" in result[0].text or "No speech detected" in result[0].text
    
    @pytest.mark.asyncio
    async def test_recording_error(self, voice_mcp_server, mock_audio_functions):
        """Test handling of recording errors"""
        # Make recording fail
        mock_audio_functions['rec'].side_effect = Exception("Recording failed")
        
        async with Client(voice_mcp_server) as client:
            result = await client.call_tool("listen_for_speech", {"duration": 1.0})
            assert "Error" in result[0].text


class TestConfiguration:
    """Test configuration handling"""
    
    def test_environment_variables(self):
        """Test that environment variables are properly loaded"""
        # Set custom environment variables
        os.environ['STT_BASE_URL'] = 'http://localhost:2022/v1'
        os.environ['TTS_BASE_URL'] = 'http://localhost:8880/v1'
        os.environ['TTS_VOICE'] = 'custom_voice'
        os.environ['TTS_MODEL'] = 'custom-tts'
        os.environ['STT_MODEL'] = 'custom-stt'
        
        # Re-import to pick up new env vars
        import importlib
        spec = importlib.util.spec_from_file_location(
            "voice_mcp_script",
            Path(__file__).parent.parent / "src" / "voice_mcp" / "scripts" / "voice-mcp"
        )
        voice_mcp_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(voice_mcp_module)
        
        assert voice_mcp_module.STT_BASE_URL == 'http://localhost:2022/v1'
        assert voice_mcp_module.TTS_BASE_URL == 'http://localhost:8880/v1'
        assert voice_mcp_module.TTS_VOICE == 'custom_voice'
        assert voice_mcp_module.TTS_MODEL == 'custom-tts'
        assert voice_mcp_module.STT_MODEL == 'custom-stt'
    
    def test_debug_mode(self):
        """Test debug mode configuration"""
        os.environ['VOICE_MCP_DEBUG'] = 'true'
        
        import importlib
        spec = importlib.util.spec_from_file_location(
            "voice_mcp_script",
            Path(__file__).parent.parent / "src" / "voice_mcp" / "scripts" / "voice-mcp"
        )
        voice_mcp_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(voice_mcp_module)
        
        assert voice_mcp_module.DEBUG == True
        assert voice_mcp_module.DEBUG_DIR.exists()


class TestAudioProcessing:
    """Test audio processing functions"""
    
    @pytest.mark.asyncio
    async def test_audio_file_formats(self, voice_mcp_server, mock_openai_clients):
        """Test handling of different audio formats"""
        # Test MP3 format (default)
        async with Client(voice_mcp_server) as client:
            result = await client.call_tool("speak_text", {"text": "Test MP3"})
            assert "successfully" in result[0].text.lower()
        
        # Verify MP3 was used
        call_args = mock_openai_clients['tts'].audio.speech.create.call_args
        assert call_args[1]['response_format'] == 'mp3'
    
    def test_audio_data_conversion(self):
        """Test audio data type conversions"""
        # Test int16 to float32 conversion
        int_samples = np.array([0, 16383, -16384, 32767, -32768], dtype=np.int16)
        float_samples = int_samples.astype(np.float32) / 32767.0
        
        # Check conversion bounds
        assert float_samples.min() >= -1.0
        assert float_samples.max() <= 1.0
        assert np.allclose(float_samples[0], 0.0)
        assert np.allclose(float_samples[3], 1.0, atol=0.001)


class TestLiveKitIntegration:
    """Test LiveKit transport functionality"""
    
    @pytest.mark.asyncio
    async def test_livekit_availability_check(self, voice_mcp_server):
        """Test LiveKit availability checking"""
        with patch('voice_mcp.scripts.voice-mcp.check_livekit_available', 
                   return_value=asyncio.coroutine(lambda: False)()):
            async with Client(voice_mcp_server) as client:
                # When LiveKit is not available, auto should fall back to local
                result = await client.call_tool(
                    "ask_voice_question",
                    {
                        "question": "Test",
                        "transport": "auto",
                        "duration": 1.0
                    }
                )
                # Should use local transport and succeed
                assert "Test transcription" in result[0].text


class TestDebugFeatures:
    """Test debug mode features"""
    
    @pytest.mark.asyncio
    async def test_debug_file_saving(self, voice_mcp_server, tmp_path):
        """Test that debug files are saved when debug mode is on"""
        os.environ['VOICE_MCP_DEBUG'] = 'true'
        debug_dir = tmp_path / "voice-mcp_recordings"
        debug_dir.mkdir()
        
        with patch('voice_mcp.scripts.voice-mcp.DEBUG_DIR', debug_dir):
            async with Client(voice_mcp_server) as client:
                await client.call_tool("speak_text", {"text": "Debug test"})
                
                # Check if debug files were created
                debug_files = list(debug_dir.glob("*-tts-output.*"))
                assert len(debug_files) > 0


# Integration test
@pytest.mark.asyncio
async def test_full_conversation_flow(voice_mcp_server):
    """Test a complete conversation flow"""
    async with Client(voice_mcp_server) as client:
        # Step 1: Ask a question
        result1 = await client.call_tool(
            "ask_voice_question",
            {
                "question": "What is your favorite color?",
                "transport": "local",
                "duration": 2.0
            }
        )
        assert "Test transcription" in result1[0].text
        
        # Step 2: Speak a response
        result2 = await client.call_tool(
            "speak_text",
            {"text": "That's an interesting choice!"}
        )
        assert "successfully" in result2[0].text.lower()
        
        # Step 3: Check audio devices
        result3 = await client.call_tool("check_audio_devices", {})
        assert "Input Devices" in result3[0].text