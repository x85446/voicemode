"""
CLI entry points for voice-mcp package.
"""

import sys
from .server_new import main as voice_mcp_main


def voice_mcp() -> None:
    """Entry point for voice-mcp command."""
    print("⚠️  DEPRECATION WARNING: 'voice-mcp' command is deprecated.", file=sys.stderr)
    print("⚠️  Please use 'voicemode' instead.", file=sys.stderr)
    print("⚠️  The 'voice-mcp' command will be removed in a future version.\n", file=sys.stderr)
    voice_mcp_main()


def voice_mode() -> None:
    """Entry point for voicemode command."""
    voice_mcp_main()


