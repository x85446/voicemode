#!/usr/bin/env python3
"""Minimal MCP server to test stdio persistence"""
import logging
from fastmcp import FastMCP

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

mcp = FastMCP("Test Server")

@mcp.tool()
async def test_tool(message: str) -> str:
    """Test tool that just echoes back"""
    logger.info(f"Received: {message}")
    return f"Echo: {message}"

if __name__ == "__main__":
    logger.info("Starting minimal test server...")
    mcp.run()