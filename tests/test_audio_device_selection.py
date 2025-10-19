"""Test audio device selection functionality."""

import os
import pytest
from unittest.mock import Mock, patch, MagicMock
from voice_mode.utils.audio_diagnostics import get_device_by_identifier


class TestDeviceSelection:
    """Test device selection by name and index."""

    @pytest.fixture
    def mock_devices(self):
        """Mock sounddevice query_devices output with real Mac device data."""
        return [
            {'name': 'DELL U3415W', 'max_input_channels': 0, 'max_output_channels': 2},
            {'name': 'LG UltraFine Display Audio', 'max_input_channels': 1, 'max_output_channels': 0},
            {'name': 'LG UltraFine Display Audio', 'max_input_channels': 0, 'max_output_channels': 2},
            {'name': 'Schiit Hel', 'max_input_channels': 0, 'max_output_channels': 2},
            {'name': 'Schiit Hel', 'max_input_channels': 2, 'max_output_channels': 0},
            {'name': 'Jabra SPEAK 410 USB', 'max_input_channels': 0, 'max_output_channels': 2},
            {'name': 'Jabra SPEAK 410 USB', 'max_input_channels': 1, 'max_output_channels': 0},
            {'name': 'Unknown USB Audio Device', 'max_input_channels': 2, 'max_output_channels': 0},
            {'name': 'Background Music', 'max_input_channels': 2, 'max_output_channels': 2},
            {'name': 'Background Music (UI Sounds)', 'max_input_channels': 2, 'max_output_channels': 2},
            {'name': 'BlackHole 2ch', 'max_input_channels': 2, 'max_output_channels': 2},
            {'name': 'Mac mini Speakers', 'max_input_channels': 0, 'max_output_channels': 2},
            {'name': 'Microsoft Teams Audio', 'max_input_channels': 1, 'max_output_channels': 1},
            {'name': 'logi+bh', 'max_input_channels': 2, 'max_output_channels': 2},
            {'name': 'schit+bh', 'max_input_channels': 0, 'max_output_channels': 2},
        ]

    def test_device_by_exact_name(self, mock_devices):
        """Test finding device by exact name match."""
        with patch('sounddevice.query_devices', return_value=mock_devices):
            # Find exact match with real Mac device names
            result = get_device_by_identifier('Jabra SPEAK 410 USB', 'input')
            assert result == 6  # Device 6 is Jabra input

            result = get_device_by_identifier('Jabra SPEAK 410 USB', 'output')
            assert result == 5  # Device 5 is Jabra output

    def test_device_by_partial_name(self, mock_devices):
        """Test finding device by partial name match - this is the key test case."""
        with patch('sounddevice.query_devices', return_value=mock_devices):
            # Find by partial match - should return first match
            result = get_device_by_identifier('Jabra', 'input')
            assert result == 6  # First Jabra input device

            result = get_device_by_identifier('Jabra', 'output')
            assert result == 5  # First Jabra output device

            # Test 'Jabra Speak' partial match
            result = get_device_by_identifier('Jabra Speak', 'input')
            assert result == 6  # Matches "Jabra SPEAK 410 USB"

            result = get_device_by_identifier('Jabra Speak', 'output')
            assert result == 5  # Matches "Jabra SPEAK 410 USB"

            # More specific partial match
            result = get_device_by_identifier('410', 'input')
            assert result == 6

            result = get_device_by_identifier('410', 'output')
            assert result == 5

    def test_device_by_index_string(self, mock_devices):
        """Test finding device by index as string."""
        with patch('sounddevice.query_devices', return_value=mock_devices):
            # Valid index for input
            result = get_device_by_identifier('6', 'input')
            assert result == 6

            # Valid index for output
            result = get_device_by_identifier('5', 'output')
            assert result == 5

            # Invalid type for index (device 0 has no input channels)
            result = get_device_by_identifier('0', 'input')
            assert result is None

    def test_device_by_index_int(self, mock_devices):
        """Test finding device by index as integer."""
        with patch('sounddevice.query_devices', return_value=mock_devices):
            result = get_device_by_identifier(6, 'input')
            assert result == 6

            result = get_device_by_identifier(5, 'output')
            assert result == 5

    def test_multiple_matches(self, mock_devices):
        """Test handling multiple matching devices."""
        # Add a second device with input channels that matches "Background"
        # Background Music and Background Music (UI Sounds) both have input channels
        with patch('sounddevice.query_devices', return_value=mock_devices):
            with patch('voice_mode.utils.audio_diagnostics.logger') as mock_logger:
                # "Background" matches both device 8 and 9, both have input channels
                result = get_device_by_identifier('Background', 'input')
                assert result == 8  # First match

                # Check that info was logged about multiple matches
                info_calls = [call for call in mock_logger.info.call_args_list
                                if 'Found' in str(call) or 'Background' in str(call)]
                assert len(info_calls) > 0

    def test_no_match(self, mock_devices):
        """Test when no device matches."""
        with patch('sounddevice.query_devices', return_value=mock_devices):
            result = get_device_by_identifier('NonExistent', 'input')
            assert result is None

            result = get_device_by_identifier('999', 'input')
            assert result is None

    def test_case_insensitive(self, mock_devices):
        """Test case-insensitive matching."""
        with patch('sounddevice.query_devices', return_value=mock_devices):
            result = get_device_by_identifier('jabra', 'input')
            assert result == 6

            result = get_device_by_identifier('JABRA', 'input')
            assert result == 6

            result = get_device_by_identifier('schiit hel', 'input')
            assert result == 4

    def test_system_default_handling(self, mock_devices):
        """Test that SYSTEM_DEFAULT is NOT passed to get_device_by_identifier.

        This is a regression test for the bug where SYSTEM_DEFAULT was being
        passed to get_device_by_identifier, causing it to search for a device
        named 'SYSTEM_DEFAULT' which doesn't exist.

        The fix ensures that converse.py and core.py check for SYSTEM_DEFAULT
        before calling this function.
        """
        with patch('sounddevice.query_devices', return_value=mock_devices):
            # SYSTEM_DEFAULT should NOT be passed to this function
            # If it is, it will fail to find a match
            result = get_device_by_identifier('SYSTEM_DEFAULT', 'input')
            assert result is None  # No device named "SYSTEM_DEFAULT" exists

            result = get_device_by_identifier('System_Default', 'input')
            assert result is None

            # The calling code should check for SYSTEM_DEFAULT and skip lookup entirely

    def test_empty_identifier(self, mock_devices):
        """Test with empty or None identifier."""
        with patch('sounddevice.query_devices', return_value=mock_devices):
            result = get_device_by_identifier('', 'input')
            assert result is None

            result = get_device_by_identifier(None, 'input')
            assert result is None

    def test_out_of_range_index(self, mock_devices):
        """Test with out of range device index."""
        with patch('sounddevice.query_devices', return_value=mock_devices):
            result = get_device_by_identifier('100', 'input')
            assert result is None

            result = get_device_by_identifier(-1, 'input')
            assert result is None


