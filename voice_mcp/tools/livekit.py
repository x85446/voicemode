"""LiveKit integration tools."""

import logging
from typing import Optional

from voice_mcp.server_new import mcp
from voice_mcp.shared import LIVEKIT_URL, LIVEKIT_API_KEY, LIVEKIT_API_SECRET

logger = logging.getLogger("voice-mcp")


@mcp.tool()
async def check_room_status() -> str:
    """Check LiveKit room status and participants"""
    # This will be implemented - moved from server.py
    return "LiveKit room status check not yet implemented in refactored structure"