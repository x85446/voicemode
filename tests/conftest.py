"""Shared test fixtures and configuration for VoiceMode tests."""

import os
import sys
import tempfile
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock
import pytest
import pytest_asyncio

# Add voice_mode to path for testing
sys.path.insert(0, str(Path(__file__).parent.parent))


@pytest.fixture
def temp_dir():
    """Create a temporary directory for test files."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)


@pytest.fixture
def mock_mcp():
    """Create a mock FastMCP instance for testing tools."""
    from fastmcp import FastMCP
    mcp = MagicMock(spec=FastMCP)
    mcp.tool = MagicMock()
    
    # Make the decorator work properly
    def tool_decorator(**kwargs):
        def decorator(func):
            func._mcp_tool_config = kwargs
            return func
        return decorator
    
    mcp.tool.side_effect = tool_decorator
    return mcp


@pytest.fixture
def mock_subprocess(monkeypatch):
    """Mock subprocess calls."""
    import subprocess
    mock = MagicMock()
    mock.Popen = MagicMock()
    mock.run = MagicMock()
    mock.DEVNULL = subprocess.DEVNULL
    mock.PIPE = subprocess.PIPE
    monkeypatch.setattr("subprocess.Popen", mock.Popen)
    monkeypatch.setattr("subprocess.run", mock.run)
    return mock
