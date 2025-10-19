"""Audio diagnostics utilities for better error handling."""

import subprocess
import platform
import os
import logging
from typing import Dict, List, Tuple, Optional

try:
    import sounddevice as sd
except ImportError:
    sd = None

logger = logging.getLogger("voice-mode")


def check_system_audio_packages() -> Dict[str, bool]:
    """Check if required system audio packages are installed.
    
    Returns:
        Dict mapping package names to installation status
    """
    system = platform.system()
    
    if system != "Linux":
        return {}
    
    # Check if we're in WSL
    is_wsl = False
    if os.path.exists("/proc/version"):
        with open("/proc/version", "r") as f:
            is_wsl = "microsoft" in f.read().lower() or "wsl" in f.read().lower()
    
    # Required packages for Ubuntu/Debian
    packages = {
        "libasound2-dev": "ALSA development files",
        "libasound2-plugins": "ALSA plugins for PulseAudio", 
        "libportaudio2": "PortAudio library",
        "portaudio19-dev": "PortAudio development files",
    }
    
    # Additional packages for WSL
    if is_wsl:
        packages.update({
            "pulseaudio": "PulseAudio sound server (required for WSL)",
            "pulseaudio-utils": "PulseAudio utilities",
        })
    
    installed = {}
    for pkg in packages:
        try:
            result = subprocess.run(
                ["dpkg", "-l", pkg], 
                capture_output=True, 
                text=True,
                check=False
            )
            installed[pkg] = result.returncode == 0 and "ii" in result.stdout
        except Exception:
            installed[pkg] = False
    
    return installed


def get_audio_error_help(error: Exception) -> str:
    """Get helpful error message for audio-related errors.
    
    Args:
        error: The exception that occurred
        
    Returns:
        Helpful error message with suggestions
    """
    error_str = str(error).lower()
    suggestions = []
    
    # Check for common sounddevice/PortAudio errors
    if "portaudio" in error_str or "error querying device" in error_str:
        suggestions.append("Audio system initialization failed. This usually means missing system packages.")
        
        # Check installed packages
        packages = check_system_audio_packages()
        missing = [pkg for pkg, installed in packages.items() if not installed]
        
        if missing:
            suggestions.append(f"\nMissing packages detected: {', '.join(missing)}")
            suggestions.append("\nTo install missing packages on Ubuntu/Debian/WSL:")
            suggestions.append(f"  sudo apt update && sudo apt install -y {' '.join(missing)}")
        
        # WSL-specific suggestions
        if os.path.exists("/proc/version"):
            with open("/proc/version", "r") as f:
                if "microsoft" in f.read().lower() or "wsl" in f.read().lower():
                    suggestions.append("\nWSL detected. Additional steps may be required:")
                    suggestions.append("  1. Ensure PulseAudio is running: pulseaudio --start")
                    suggestions.append("  2. Check Windows microphone permissions")
                    suggestions.append("  3. See: docs/troubleshooting/wsl2-microphone-access.md")
    
    elif "no audio devices" in error_str or "device unavailable" in error_str:
        suggestions.append("No audio input devices found.")
        suggestions.append("\nPossible solutions:")
        suggestions.append("  1. Check microphone is connected and enabled")
        suggestions.append("  2. Check system audio settings")
        suggestions.append("  3. On WSL: Ensure Windows allows microphone access to apps")
        suggestions.append("  4. Try using LiveKit transport instead of local microphone")
    
    elif "permission" in error_str:
        suggestions.append("Permission denied accessing audio device.")
        suggestions.append("\nPossible solutions:")
        suggestions.append("  1. Check user is in 'audio' group: sudo usermod -a -G audio $USER")
        suggestions.append("  2. Log out and back in for group changes to take effect")
        suggestions.append("  3. Check device permissions: ls -la /dev/snd/")
    
    else:
        # Generic audio error
        suggestions.append(f"Audio error: {error}")
        suggestions.append("\nFor diagnostics, run:")
        suggestions.append("  python scripts/diagnose-wsl-audio.py")
    
    return "\n".join(suggestions)


