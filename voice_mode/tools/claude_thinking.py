"""Claude Code thinking extraction tool for Think Out Loud mode."""

import json
import os
from pathlib import Path
from typing import Optional, List, Dict, Any
from datetime import datetime

from voice_mode.server import mcp
from voice_mode.config import THINK_OUT_LOUD_ENABLED


def find_claude_log_file(working_dir: Optional[str] = None) -> Optional[Path]:
    """Find the current Claude Code conversation log file.
    
    Args:
        working_dir: The working directory (defaults to CWD)
        
    Returns:
        Path to the most recent JSONL log file, or None if not found
    """
    if working_dir is None:
        working_dir = os.getcwd()
    
    # Transform path: /Users/admin/Code/project → -Users-admin-Code-project
    project_dir = working_dir.replace('/', '-')
    
    # Build path to Claude logs
    claude_base = Path.home() / '.claude' / 'projects'
    log_dir = claude_base / project_dir
    
    if not log_dir.exists():
        return None
    
    # Find most recent .jsonl file
    log_files = sorted(
        log_dir.glob('*.jsonl'), 
        key=lambda p: p.stat().st_mtime,
        reverse=True
    )
    
    return log_files[0] if log_files else None


def extract_thinking_from_log(log_file: Path, last_n: int = 1) -> List[Dict[str, Any]]:
    """Extract thinking entries from Claude Code JSONL log.
    
    Args:
        log_file: Path to the JSONL log file
        last_n: Number of most recent thinking entries to return
        
    Returns:
        List of thinking entries with metadata
    """
    thinking_entries = []
    
    try:
        with open(log_file, 'r') as f:
            lines = f.readlines()
            
        # Process lines in reverse to get most recent first
        for line in reversed(lines):
            if not line.strip():
                continue
                
            try:
                entry = json.loads(line)
                
                # Look for assistant messages with thinking
                if entry.get('type') == 'assistant':
                    message = entry.get('message', {})
                    content = message.get('content', [])
                    
                    for item in content:
                        if item.get('type') == 'thinking':
                            thinking_text = item.get('text', '')
                            if thinking_text:
                                thinking_entries.append({
                                    'text': thinking_text,
                                    'timestamp': entry.get('timestamp'),
                                    'uuid': entry.get('uuid'),
                                    'raw_entry': entry
                                })
                                
                                if len(thinking_entries) >= last_n:
                                    return thinking_entries
                                    
            except json.JSONDecodeError:
                continue
                
    except Exception as e:
        # Log error but don't crash
        print(f"Error reading log file: {e}")
        
    return thinking_entries


@mcp.tool
def get_claude_thinking(
    last_n: int = 1,
    working_dir: Optional[str] = None,
    include_metadata: bool = False
) -> str:
    """Extract thinking from Claude Code conversation logs.
    
    This tool reads Claude Code's conversation logs to extract thinking entries
    that can be used for Think Out Loud mode. It's designed to work specifically
    with Claude Code's log format.
    
    Args:
        last_n: Number of most recent thinking entries to return (default: 1)
        working_dir: Working directory to find logs for (defaults to CWD)
        include_metadata: Include timestamp and UUID metadata
        
    Returns:
        The extracted thinking text, or an error message if not found
    """
    # Check if Think Out Loud mode is enabled
    if not THINK_OUT_LOUD_ENABLED:
        return "Think Out Loud mode is not enabled. Set VOICEMODE_THINK_OUT_LOUD=true to enable."
    
    # Find the log file
    log_file = find_claude_log_file(working_dir)
    if not log_file:
        return f"Could not find Claude Code logs for directory: {working_dir or os.getcwd()}"
    
    # Extract thinking
    thinking_entries = extract_thinking_from_log(log_file, last_n)
    
    if not thinking_entries:
        return "No thinking entries found in recent Claude Code logs."
    
    # Format output
    if len(thinking_entries) == 1 and not include_metadata:
        return thinking_entries[0]['text']
    
    # Multiple entries or metadata requested
    result = []
    for i, entry in enumerate(thinking_entries, 1):
        if include_metadata:
            timestamp = entry.get('timestamp', 'Unknown')
            uuid = entry.get('uuid', 'Unknown')
            result.append(f"=== Thinking Entry {i} ===")
            result.append(f"Timestamp: {timestamp}")
            result.append(f"UUID: {uuid}")
            result.append(f"Text:\n{entry['text']}")
            result.append("")
        else:
            if len(thinking_entries) > 1:
                result.append(f"=== Thinking Entry {i} ===")
            result.append(entry['text'])
            result.append("")
    
    return "\n".join(result).strip()


@mcp.tool
def check_claude_context() -> str:
    """Check if running in Claude Code context.
    
    Returns information about the Claude Code environment including:
    - Whether Claude Code logs are accessible
    - Current working directory
    - Log file location if found
    """
    working_dir = os.getcwd()
    log_file = find_claude_log_file(working_dir)
    
    result = []
    result.append(f"Working Directory: {working_dir}")
    result.append(f"Claude Logs Found: {'Yes' if log_file else 'No'}")
    
    if log_file:
        result.append(f"Log File: {log_file}")
        result.append(f"Log Size: {log_file.stat().st_size:,} bytes")
        
        # Check for recent activity
        mtime = datetime.fromtimestamp(log_file.stat().st_mtime)
        now = datetime.now()
        age = now - mtime
        
        if age.total_seconds() < 60:
            result.append(f"Last Updated: {int(age.total_seconds())} seconds ago")
        elif age.total_seconds() < 3600:
            result.append(f"Last Updated: {int(age.total_seconds() / 60)} minutes ago")
        else:
            result.append(f"Last Updated: {int(age.total_seconds() / 3600)} hours ago")
    else:
        project_dir = working_dir.replace('/', '-')
        expected_path = Path.home() / '.claude' / 'projects' / project_dir
        result.append(f"Expected Log Location: {expected_path}")
        result.append("Note: Logs are only created when using Claude Code (claude.ai/code)")
    
    return "\n".join(result)