"""Status check prompts for voice services."""

from voice_mcp.server_new import mcp


@mcp.prompt(name="voice-status")
def voice_status() -> str:
    """Check the comprehensive status of all voice services.
    
    This prompt instructs the assistant to check the status of all voice infrastructure
    including TTS, STT, LiveKit, audio devices, and provider availability.
    
    Returns:
        Instructions for checking comprehensive voice status
    """
    return "Use the voice_status tool to check the status of all voice services. This will show TTS/STT providers, LiveKit status, audio devices, and recommendations for optimal configuration."