class TestRecordingWithDevice:
    """Test recording functions with device selection."""

    def test_record_audio_with_device(self):
        """Test record_audio sets the correct device."""
        import numpy as np
        import importlib

        mock_devices = [
            {'name': 'Built-in Microphone', 'max_input_channels': 2, 'max_output_channels': 0},
            {'name': 'Jabra SPEAK 410 USB', 'max_input_channels': 1, 'max_output_channels': 0},
        ]

        # Patch environment and reload config to pick up INPUT_DEVICE
        with patch.dict('os.environ', {'VOICEMODE_INPUT_DEVICE': 'Jabra'}):
            # Reload config module to pick up the environment variable
            import voice_mode.config as config_module
            importlib.reload(config_module)

            # Import converse module first so we can patch sd.default within it
            from voice_mode.tools import converse

            # Create a simple object to track device changes
            # We need to track attribute assignment, not just value changes
            class DeviceTracker:
                def __init__(self):
                    self._device = [0, 0]
                    self.assignments = []  # Track all device assignments

                @property
                def device(self):
                    return self._device

                @device.setter
                def device(self, value):
                    self.assignments.append(list(value) if hasattr(value, '__iter__') else value)
                    self._device = value

            device_tracker = DeviceTracker()

            # Patch sd.default directly in the converse module where it's already imported
            # Also patch sd.query_devices in audio_diagnostics
            with patch.object(converse.sd, 'default', device_tracker):
                with patch('voice_mode.utils.audio_diagnostics.sd.query_devices', return_value=mock_devices):
                    with patch.object(converse.sd, 'rec', return_value=np.zeros((24000, 1), dtype=np.int16)):
                        with patch.object(converse.sd, 'wait'):
                            # Mock SAMPLE_RATE and CHANNELS constants
                            with patch.object(converse, 'SAMPLE_RATE', 24000):
                                with patch.object(converse, 'CHANNELS', 1):
                                    with patch.object(converse, 'DEBUG', False):
                                        # This should set device to index 1 (Jabra)
                                        result = converse.record_audio(1.0)

                                        # Check that device was set to Jabra (index 1) at some point
                                        # The function temporarily sets the device, then restores it
                                        assert [1, 0] in device_tracker.assignments, \
                                            f"Expected [1, 0] in assignments, got {device_tracker.assignments}"

                                        # Verify result is a numpy array
                                        assert isinstance(result, np.ndarray)


