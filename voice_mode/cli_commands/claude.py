"""CLI commands for Claude-related functionality."""

import click


@click.group(name='claude')
def claude_group():
    """Claude-related commands."""
    pass