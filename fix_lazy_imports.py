#!/usr/bin/env python3
"""Script to add lazy imports to cli.py for performance optimization."""

import re
from pathlib import Path

# Read the current file
cli_file = Path("voice_mode/cli.py")
content = cli_file.read_text()

# 1. Remove the server import from the top
content = content.replace(
    "from .server import main as voice_mode_main",
    ""
)

# 2. Add lazy import in the main CLI function
content = content.replace(
    """    if ctx.invoked_subcommand is None:
        # No subcommand - run MCP server
        # Note: warnings are already suppressed at module level unless debug is enabled
        voice_mode_main()""",
    """    if ctx.invoked_subcommand is None:
        # No subcommand - run MCP server
        # Note: warnings are already suppressed at module level unless debug is enabled
        from .server import main as voice_mode_main
        voice_mode_main()"""
)

# 3. Remove all the imports at module level (lines 77-100)
lines_to_remove = """# Import service functions
from voice_mode.tools.service import (
    status_service, start_service, stop_service, restart_service,
    enable_service, disable_service, view_logs, update_service_files
)

# Import install/uninstall functions
from voice_mode.tools.services.kokoro.install import kokoro_install
from voice_mode.tools.services.kokoro.uninstall import kokoro_uninstall
from voice_mode.tools.services.whisper.install import whisper_install
from voice_mode.tools.services.whisper.uninstall import whisper_uninstall
from voice_mode.tools.services.whisper.download_model import download_model
from voice_mode.tools.services.livekit.install import livekit_install
from voice_mode.tools.services.livekit.uninstall import livekit_uninstall
from voice_mode.tools.services.livekit.frontend import livekit_frontend_start, livekit_frontend_stop, livekit_frontend_status, livekit_frontend_open, livekit_frontend_logs, livekit_frontend_install

# Import configuration management functions
from voice_mode.tools.configuration_management import update_config, list_config_keys

# Import diagnostic functions - extract the actual async functions from the tools
from voice_mode.tools.diagnostics import voice_mode_info
from voice_mode.tools.devices import check_audio_devices
from voice_mode.tools.voice_registry import voice_registry
from voice_mode.tools.dependencies import check_audio_dependencies"""

content = content.replace(lines_to_remove, "# Service functions are imported lazily in their respective command handlers")

# 4. Add lazy imports to each command function that needs them

# Service functions mappings
service_functions = {
    "status_service": "from voice_mode.tools.service import status_service",
    "start_service": "from voice_mode.tools.service import start_service",
    "stop_service": "from voice_mode.tools.service import stop_service",
    "restart_service": "from voice_mode.tools.service import restart_service",
    "enable_service": "from voice_mode.tools.service import enable_service",
    "disable_service": "from voice_mode.tools.service import disable_service",
    "view_logs": "from voice_mode.tools.service import view_logs",
    "update_service_files": "from voice_mode.tools.service import update_service_files",
}

# Install/uninstall functions
install_functions = {
    "kokoro_install": "from voice_mode.tools.services.kokoro.install import kokoro_install",
    "kokoro_uninstall": "from voice_mode.tools.services.kokoro.uninstall import kokoro_uninstall",
    "whisper_install": "from voice_mode.tools.services.whisper.install import whisper_install",
    "whisper_uninstall": "from voice_mode.tools.services.whisper.uninstall import whisper_uninstall",
    "download_model": "from voice_mode.tools.services.whisper.download_model import download_model",
    "livekit_install": "from voice_mode.tools.services.livekit.install import livekit_install",
    "livekit_uninstall": "from voice_mode.tools.services.livekit.uninstall import livekit_uninstall",
    "livekit_frontend_start": "from voice_mode.tools.services.livekit.frontend import livekit_frontend_start",
    "livekit_frontend_stop": "from voice_mode.tools.services.livekit.frontend import livekit_frontend_stop",
    "livekit_frontend_status": "from voice_mode.tools.services.livekit.frontend import livekit_frontend_status",
    "livekit_frontend_open": "from voice_mode.tools.services.livekit.frontend import livekit_frontend_open",
    "livekit_frontend_logs": "from voice_mode.tools.services.livekit.frontend import livekit_frontend_logs",
    "livekit_frontend_install": "from voice_mode.tools.services.livekit.frontend import livekit_frontend_install",
}