class TestPlaybackWithDevice:
    """Test playback functions with device selection."""

    @pytest.fixture
    def mock_config(self):
        """Mock configuration values."""
        with patch('voice_mode.config.OUTPUT_DEVICE', 'Jabra'):
            yield

    def test_tts_playback_with_device(self, mock_config):
        """Test TTS playback sets the correct output device."""
        # This would require more complex mocking of the text_to_speech function
        # For now, we test that the configuration is accessible
        from voice_mode.config import OUTPUT_DEVICE

        with patch.dict('os.environ', {'VOICEMODE_OUTPUT_DEVICE': 'Jabra SPEAK 410'}):
            from voice_mode.config import OUTPUT_DEVICE
            # Note: This would need to reload the config module to pick up the env var
            # In practice, the device selection will work when the module is loaded fresh


class TestConfigIntegration:
    """Test integration with configuration system."""

    def test_config_environment_variables(self):
        """Test that environment variables are properly read."""
        with patch.dict('os.environ', {
            'VOICEMODE_INPUT_DEVICE': 'Jabra',
            'VOICEMODE_OUTPUT_DEVICE': 'Speakers'
        }):
            # Force reload of config module
            import importlib
            import voice_mode.config as config_module
            importlib.reload(config_module)

            assert config_module.INPUT_DEVICE == 'Jabra'
            assert config_module.OUTPUT_DEVICE == 'Speakers'

    def test_config_strips_double_quotes(self):
        """Test that double quotes are stripped from device names."""
        with patch.dict('os.environ', {
            'VOICEMODE_INPUT_DEVICE': '"Jabra"',
            'VOICEMODE_OUTPUT_DEVICE': '"Jabra SPEAK 410 USB"'
        }):
            # Force reload of config module
            import importlib
            import voice_mode.config as config_module
            importlib.reload(config_module)

            assert config_module.INPUT_DEVICE == 'Jabra'
            assert config_module.OUTPUT_DEVICE == 'Jabra SPEAK 410 USB'

    def test_config_strips_single_quotes(self):
        """Test that single quotes are stripped from device names."""
        with patch.dict('os.environ', {
            'VOICEMODE_INPUT_DEVICE': "'Jabra'",
            'VOICEMODE_OUTPUT_DEVICE': "'Jabra SPEAK 410 USB'"
        }):
            # Force reload of config module
            import importlib
            import voice_mode.config as config_module
            importlib.reload(config_module)

            assert config_module.INPUT_DEVICE == 'Jabra'
            assert config_module.OUTPUT_DEVICE == 'Jabra SPEAK 410 USB'

    def test_config_handles_no_quotes(self):
        """Test that device names without quotes are handled correctly."""
        with patch.dict('os.environ', {
            'VOICEMODE_INPUT_DEVICE': 'Jabra',
            'VOICEMODE_OUTPUT_DEVICE': 'Jabra SPEAK 410 USB'
        }):
            # Force reload of config module
            import importlib
            import voice_mode.config as config_module
            importlib.reload(config_module)

            assert config_module.INPUT_DEVICE == 'Jabra'
            assert config_module.OUTPUT_DEVICE == 'Jabra SPEAK 410 USB'

    def test_config_handles_mismatched_quotes(self):
        """Test that mismatched quotes are NOT stripped (invalid syntax)."""
        with patch.dict('os.environ', {
            'VOICEMODE_INPUT_DEVICE': '"Jabra\'',
            'VOICEMODE_OUTPUT_DEVICE': '\'Jabra"'
        }):
            # Force reload of config module
            import importlib
            import voice_mode.config as config_module
            importlib.reload(config_module)

            # Mismatched quotes should not be stripped
            assert config_module.INPUT_DEVICE == '"Jabra\''
            assert config_module.OUTPUT_DEVICE == '\'Jabra"'