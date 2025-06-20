"""
Configuration and shared utilities for Voice MCP Server.

This module contains all configuration constants, global state, initialization functions,
and shared utilities used across the voice-mcp server.
"""

import os
import logging
import asyncio
import subprocess
from pathlib import Path
from typing import Dict, Optional
from datetime import datetime

# ==================== ENVIRONMENT CONFIGURATION ====================

# Debug configuration
DEBUG = os.getenv("VOICE_MCP_DEBUG", "").lower() in ("true", "1", "yes", "on")
TRACE_DEBUG = os.getenv("VOICE_MCP_DEBUG", "").lower() == "trace"
DEBUG_DIR = Path.home() / "voice-mcp_recordings"

# Audio saving configuration
SAVE_AUDIO = os.getenv("VOICE_MCP_SAVE_AUDIO", "").lower() in ("true", "1", "yes", "on")
AUDIO_DIR = Path.home() / "voice-mcp_audio"

# Audio feedback configuration
audio_feedback_raw = os.getenv("VOICE_MCP_AUDIO_FEEDBACK", "chime").lower()

# Backward compatibility: treat "true" as "chime", "false" as "none"
if audio_feedback_raw in ("true", "1", "yes", "on"):
    AUDIO_FEEDBACK_TYPE = "chime"
elif audio_feedback_raw in ("false", "0", "no", "off"):
    AUDIO_FEEDBACK_TYPE = "none"
elif audio_feedback_raw in ("chime", "voice", "both", "none"):
    AUDIO_FEEDBACK_TYPE = audio_feedback_raw
else:
    # Invalid value, default to chime
    AUDIO_FEEDBACK_TYPE = "chime"

# Derived boolean for compatibility
AUDIO_FEEDBACK_ENABLED = AUDIO_FEEDBACK_TYPE != "none"

# Voice feedback specific settings (used when type is "voice" or "both")
AUDIO_FEEDBACK_VOICE = os.getenv("VOICE_MCP_FEEDBACK_VOICE", "nova")
AUDIO_FEEDBACK_MODEL = os.getenv("VOICE_MCP_FEEDBACK_MODEL", "gpt-4o-mini-tts")
AUDIO_FEEDBACK_STYLE = os.getenv("VOICE_MCP_FEEDBACK_STYLE", "whisper")  # "whisper" or "shout"

# Local provider preference configuration
PREFER_LOCAL = os.getenv("VOICE_MCP_PREFER_LOCAL", "true").lower() in ("true", "1", "yes", "on")

# Auto-start configuration
AUTO_START_KOKORO = os.getenv("VOICE_MCP_AUTO_START_KOKORO", "").lower() in ("true", "1", "yes", "on")

# Emotional TTS configuration
ALLOW_EMOTIONS = os.getenv("VOICE_ALLOW_EMOTIONS", "false").lower() in ("true", "1", "yes", "on")
EMOTION_AUTO_UPGRADE = os.getenv("VOICE_EMOTION_AUTO_UPGRADE", "false").lower() in ("true", "1", "yes", "on")

# ==================== SERVICE CONFIGURATION ====================

# OpenAI configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY is required")

# STT (Speech-to-Text) configuration
STT_BASE_URL = os.getenv("STT_BASE_URL", "https://api.openai.com/v1")
STT_MODEL = os.getenv("STT_MODEL", "whisper-1")

# TTS (Text-to-Speech) configuration
TTS_BASE_URL = os.getenv("TTS_BASE_URL", "https://api.openai.com/v1")
TTS_VOICE = os.getenv("TTS_VOICE", "alloy")
TTS_MODEL = os.getenv("TTS_MODEL", "tts-1")

# Provider-specific TTS configuration
OPENAI_TTS_BASE_URL = os.getenv("OPENAI_TTS_BASE_URL", "https://api.openai.com/v1")
KOKORO_TTS_BASE_URL = os.getenv("KOKORO_TTS_BASE_URL", os.getenv("TTS_BASE_URL", "http://localhost:8880/v1"))

# LiveKit configuration
LIVEKIT_URL = os.getenv("LIVEKIT_URL", "ws://localhost:7880")
LIVEKIT_API_KEY = os.getenv("LIVEKIT_API_KEY", "devkey")
LIVEKIT_API_SECRET = os.getenv("LIVEKIT_API_SECRET", "secret")

# ==================== AUDIO CONFIGURATION ====================

# Audio parameters
SAMPLE_RATE = 44100
CHANNELS = 1

# ==================== GLOBAL STATE ====================

# Service management
service_processes: Dict[str, subprocess.Popen] = {}

# Concurrency control for audio operations
# This prevents multiple audio operations from interfering with stdio
audio_operation_lock = asyncio.Lock()

# Flag to track if startup initialization has run
_startup_initialized = False

# ==================== LOGGING CONFIGURATION ====================