def check_pulseaudio_status() -> Tuple[bool, str]:
    """Check if PulseAudio is running and accessible.
    
    Returns:
        Tuple of (is_running, status_message)
    """
    try:
        result = subprocess.run(
            ["pactl", "info"],
            capture_output=True,
            text=True,
            check=False
        )
        if result.returncode == 0:
            return True, "PulseAudio is running and accessible"
        else:
            return False, f"PulseAudio check failed: {result.stderr}"
    except FileNotFoundError:
        return False, "PulseAudio utils not installed (pactl command not found)"
    except Exception as e:
        return False, f"Error checking PulseAudio: {e}"


def get_device_by_identifier(identifier, device_type: str) -> Optional[int]:
    """Find audio device by name (partial match) or index.

    Args:
        identifier: Device name (string, partial match supported) or device index (int or string)
        device_type: 'input' or 'output'

    Returns:
        Device index if found, None otherwise
    """
    if identifier is None or identifier == '':
        return None

    if sd is None:
        logger.error("sounddevice module not available")
        return None

    try:
        devices = sd.query_devices()
    except Exception as e:
        logger.error(f"Error querying audio devices: {e}")
        return None

    # Determine which channel count to check based on device_type
    channel_key = 'max_input_channels' if device_type == 'input' else 'max_output_channels'

    # Try to parse as integer index first, but only if it's a reasonable device index
    # This allows numeric strings like "410" in "Jabra SPEAK 410" to be treated as names
    is_numeric = False
    try:
        device_index = int(identifier)
        is_numeric = True

        # Only treat as index if it's in valid range (0 to num_devices-1)
        if 0 <= device_index < len(devices):
            # Validate device has the right capabilities
            if devices[device_index][channel_key] > 0:
                return device_index
            else:
                logger.warning(f"Device {device_index} ({devices[device_index]['name']}) "
                              f"does not support {device_type}")
                return None
        # If numeric but out of range, fall through to name matching
        # This handles cases like "410" which should match "Jabra SPEAK 410 USB"
    except ValueError:
        # Not an integer, treat as device name
        pass

    # Search by name (case-insensitive partial match)
    identifier_lower = str(identifier).lower()
    matches = []

    for idx, device in enumerate(devices):
        device_name = device['name'].lower()
        # Check if identifier is in device name (partial match)
        if identifier_lower in device_name:
            # Check if device has the right capabilities
            if device[channel_key] > 0:
                matches.append((idx, device['name']))

    if len(matches) == 0:
        # Log appropriate message based on whether it was numeric or not
        if is_numeric:
            logger.warning(f"Device index {identifier} out of range (0-{len(devices)-1}) "
                          f"and no device name matching '{identifier}' found")
        else:
            logger.warning(f"No {device_type} device found matching '{identifier}'")
        return None

    if len(matches) > 1:
        logger.info(f"Found {len(matches)} devices matching '{identifier}': "
                   f"{', '.join([f'{idx}:{name}' for idx, name in matches])}")
        logger.info(f"Using first match: {matches[0][0]} ({matches[0][1]})")

    return matches[0][0]


def diagnose_audio_setup() -> List[str]:
    """Run basic audio diagnostics and return list of findings.

    Returns:
        List of diagnostic messages
    """
    findings = []

    # Check platform
    system = platform.system()
    findings.append(f"Platform: {system}")

    # Check if WSL
    if system == "Linux" and os.path.exists("/proc/version"):
        with open("/proc/version", "r") as f:
            if "microsoft" in f.read().lower() or "wsl" in f.read().lower():
                findings.append("Environment: WSL detected")

    # Check packages on Linux
    if system == "Linux":
        packages = check_system_audio_packages()
        missing = [pkg for pkg, installed in packages.items() if not installed]
        if missing:
            findings.append(f"Missing packages: {', '.join(missing)}")
        else:
            findings.append("All required packages installed")

        # Check PulseAudio
        pa_running, pa_status = check_pulseaudio_status()
        findings.append(f"PulseAudio: {pa_status}")

    # Check Python audio
    try:
        import sounddevice as sd
        devices = sd.query_devices()
        input_count = sum(1 for d in devices if d['max_input_channels'] > 0)
        findings.append(f"Audio devices: {len(devices)} total, {input_count} input devices")
    except Exception as e:
        findings.append(f"sounddevice error: {e}")

    return findings