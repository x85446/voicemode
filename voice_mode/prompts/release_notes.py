"""Release notes prompt for displaying recent CHANGELOG entries."""

from pathlib import Path
from voice_mode.server import mcp


def parse_changelog(changelog_path: Path, max_versions: int = 5) -> str:
    """Parse CHANGELOG.md and extract recent version entries.
    
    Args:
        changelog_path: Path to CHANGELOG.md file
        max_versions: Maximum number of versions to return
        
    Returns:
        Formatted string of recent changelog entries
    """
    if not changelog_path.exists():
        return "CHANGELOG.md not found"
    
    try:
        content = changelog_path.read_text()
        lines = content.split('\n')
        
        # Track versions found
        versions = []
        current_version = None
        current_content = []
        
        for line in lines:
            # Skip the header and empty lines at the beginning
            if line.startswith('# Changelog') or (not line.strip() and not current_version):
                continue
                
            # Check for version header (## [x.y.z] - date)
            if line.startswith('## [') and '] - ' in line:
                # Save previous version if exists
                if current_version and current_content:
                    versions.append({
                        'header': current_version,
                        'content': '\n'.join(current_content).strip()
                    })
                    
                # Start new version
                current_version = line
                current_content = []
                
                # Stop if we have enough versions
                if len(versions) >= max_versions:
                    break
            elif current_version:
                # Add content to current version
                current_content.append(line)
        
        # Don't forget the last version
        if current_version and current_content and len(versions) < max_versions:
            versions.append({
                'header': current_version,
                'content': '\n'.join(current_content).strip()
            })
        
        # Reverse to show oldest first (newest last)
        versions.reverse()
        
        # Format the output
        output = []
        for version in versions:
            output.append(version['header'])
            output.append(version['content'])
            output.append('')  # Empty line between versions
        
        return '\n'.join(output).strip()
        
    except Exception as e:
        return f"Error reading CHANGELOG.md: {str(e)}"


@mcp.prompt(name="release-notes")
def release_notes_prompt(versions: int = 5) -> str:
    """View recent release notes from Voice Mode's CHANGELOG.
    
    Args:
        versions: Number of recent versions to display (default: 5)
    """
    # Get the path to CHANGELOG.md relative to this file
    changelog_path = Path(__file__).parent.parent.parent / "CHANGELOG.md"
    
    # Parse and return the changelog entries
    changelog_content = parse_changelog(changelog_path, max_versions=versions)
    
    # Format as a nice message
    return f"""Voice Mode Release Notes
=======================

{changelog_content}

For the complete changelog, see: https://github.com/remsky/voicemode/blob/master/CHANGELOG.md"""