"""Voice preferences system for loading user/project voice preferences."""

import os
import logging
from pathlib import Path
from typing import List, Optional

logger = logging.getLogger("voice-mode")

# Cache for loaded preferences
_cached_preferences: Optional[List[str]] = None
_preferences_loaded = False


def find_voices_file() -> Optional[Path]:
    """
    Find the first voices.txt file by walking up the directory tree.
    
    Returns:
        Path to voices.txt file or None if not found
    """
    # Start from current working directory
    current_dir = Path.cwd()
    
    # Walk up directory tree
    while True:
        voices_file = current_dir / ".voicemode" / "voices.txt"
        if voices_file.exists():
            logger.info(f"Found voice preferences at: {voices_file}")
            return voices_file
        
        # Check if we've reached the root
        parent = current_dir.parent
        if parent == current_dir:
            break
        current_dir = parent
    
    # Check user home directory
    home_voices = Path.home() / ".voicemode" / "voices.txt"
    if home_voices.exists():
        logger.info(f"Found voice preferences at: {home_voices}")
        return home_voices
    
    logger.debug("No voice preferences file found")
    return None


def load_voice_preferences() -> List[str]:
    """
    Load voice preferences from voices.txt file.
    
    Returns:
        List of voice names in preference order, or empty list if no file found
    """
    global _cached_preferences, _preferences_loaded
    
    # Return cached preferences if already loaded
    if _preferences_loaded:
        return _cached_preferences or []
    
    _preferences_loaded = True
    
    # Find voices file
    voices_file = find_voices_file()
    if not voices_file:
        _cached_preferences = []
        return []
    
    # Load preferences
    try:
        with open(voices_file, 'r') as f:
            # Read lines, strip whitespace, skip empty lines and comments
            voices = []
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    voices.append(line)
        
        logger.info(f"Loaded {len(voices)} voice preferences: {', '.join(voices)}")
        _cached_preferences = voices
        return voices
        
    except Exception as e:
        logger.error(f"Error loading voice preferences from {voices_file}: {e}")
        _cached_preferences = []
        return []


def get_preferred_voices() -> List[str]:
    """
    Get the list of preferred voices, loading from file if needed.
    
    This is the main API for getting voice preferences.
    
    Returns:
        List of voice names in preference order
    """
    return load_voice_preferences()


def clear_cache():
    """Clear the preferences cache, forcing a reload on next access."""
    global _cached_preferences, _preferences_loaded
    _cached_preferences = None
    _preferences_loaded = False
    logger.debug("Voice preferences cache cleared")