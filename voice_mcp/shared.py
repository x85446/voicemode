"""Shared configuration and initialization for voice-mcp."""

import asyncio
import logging
import os
import subprocess
import sys
from pathlib import Path
from typing import Dict, Optional

import httpx
import sounddevice as sd

# Get logger
logger = logging.getLogger("voice-mcp")

# Debug configuration
DEBUG = os.getenv("VOICE_MCP_DEBUG", "").lower() in ("true", "1", "yes", "on")
DEBUG_DIR = Path.home() / "voice-mcp_recordings"
SAVE_AUDIO = os.getenv("VOICE_MCP_SAVE_AUDIO", "").lower() in ("true", "1", "yes", "on")
AUDIO_DIR = Path.home() / "voice-mcp_audio"

if DEBUG:
    DEBUG_DIR.mkdir(exist_ok=True)

if SAVE_AUDIO:
    AUDIO_DIR.mkdir(exist_ok=True)

# Audio feedback configuration
AUDIO_FEEDBACK_ENABLED = os.getenv("VOICE_MCP_AUDIO_FEEDBACK", "true").lower() in ("true", "1", "yes", "on")
AUDIO_FEEDBACK_VOICE = os.getenv("VOICE_MCP_FEEDBACK_VOICE", "nova")
AUDIO_FEEDBACK_MODEL = os.getenv("VOICE_MCP_FEEDBACK_MODEL", "gpt-4o-mini-tts")
AUDIO_FEEDBACK_STYLE = os.getenv("VOICE_MCP_FEEDBACK_STYLE", "whisper")  # "whisper" or "shout"

# Service configuration
STT_BASE_URL = os.getenv("STT_BASE_URL", "https://api.openai.com/v1")
TTS_BASE_URL = os.getenv("TTS_BASE_URL", "https://api.openai.com/v1")
TTS_VOICE = os.getenv("TTS_VOICE", "alloy")
TTS_MODEL = os.getenv("TTS_MODEL", "tts-1")
STT_MODEL = os.getenv("STT_MODEL", "whisper-1")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Provider-specific TTS configuration
OPENAI_TTS_BASE_URL = os.getenv("OPENAI_TTS_BASE_URL", "https://api.openai.com/v1")
KOKORO_TTS_BASE_URL = os.getenv("KOKORO_TTS_BASE_URL", os.getenv("TTS_BASE_URL", "http://localhost:8880/v1"))

# LiveKit configuration
LIVEKIT_URL = os.getenv("LIVEKIT_URL", "ws://localhost:7880")
LIVEKIT_API_KEY = os.getenv("LIVEKIT_API_KEY", "devkey")
LIVEKIT_API_SECRET = os.getenv("LIVEKIT_API_SECRET", "secret")

# Auto-start configuration
AUTO_START_KOKORO = os.getenv("VOICE_MCP_AUTO_START_KOKORO", "").lower() in ("true", "1", "yes", "on")

# Emotional TTS configuration
ALLOW_EMOTIONS = os.getenv("VOICE_ALLOW_EMOTIONS", "false").lower() in ("true", "1", "yes", "on")
EMOTION_AUTO_UPGRADE = os.getenv("VOICE_EMOTION_AUTO_UPGRADE", "false").lower() in ("true", "1", "yes", "on")

# Local provider preference configuration
PREFER_LOCAL = os.getenv("VOICE_MCP_PREFER_LOCAL", "true").lower() in ("true", "1", "yes", "on")

# Audio configuration
SAMPLE_RATE = 44100
CHANNELS = 1

# Concurrency control for audio operations
# This prevents multiple audio operations from interfering with stdio
audio_operation_lock = asyncio.Lock()

# Track service processes
service_processes: Dict[str, subprocess.Popen] = {}

# Track if startup has been initialized
_startup_initialized = False


def disable_sounddevice_stderr_redirect():
    """Comprehensively disable sounddevice's stderr redirection"""
    try:
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
        import sys
        original_stderr = sys.stderr
        
        # Create a hook to prevent stderr replacement
        def protect_stderr():
            if sys.stderr != original_stderr:
                sys.stderr = original_stderr
        
        # Install protection
        import atexit
        atexit.register(protect_stderr)
        
    except Exception as e:
        # Log but continue - audio might still work
        if DEBUG:
            # Can't use logger here as it's not initialized yet
            print(f"DEBUG: Could not fully disable sounddevice stderr redirect: {e}", file=sys.stderr)


# Apply sounddevice workaround
disable_sounddevice_stderr_redirect()


async def startup_initialization():
    """Initialize services on startup based on configuration"""
    global _startup_initialized
    
    if _startup_initialized:
        return
    
    _startup_initialized = True
    logger.info("Running startup initialization...")
    
    # Check if we should auto-start Kokoro
    if AUTO_START_KOKORO:
        try:
            # Check if Kokoro is already running
            async with httpx.AsyncClient(timeout=3.0) as client:
                base_url = KOKORO_TTS_BASE_URL.rstrip('/').removesuffix('/v1')
                health_url = f"{base_url}/health"
                response = await client.get(health_url)
                
                if response.status_code == 200:
                    logger.info("Kokoro TTS is already running externally")
                else:
                    raise Exception("Not running")
        except:
            # Kokoro is not running, start it
            logger.info("Auto-starting Kokoro TTS service...")
            try:
                global service_processes
                if "kokoro" not in service_processes:
                    process = subprocess.Popen(
                        ["uvx", "kokoro-fastapi"],
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                        text=True,
                        env={**os.environ}
                    )
                    service_processes["kokoro"] = process
                    
                    # Wait a moment for it to start
                    await asyncio.sleep(2.0)
                    
                    # Verify it started
                    if process.poll() is None:
                        logger.info(f"✓ Kokoro TTS started successfully (PID: {process.pid})")
                    else:
                        logger.error("Failed to start Kokoro TTS")
            except Exception as e:
                logger.error(f"Error auto-starting Kokoro: {e}")
    
    # Log initial status
    logger.info("Service initialization complete")


def cleanup_on_shutdown():
    """Cleanup function called on shutdown"""
    from voice_mcp.core import cleanup as cleanup_clients
    
    # Cleanup OpenAI clients
    cleanup_clients()
    
    # Stop any services we started
    for name, process in service_processes.items():
        if process and process.poll() is None:
            logger.info(f"Stopping {name} service (PID: {process.pid})...")
            process.terminate()
            try:
                process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                process.kill()
                process.wait()
            logger.info(f"✓ {name} service stopped")