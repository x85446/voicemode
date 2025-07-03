"""Integration tests for voice preferences with provider selection."""

import os
import tempfile
import pytest
from unittest.mock import patch, MagicMock, AsyncMock

from voice_mode.voice_preferences import clear_cache
from voice_mode.providers import select_best_voice, get_tts_client_and_voice


class TestVoicePreferencesIntegration:
    """Test voice preferences integration with provider selection."""
    
    def setup_method(self):
        """Clear cache before each test."""
        clear_cache()
    
    def test_select_best_voice_with_preferences(self, tmp_path):
        """Test that select_best_voice uses preferences."""
        # Create voices file
        voicemode_dir = tmp_path / ".voicemode"
        voicemode_dir.mkdir()
        voices_file = voicemode_dir / "voices.txt"
        voices_file.write_text("shimmer\necho\n")
        
        original_cwd = os.getcwd()
        try:
            os.chdir(tmp_path)
            clear_cache()
            
            # Test with available voices
            available = ["alloy", "nova", "echo", "fable", "onyx", "shimmer"]
            
            # Should select shimmer (first in preferences)
            selected = select_best_voice("openai", available)
            assert selected == "shimmer"
            
            # If shimmer not available, should select echo
            available = ["alloy", "nova", "echo", "fable", "onyx"]
            selected = select_best_voice("openai", available)
            assert selected == "echo"
            
            # If neither available, should fall back to system defaults
            available = ["alloy", "nova"]
            selected = select_best_voice("openai", available)
            assert selected in ["alloy", "nova"]  # Should pick from defaults
            
        finally:
            os.chdir(original_cwd)
    
    def test_preferences_override_system_defaults(self, tmp_path):
        """Test that user preferences take precedence over system defaults."""
        # Create voices file with opposite preference
        voicemode_dir = tmp_path / ".voicemode"
        voicemode_dir.mkdir()
        voices_file = voicemode_dir / "voices.txt"
        # System default is af_sky, but user prefers alloy
        voices_file.write_text("alloy\nnova\n")
        
        original_cwd = os.getcwd()
        try:
            os.chdir(tmp_path)
            clear_cache()
            
            # Mock TTS_VOICES to have af_sky as first choice
            with patch('voice_mode.config.TTS_VOICES', ['af_sky', 'alloy']):
                # Available voices include both
                available = ["af_sky", "alloy", "nova"]
                
                # Should select alloy (user preference) not af_sky (system default)
                selected = select_best_voice("openai", available)
                assert selected == "alloy"
                
        finally:
            os.chdir(original_cwd)
    
    @pytest.mark.asyncio
    async def test_get_tts_client_with_preferences(self, tmp_path):
        """Test that get_tts_client_and_voice uses preferences."""
        # Create voices file
        voicemode_dir = tmp_path / ".voicemode"
        voicemode_dir.mkdir()
        voices_file = voicemode_dir / "voices.txt"
        voices_file.write_text("nova\nshimmer\n")
        
        original_cwd = os.getcwd()
        try:
            os.chdir(tmp_path)
            clear_cache()
            
            # Mock provider registry
            mock_registry = MagicMock()
            mock_endpoint = MagicMock()
            mock_endpoint.healthy = True
            mock_endpoint.voices = ["alloy", "nova", "echo", "shimmer"]
            mock_endpoint.models = ["tts-1"]
            mock_endpoint.provider_type = "openai"
            mock_endpoint.base_url = "https://api.openai.com/v1"
            
            mock_registry.registry = {
                "tts": {
                    "https://api.openai.com/v1": mock_endpoint
                }
            }
            mock_registry.initialize = AsyncMock()
            
            with patch('voice_mode.providers.provider_registry', mock_registry):
                with patch('voice_mode.config.TTS_BASE_URLS', ["https://api.openai.com/v1"]):
                    with patch('voice_mode.config.TTS_VOICES', ["alloy", "echo"]):
                        # Get client without specifying voice
                        client, voice, model, endpoint = await get_tts_client_and_voice()
                        
                        # Should select nova (first user preference that's available)
                        assert voice == "nova"
                        
        finally:
            os.chdir(original_cwd)