def setup_logging() -> logging.Logger:
    """Configure logging for the voice-mcp server.
    
    Returns:
        Logger instance configured for voice-mcp
    """
    log_level = logging.DEBUG if DEBUG else logging.INFO
    logging.basicConfig(
        level=log_level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    logger = logging.getLogger("voice-mcp")
    
    # Trace logging setup
    if TRACE_DEBUG:
        import sys
        trace_file = Path.home() / "voice_mcp_trace.log"
        trace_logger = logging.getLogger("voice-mcp-trace")
        trace_handler = logging.FileHandler(trace_file, mode='a')
        trace_handler.setFormatter(logging.Formatter('%(asctime)s - %(message)s'))
        trace_logger.addHandler(trace_handler)
        trace_logger.setLevel(logging.DEBUG)
        
        def trace_calls(frame, event, arg):
            if event == 'call':
                code = frame.f_code
                if 'voice-mcp' in code.co_filename or 'voice_mcp' in code.co_filename:
                    trace_logger.debug(f"Called {code.co_filename}:{frame.f_lineno} {code.co_name}")
            elif event == 'exception':
                trace_logger.debug(f"Exception: {arg}")
            return trace_calls
        
        sys.settrace(trace_calls)
        logger.info(f"Trace debugging enabled, writing to: {trace_file}")
    
    # Also log to file in debug mode
    if DEBUG:
        debug_log_file = Path.home() / "voice_mcp_debug.log"
        file_handler = logging.FileHandler(debug_log_file, mode='a')
        file_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
        logger.addHandler(file_handler)
        logger.info(f"Debug logging to file: {debug_log_file}")
    
    # Suppress verbose binary data in HTTP logs
    if DEBUG:
        # Keep our debug logs but reduce HTTP client verbosity
        logging.getLogger("openai._base_client").setLevel(logging.INFO)
        logging.getLogger("httpcore").setLevel(logging.INFO)
        logging.getLogger("httpx").setLevel(logging.INFO)
    
    return logger

# ==================== DIRECTORY INITIALIZATION ====================

def initialize_directories():
    """Create necessary directories for debug and audio storage."""
    if DEBUG:
        DEBUG_DIR.mkdir(exist_ok=True)
    
    if SAVE_AUDIO:
        AUDIO_DIR.mkdir(exist_ok=True)

# ==================== UTILITY FUNCTIONS ====================

def get_debug_filename(prefix: str, extension: str) -> str:
    """Generate a timestamped filename for debug files.
    
    Args:
        prefix: Prefix for the filename (e.g., 'stt-input', 'tts-output')
        extension: File extension (e.g., 'wav', 'mp3')
    
    Returns:
        Timestamped filename string
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")[:-3]
    return f"{prefix}_{timestamp}.{extension}"

# ==================== SOUNDDEVICE WORKAROUND ====================

def disable_sounddevice_stderr_redirect():
    """Comprehensively disable sounddevice's stderr redirection.
    
    This prevents sounddevice from redirecting stderr to /dev/null
    which can interfere with audio playback in MCP server context.
    """
    try:
        import sounddevice as sd
        import sys
        import atexit
        
        # Method 1: Override _ignore_stderr in various locations
        if hasattr(sd, '_sounddevice'):
            if hasattr(sd._sounddevice, '_ignore_stderr'):
                sd._sounddevice._ignore_stderr = lambda: None
        if hasattr(sd, '_ignore_stderr'):
            sd._ignore_stderr = lambda: None
        
        # Method 2: Override _check_error if it exists
        if hasattr(sd, '_check'):
            original_check = sd._check
            def safe_check(*args, **kwargs):
                # Prevent any stderr manipulation
                return original_check(*args, **kwargs)
            sd._check = safe_check
        
        # Method 3: Protect file descriptors
        original_stderr = sys.stderr
        
        # Create a hook to prevent stderr replacement
        def protect_stderr():
            if sys.stderr != original_stderr:
                sys.stderr = original_stderr
        
        # Install protection
        atexit.register(protect_stderr)
        
    except Exception as e:
        # Log but continue - audio might still work
        if DEBUG:
            # Can't use logger here as it's not initialized yet
            print(f"DEBUG: Could not fully disable sounddevice stderr redirect: {e}", file=sys.stderr)

# ==================== HTTP CLIENT CONFIGURATION ====================

# HTTP client configuration for OpenAI clients
HTTP_CLIENT_CONFIG = {
    'timeout': {
        'total': 30.0,
        'connect': 5.0
    },
    'limits': {
        'max_keepalive_connections': 5,
        'max_connections': 10
    }
}

# ==================== INITIALIZATION ====================

# Initialize directories on module import
initialize_directories()

# Apply sounddevice workaround on module import
disable_sounddevice_stderr_redirect()

# Set up logger
logger = setup_logging()