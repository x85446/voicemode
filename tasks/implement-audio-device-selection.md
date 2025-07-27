# Task: Implement Audio Device Selection for Voice Mode

## Overview
Add the ability to select specific input and output audio devices in voice-mode, allowing users to route audio to different devices (e.g., microphone from one device, speakers from another).

## Background
Currently, voice-mode uses system default audio devices for both input and output. Users cannot specify which devices to use, which limits flexibility in multi-device setups.

## Requirements

### Functional Requirements
1. Allow users to select specific input device for recording (STT)
2. Allow users to select specific output device for playback (TTS)
3. Support device selection by:
   - Device index (e.g., `0`, `1`, `2`)
   - Device name substring (e.g., `"USB microphone"`, `"Bose SoundLink"`)
4. Persist device preferences across sessions
5. Provide tools to list and manage audio devices
6. Handle device disconnection gracefully (fallback to defaults)

### Non-Functional Requirements
1. Maintain backward compatibility (use defaults if not specified)
2. Thread-safe implementation for concurrent audio operations
3. Clear error messages when selected devices are unavailable
4. No performance degradation

## Technical Design

### 1. Configuration Changes

Add new environment variables to `voice_mode/config.py`:

```python
# Audio device configuration
INPUT_DEVICE = os.getenv('VOICEMODE_INPUT_DEVICE', None)  # None means use default
OUTPUT_DEVICE = os.getenv('VOICEMODE_OUTPUT_DEVICE', None)  # None means use default

# Parse device specifications (can be int index or string name)
def parse_device_spec(spec):
    if spec is None:
        return None
    try:
        return int(spec)  # Device index
    except ValueError:
        return spec  # Device name substring
```

### 2. New MCP Tools

Create new tools in `voice_mode/tools/devices.py`:

```python
@mcp.tool()
async def set_audio_devices(
    input_device: Optional[str] = None,
    output_device: Optional[str] = None,
    persist: bool = True
) -> str:
    """Set audio input and/or output devices.
    
    Args:
        input_device: Device index or name substring for input (microphone)
        output_device: Device index or name substring for output (speakers)
        persist: Whether to save settings to config file
        
    Returns:
        Status message with selected devices
    """
    # Implementation details below

@mcp.tool()
async def get_current_audio_devices() -> str:
    """Get currently configured audio devices.
    
    Returns:
        Current input and output device settings
    """
    # Implementation details below

@mcp.tool()
async def test_audio_devices(
    test_input: bool = True,
    test_output: bool = True
) -> str:
    """Test configured audio devices.
    
    Args:
        test_input: Test input device by recording brief sample
        test_output: Test output device by playing test tone
        
    Returns:
        Test results for each device
    """
    # Implementation details below
```

### 3. Core Changes

#### Modify `voice_mode/tools/converse.py`:

```python
def record_audio(duration: float, device=None) -> np.ndarray:
    """Record audio from microphone"""
    # Use configured device or default
    if device is None:
        device = config.INPUT_DEVICE
    
    recording = sd.rec(
        samples_to_record,
        samplerate=SAMPLE_RATE,
        channels=CHANNELS,
        dtype=np.int16,
        device=device  # Add device parameter
    )
    # ... rest of implementation
```

#### Modify `voice_mode/core.py`:

```python
async def text_to_speech(...):
    # In the playback section:
    sd.play(
        samples_with_buffer, 
        audio.frame_rate,
        device=config.OUTPUT_DEVICE  # Add device parameter
    )
```

### 4. Device Management Module

Create `voice_mode/audio_devices.py`:

