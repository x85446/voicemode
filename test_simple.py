#!/usr/bin/env python
"""Simple test to verify CLI structure."""

import sys

def main():
    print("Testing CLI structure...")
    
    # Test that we can import the CLI
    from voice_mode.cli import voice_mode_main_cli
    print("✅ CLI imports successfully")
    
    # Test that the CLI has the expected structure
    commands = voice_mode_main_cli.commands
    assert 'kokoro' in commands, "Kokoro command group missing"
    assert 'whisper' in commands, "Whisper command group missing"
    print("✅ Command groups present")
    
    # Test kokoro subcommands
    kokoro_commands = commands['kokoro'].commands
    expected_kokoro = ['status', 'start', 'stop', 'restart', 'enable', 'disable', 'logs', 'update-service-files', 'health']
    for cmd in expected_kokoro:
        assert cmd in kokoro_commands, f"Kokoro {cmd} command missing"
    print("✅ Kokoro commands present")
    
    # Test whisper subcommands
    whisper_commands = commands['whisper'].commands
    expected_whisper = ['status', 'start', 'stop', 'restart', 'enable', 'disable', 'logs', 'update-service-files', 'health']
    for cmd in expected_whisper:
        assert cmd in whisper_commands, f"Whisper {cmd} command missing"
    print("✅ Whisper commands present")
    
    print("\n🎉 CLI structure is correct!")
    print("Available commands:")
    print("  voice-mode                    # Starts MCP server")
    print("  voice-mode kokoro status      # Check Kokoro status")
    print("  voice-mode kokoro start       # Start Kokoro")
    print("  voice-mode whisper status     # Check Whisper status")
    print("  voice-mode whisper start      # Start Whisper")
    print("  ... and more!")

if __name__ == "__main__":
    main()