# Config functions
config_functions = {
    "update_config": "from voice_mode.tools.configuration_management import update_config",
    "list_config_keys": "from voice_mode.tools.configuration_management import list_config_keys",
}

# Diagnostic functions
diag_functions = {
    "voice_mode_info": "from voice_mode.tools.diagnostics import voice_mode_info",
    "check_audio_devices": "from voice_mode.tools.devices import check_audio_devices",
    "voice_registry": "from voice_mode.tools.voice_registry import voice_registry",
    "check_audio_dependencies": "from voice_mode.tools.dependencies import check_audio_dependencies",
}

# Exchanges import
exchanges_import = "from voice_mode.cli_commands import exchanges as exchanges_cmd"

# All functions to check
all_functions = {**service_functions, **install_functions, **config_functions, **diag_functions}

# Function to add import after function definition
def add_lazy_import(content, func_name, import_stmt):
    # Find all occurrences of the function call
    pattern = rf'(\n@[\w.]+\.command[^\n]*\ndef [\w_]+\([^)]*\):\n    """[^"]*"""\n)(    result = asyncio\.run\({func_name}[\.\w]*\('
    
    def replacer(match):
        return match.group(1) + f"    {import_stmt}\n" + match.group(2)
    
    content = re.sub(pattern, replacer, content)
    return content

# Apply lazy imports for all functions
for func_name, import_stmt in all_functions.items():
    # Add import before the function is used
    if func_name in content:
        # Special handling for different patterns
        if func_name in service_functions:
            # For service functions, they're called directly
            pattern = r'(def [\w_]+\([^)]*\):\n    """[^"]*"""\n)(    result = asyncio\.run\(' + re.escape(func_name) + r'\('
            replacement = rf'\1    {import_stmt}\n\2'
            content = re.sub(pattern, replacement, content)
        elif func_name.endswith('_install') or func_name.endswith('_uninstall'):
            # For install/uninstall functions, they're called with .fn
            pattern = r'(def [\w_]+\([^)]*\):\n    """[^"]*"""\n)(    result = asyncio\.run\(' + re.escape(func_name) + r'\.fn\('
            replacement = rf'\1    {import_stmt}\n\2'
            content = re.sub(pattern, replacement, content)
        elif func_name.startswith('livekit_frontend'):
            # For frontend functions
            pattern = r'(def [\w_]+\([^)]*\):\n    """[^"]*"""\n)(    result = asyncio\.run\(' + re.escape(func_name) + r'\.fn\('
            replacement = rf'\1    {import_stmt}\n\2'
            content = re.sub(pattern, replacement, content)
        elif func_name in config_functions or func_name in diag_functions:
            # For config and diag functions
            pattern = r'(def [\w_]+\([^)]*\):\n    """[^"]*"""\n)(    result = asyncio\.run\(' + re.escape(func_name) + r'\.fn\('
            replacement = rf'\1    {import_stmt}\n\2'
            content = re.sub(pattern, replacement, content)

# Special case for download_model - it's used after import json
content = content.replace(
    "    import json\n    result = asyncio.run(download_model.fn(",
    "    import json\n    from voice_mode.tools.services.whisper.download_model import download_model\n    result = asyncio.run(download_model.fn("
)

# Remove the exchanges import from module level
content = content.replace(
    "# Import subcommand groups\nfrom voice_mode.cli_commands import exchanges as exchanges_cmd",
    "# Exchanges subcommand is imported lazily"
)

# Update the exchanges command to import lazily
content = content.replace(
    "# Add subcommands to legacy CLI\ncli.add_command(exchanges_cmd.exchanges)\n\n# Add exchanges to main CLI\nvoice_mode_main_cli.add_command(exchanges_cmd.exchanges)",
    """# Add exchanges command to both CLIs with lazy import
@voice_mode_main_cli.command('exchanges')
@click.pass_context
def exchanges_main(ctx):
    \"\"\"Manage and view conversation exchange logs.\"\"\"
    from voice_mode.cli_commands import exchanges as exchanges_cmd
    ctx.invoke(exchanges_cmd.exchanges)

@cli.command('exchanges')
@click.pass_context 
def exchanges_legacy(ctx):
    \"\"\"Manage and view conversation exchange logs.\"\"\"
    from voice_mode.cli_commands import exchanges as exchanges_cmd
    ctx.invoke(exchanges_cmd.exchanges)"""
)

# Write the modified content
cli_file.write_text(content)
print("✅ Lazy imports applied successfully!")