```python
import sounddevice as sd
import logging
from typing import Optional, Union, Tuple, Dict

logger = logging.getLogger("voicemode")

class AudioDeviceManager:
    """Manages audio device selection and validation."""
    
    def __init__(self):
        self.input_device = None
        self.output_device = None
        
    def set_devices(self, input_device=None, output_device=None):
        """Set audio devices with validation."""
        if input_device is not None:
            self.input_device = self._validate_device(input_device, 'input')
        if output_device is not None:
            self.output_device = self._validate_device(output_device, 'output')
    
    def _validate_device(self, device_spec: Union[int, str], kind: str) -> Optional[int]:
        """Validate and resolve device specification to index."""
        try:
            devices = sd.query_devices()
            
            # If integer, validate it's a valid index
            if isinstance(device_spec, int):
                if 0 <= device_spec < len(devices):
                    device = devices[device_spec]
                    if kind == 'input' and device['max_input_channels'] > 0:
                        return device_spec
                    elif kind == 'output' and device['max_output_channels'] > 0:
                        return device_spec
                raise ValueError(f"Device {device_spec} is not a valid {kind} device")
            
            # If string, search for matching device
            elif isinstance(device_spec, str):
                matches = []
                for idx, device in enumerate(devices):
                    if device_spec.lower() in device['name'].lower():
                        if kind == 'input' and device['max_input_channels'] > 0:
                            matches.append(idx)
                        elif kind == 'output' and device['max_output_channels'] > 0:
                            matches.append(idx)
                
                if len(matches) == 1:
                    return matches[0]
                elif len(matches) > 1:
                    raise ValueError(f"Multiple devices match '{device_spec}': {matches}")
                else:
                    raise ValueError(f"No {kind} device matches '{device_spec}'")
                    
        except Exception as e:
            logger.error(f"Device validation failed: {e}")
            return None
    
    def get_device_info(self) -> Dict[str, Optional[str]]:
        """Get current device information."""
        info = {}
        try:
            devices = sd.query_devices()
            if self.input_device is not None:
                info['input'] = devices[self.input_device]['name']
            else:
                info['input'] = sd.query_devices(kind='input')['name']
                
            if self.output_device is not None:
                info['output'] = devices[self.output_device]['name']
            else:
                info['output'] = sd.query_devices(kind='output')['name']
        except Exception as e:
            logger.error(f"Failed to get device info: {e}")
            info['error'] = str(e)
        
        return info

# Global instance
audio_device_manager = AudioDeviceManager()
```

### 5. Integration Points

1. **Initialization**: Load device settings on startup in `voice_mode/shared.py`
2. **Configuration UI**: Update `update_config` tool to support device settings
3. **Error Handling**: Add device-specific error messages in playback/recording failures
4. **Documentation**: Update README with device selection examples

## Implementation Steps

1. **Phase 1: Core Infrastructure** (2-3 hours)
   - Create `audio_devices.py` module
   - Add configuration variables
   - Implement device validation logic

2. **Phase 2: Modify Audio Operations** (2-3 hours)
   - Update `record_audio()` to accept device parameter
   - Update TTS playback to use output device
   - Add error handling for device failures

3. **Phase 3: MCP Tools** (2-3 hours)
   - Implement `set_audio_devices` tool
   - Implement `get_current_audio_devices` tool
   - Implement `test_audio_devices` tool
   - Update `check_audio_devices` to show current selection

4. **Phase 4: Testing & Polish** (2-3 hours)
   - Test with multiple devices
   - Test device disconnection scenarios
   - Add logging and debugging info
   - Update documentation

## Testing Plan

1. **Unit Tests**:
   - Test device validation with various inputs
   - Test fallback behavior
   - Test error handling

2. **Integration Tests**:
   - Test recording with specific input device
   - Test playback with specific output device
   - Test device switching during operation

3. **Manual Tests**:
   - Test with USB microphone + built-in speakers
   - Test with Bluetooth headphones
   - Test device disconnection during operation
   - Test invalid device specifications

## Example Usage

```bash
# List available devices
/check-audio-devices

# Set specific devices by index
/set-audio-devices input=1 output=3

# Set devices by name
/set-audio-devices input="USB microphone" output="Bose SoundLink"

# Test the devices
/test-audio-devices

# Use in conversation with specific devices
/converse "Hello, can you hear me?" 

# Get current device settings
/get-current-audio-devices
```

## Success Criteria

1. Users can successfully select and use different audio devices
2. Device preferences persist across sessions
3. Clear error messages when devices are unavailable
4. No regression in existing functionality
5. Documentation clearly explains the feature

## Risks & Mitigations

1. **Risk**: Device indices change when devices are plugged/unplugged
   - **Mitigation**: Support device name matching as primary method

2. **Risk**: Thread safety issues with concurrent audio operations
   - **Mitigation**: Use existing `audio_operation_lock`

3. **Risk**: Platform-specific device naming conventions
   - **Mitigation**: Test on macOS, Linux, and Windows (WSL)

## References

- [python-sounddevice documentation](https://python-sounddevice.readthedocs.io/)
- Current implementation in `voice_mode/tools/converse.py`
- Device listing in `voice_mode/tools/devices.py`