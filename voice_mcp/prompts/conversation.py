"""Conversation prompts for voice interactions."""

from voice_mcp.server_new import mcp


@mcp.prompt()
def converse() -> str:
    """Have an ongoing two-way voice conversation with the user."""
    instructions = [
        "Using tools from voice-mcp, have an ongoing two-way conversation",
        "End the chat when the user indicates they want to end it",
        "Keep your utterances brief unless a longer response is requested or necessary",
        "Listen for up to 20 seconds per response",
        "Prefer Kokoro TTS with voice 'af_sky' if available, otherwise use OpenAI with voice 'alloy'"
    ]
    
    return "\n".join(f"- {instruction}" for instruction in instructions)