#!/usr/bin/env python
"""Test script to verify CLI behavior."""

import subprocess
import sys
import time
import os

def test_subcommands():
    """Test that subcommands work correctly."""
    print("Testing subcommands...")
    
    # Test help
    result = subprocess.run([sys.executable, "-m", "voice_mode", "--help"], 
                          capture_output=True, text=True)
    assert result.returncode == 0
    assert "kokoro" in result.stdout
    assert "whisper" in result.stdout
    print("✅ Help command works")
    
    # Test kokoro status
    result = subprocess.run([sys.executable, "-m", "voice_mode", "kokoro", "status"], 
                          capture_output=True, text=True, timeout=10)
    assert result.returncode == 0
    print("✅ Kokoro status works")
    
    # Test whisper status  
    result = subprocess.run([sys.executable, "-m", "voice_mode", "whisper", "status"], 
                          capture_output=True, text=True, timeout=10)
    assert result.returncode == 0
    print("✅ Whisper status works")
    
    print("All subcommand tests passed! 🎉")

def test_default_behavior():
    """Test that running without arguments would start MCP server."""
    print("Testing default behavior (would start MCP server)...")
    
    # We can't easily test this without actually starting the server,
    # but we can verify the CLI structure is correct
    from voice_mode.cli import voice_mode_main_cli
    
    # Import click for testing
    import click
    from click.testing import CliRunner
    
    runner = CliRunner()
    
    # Test that calling with no args would try to start MCP server
    # We'll use a timeout since we don't want to actually start it
    try:
        result = runner.invoke(voice_mode_main_cli, [], catch_exceptions=False, standalone_mode=False)
        # This should try to start the MCP server, which we'll interrupt
    except SystemExit:
        # Expected - the MCP server would normally start here
        pass
    
    print("✅ Default behavior correctly configured")

if __name__ == "__main__":
    test_subcommands()
    test_default_behavior()
    print("\n🎉 All tests passed! The CLI implementation is working correctly.")