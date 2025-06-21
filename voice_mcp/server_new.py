#!/usr/bin/env python
"""VoiceMode MCP Server - Modular version using FastMCP patterns."""

from fastmcp import FastMCP

# Create FastMCP instance
mcp = FastMCP("voicemode")

# Import shared configuration and utilities
from . import config

# Auto-import all tools, prompts, and resources
# The __init__.py files in each directory handle the imports
from . import tools
from . import prompts 
from . import resources

# Main entry point
def main():
    """Run the VoiceMode MCP server."""
    from .config import setup_logging
    
    # Set up logging
    setup_logging()
    
    # Run the server
    mcp.run(transport="stdio")

if __name__ == "__main__":
    main()