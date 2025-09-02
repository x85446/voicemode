# Claude Thinking Implementation Review

## Summary
The `get_claude_messages` implementation in `voice_mode/tools/claude_thinking.py` follows **most** of the established conventions but needs a CLI command implementation to fully align with the codebase patterns.

## Current Implementation Analysis

### ✅ What's Done Right

1. **Shared Core Functions**: The implementation correctly separates core logic into reusable functions:
   - `find_claude_log_file()` - Finds the Claude Code log file
   - `extract_messages_from_log()` - Extracts messages from JSONL
   - `extract_thinking_from_messages()` - Extracts thinking content

2. **MCP Tool Pattern**: The MCP tools (`@mcp.tool` decorated functions) properly wrap the core functions and handle:
   - Configuration checking (THINK_OUT_LOUD_ENABLED)
   - Error handling with user-friendly messages
   - Multiple output formats (full, text, thinking)

3. **Backward Compatibility**: Maintains `get_claude_thinking()` as a legacy wrapper around the more general `get_claude_messages()`

4. **Proper Tool Documentation**: Extensive docstrings with clear examples and parameter descriptions

### ❌ What's Missing

1. **CLI Command Implementation**: No CLI command exists yet. Based on the pattern from other tools, there should be a `voice_mode/cli_commands/claude.py` file.

2. **Proper Logging**: Missing voice mode standard logging. Other tools use:
   ```python
   import logging
   logger = logging.getLogger("voice-mode")
   ```

3. **Debug/Verbose Output**: No debug logging for troubleshooting (other tools log at debug level)

## Recommended CLI Implementation

Create `voice_mode/cli_commands/claude.py`:

```python
"""CLI commands for Claude Code message extraction."""

import click
import json
import asyncio
from typing import Optional, List
import logging

from voice_mode.tools.claude_thinking import (
    find_claude_log_file,
    extract_messages_from_log,
    extract_thinking_from_messages
)

logger = logging.getLogger("voice-mode")


@click.group(name='claude')
def claude_group():
    """Extract messages from Claude Code conversation logs."""
    pass


@claude_group.command(name='messages')
@click.option('--last-n', '-n', default=2, type=int,
              help='Number of recent messages to extract')
@click.option('--type', '-t', 'message_types', multiple=True,
              type=click.Choice(['user', 'assistant']),
              help='Filter by message type (can specify multiple)')
@click.option('--format', '-f', 
              type=click.Choice(['full', 'text', 'thinking']),
              default='full',
              help='Output format')
@click.option('--working-dir', '-d', type=click.Path(exists=True),
              help='Working directory to find logs for')
@click.option('--output', '-o', type=click.Path(),
              help='Save output to file')
@click.option('--json', 'as_json', is_flag=True,
              help='Output as JSON (overrides format)')
@click.option('--debug', is_flag=True,
              help='Enable debug logging')
def messages_command(last_n: int, message_types: tuple, format: str,
                    working_dir: Optional[str], output: Optional[str],
                    as_json: bool, debug: bool):
    """
    Extract recent messages from Claude Code logs.
    
    Examples:
    
        voice-mode claude messages
        
        voice-mode claude messages -n 5 --format thinking
        
        voice-mode claude messages --type assistant --format text
        
        voice-mode claude messages --json -o messages.json
    """
    if debug:
        logger.setLevel(logging.DEBUG)
    
    # Find log file
    log_file = find_claude_log_file(working_dir)
    if not log_file:
        click.echo(f"Error: Could not find Claude Code logs", err=True)
        return
    
    logger.debug(f"Found log file: {log_file}")
    
    # Extract messages
    message_type_list = list(message_types) if message_types else None
    messages = extract_messages_from_log(log_file, last_n, message_type_list)
    
    if not messages:
        click.echo("No messages found in recent logs", err=True)
        return
    
    logger.debug(f"Extracted {len(messages)} messages")
    
    # Format output
    if as_json:
        content = json.dumps(messages, indent=2)
    elif format == 'thinking':
        thinking_texts = extract_thinking_from_messages(messages)
        if not thinking_texts:
            click.echo("No thinking content found", err=True)
            return
        content = "\n\n=== Next Thinking ===\n\n".join(thinking_texts)
    elif format == 'text':
        result = []
        for msg in messages:
            content_text = []
            for item in msg.get('content', []):
                if isinstance(item, dict):
                    if item.get('type') == 'text':
                        content_text.append(item.get('text', ''))
                    elif item.get('type') == 'thinking':
                        content_text.append(f"[Thinking: {item.get('text', '')}]")
            if content_text:
                result.append(f"{msg['type'].title()}: {' '.join(content_text)}")
        content = "\n\n".join(result)
    else:  # full format
        # Format as human-readable
        result = []
        for i, msg in enumerate(messages, 1):
            result.append(f"=== Message {i} ===")
            result.append(f"Type: {msg['type']}")
            result.append(f"Timestamp: {msg.get('timestamp', 'Unknown')}")
            # ... rest of formatting
        content = "\n".join(result)
    
    # Output
    if output:
        from pathlib import Path
        Path(output).write_text(content)
        click.echo(f"Output saved to {output}")
    else:
        click.echo(content)


@claude_group.command(name='thinking')
@click.option('--last-n', '-n', default=1, type=int,
              help='Number of messages to search for thinking')
@click.option('--working-dir', '-d', type=click.Path(exists=True),
              help='Working directory')
def thinking_command(last_n: int, working_dir: Optional[str]):
    """
    Extract only thinking content from Claude Code logs.
    
    Convenience command equivalent to:
    voice-mode claude messages --format thinking --type assistant
    """
    # Delegate to messages command with thinking format
    messages_command.callback(
        last_n=last_n,
        message_types=('assistant',),
        format='thinking',
        working_dir=working_dir,
        output=None,
        as_json=False,
        debug=False
    )


@claude_group.command(name='check')
def check_command():
    """Check if Claude Code context is available."""
    import os
    from pathlib import Path
    from datetime import datetime
    
    working_dir = os.getcwd()
    log_file = find_claude_log_file(working_dir)
    
    click.echo(f"Working Directory: {working_dir}")
    click.echo(f"Claude Logs Found: {'Yes' if log_file else 'No'}")
    
    if log_file:
        click.echo(f"Log File: {log_file}")
        click.echo(f"Log Size: {log_file.stat().st_size:,} bytes")
        
        mtime = datetime.fromtimestamp(log_file.stat().st_mtime)
        now = datetime.now()
        age = now - mtime
        
        if age.total_seconds() < 60:
            click.echo(f"Last Updated: {int(age.total_seconds())} seconds ago")
        elif age.total_seconds() < 3600:
            click.echo(f"Last Updated: {int(age.total_seconds() / 60)} minutes ago")
        else:
            click.echo(f"Last Updated: {int(age.total_seconds() / 3600)} hours ago")
    else:
        project_dir = working_dir.replace('/', '-')
        expected_path = Path.home() / '.claude' / 'projects' / project_dir
        click.echo(f"Expected Log Location: {expected_path}")
        click.echo("Note: Logs are only created when using Claude Code")
```

