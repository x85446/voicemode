"""
Hook commands for Voice Mode - primarily for Claude Code integration.
"""

import click
import sys
import json
import os
from pathlib import Path


@click.group()
@click.help_option('-h', '--help', help='Show this message and exit')
def hook():
    """Manage Voice Mode hooks and event handlers."""
    pass


@hook.command()
@click.argument('tool_name')
@click.argument('action', type=click.Choice(['start', 'end', 'complete']))
@click.argument('subagent_type', required=False)
@click.option('--debug', is_flag=True, help='Enable debug output')
def receiver(tool_name, action, subagent_type, debug):
    """Receive and process hook events from Claude Code.
    
    This command is designed to be called by Claude Code hooks to play sounds
    when tools are used.
    
    Arguments:
        TOOL_NAME: The name of the tool being called (e.g., Task, Bash, Read)
        ACTION: The action type (start, end, or complete)
        SUBAGENT_TYPE: Optional subagent type for Task tool (e.g., mama-bear)
    
    Example:
        voicemode hook receiver Task start mama-bear
        voicemode hook receiver Bash end
    """
    # Import here to avoid circular imports
    from voice_mode.tools.sound_fonts.player import AudioPlayer
    
    if debug:
        click.echo(f"[DEBUG] Hook received: tool={tool_name}, action={action}, subagent={subagent_type}", err=True)
    
    try:
        # Create player instance
        player = AudioPlayer()
        
        # Play the sound
        success = player.play_sound_for_event(
            tool_name=tool_name,
            action=action,
            subagent_type=subagent_type,
            metadata={}
        )
        
        if debug:
            if success:
                click.echo(f"[DEBUG] Sound played successfully", err=True)
            else:
                click.echo(f"[DEBUG] No sound played (no config or sound file)", err=True)
        
        # Silent exit for hooks - don't clutter Claude Code output
        sys.exit(0 if success else 0)  # Always exit 0 to not disrupt Claude Code
        
    except Exception as e:
        if debug:
            click.echo(f"[DEBUG] Error: {e}", err=True)
        # Silent fail - hooks should not disrupt Claude Code operation
        sys.exit(0)