## Integration Requirements

1. **Add to CLI main**: Update `voice_mode/cli.py` to import and register the claude commands:
   ```python
   # Add import
   from voice_mode.cli_commands.claude import claude_group
   
   # Register with main CLI
   voice_mode_main_cli.add_command(claude_group)
   ```

2. **Add Logging**: Update `claude_thinking.py` to add proper logging:
   ```python
   import logging
   logger = logging.getLogger("voice-mode")
   
   # Add debug logging at key points
   logger.debug(f"Searching for Claude logs in: {log_dir}")
   logger.debug(f"Found {len(messages)} messages")
   ```

3. **Error Handling**: Ensure consistent error handling between CLI and MCP tool

## Convention Compliance Score

- **Shared Core Functions**: ✅ 10/10
- **MCP Tool Pattern**: ✅ 9/10 (missing debug logging)
- **CLI Command**: ❌ 0/10 (not implemented)
- **Logging/Debug**: ❌ 3/10 (minimal error logging only)
- **Documentation**: ✅ 9/10 (excellent docstrings)

**Overall**: 62% - Needs CLI implementation and logging to meet standards

## Recommendations

1. **Immediate**: Implement the CLI command as shown above
2. **Important**: Add standard voice-mode logging throughout
3. **Nice to have**: Add configuration option for THINK_OUT_LOUD check bypass
4. **Future**: Consider caching log file discovery for performance

## Testing Checklist

After implementing CLI:
- [ ] CLI command works standalone
- [ ] MCP tool continues to work
- [ ] Both share same core functions (no duplication)
- [ ] Debug logging works with VOICEMODE_DEBUG=true
- [ ] Error messages are consistent between CLI and MCP
- [ ] Output formats match between interfaces