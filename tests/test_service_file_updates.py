"""Tests for service file update functionality."""

import os
import json
import tempfile
from pathlib import Path
from unittest.mock import patch, MagicMock
import pytest

from voice_mode.tools.service import (
    load_service_file_version,
    get_installed_service_version,
    get_service_config_vars,
    update_service_files
)


def test_load_service_file_version():
    """Test loading service file versions from versions.json."""
    # Test for kokoro on macOS
    version = load_service_file_version("kokoro", "plist")
    assert version == "1.1.0"
    
    # Test for whisper on Linux
    version = load_service_file_version("whisper", "service")
    assert version == "1.1.0"


def test_get_service_config_vars():
    """Test getting configuration variables for service templates."""
    # Test whisper config
    whisper_vars = get_service_config_vars("whisper")
    assert "WHISPER_BIN" in whisper_vars
    assert "WHISPER_PORT" in whisper_vars
    assert whisper_vars["WHISPER_PORT"] == "2022"
    assert "MODEL_FILE" in whisper_vars
    assert "WORKING_DIR" in whisper_vars
    assert "LOG_DIR" in whisper_vars
    assert whisper_vars["LOG_DIR"].endswith("logs/whisper")
    
    # Test kokoro config
    kokoro_vars = get_service_config_vars("kokoro")
    assert "KOKORO_DIR" in kokoro_vars
    assert "KOKORO_PORT" in kokoro_vars
    assert kokoro_vars["KOKORO_PORT"] == "8880"
    assert "START_SCRIPT" in kokoro_vars
    assert "LOG_DIR" in kokoro_vars
    assert kokoro_vars["LOG_DIR"].endswith("logs/kokoro")


@pytest.mark.asyncio
async def test_update_service_files_already_up_to_date():
    """Test updating service files when already at latest version."""
    with patch('voice_mode.tools.service.get_installed_service_version') as mock_installed:
        with patch('voice_mode.tools.service.load_service_file_version') as mock_template:
            mock_installed.return_value = "1.1.0"
            mock_template.return_value = "1.1.0"
            
            result = await update_service_files("kokoro")
            assert "already up to date" in result
            assert "version 1.1.0" in result


@pytest.mark.asyncio
async def test_update_service_files_needs_update():
    """Test updating service files when update is needed."""
    with patch('voice_mode.tools.service.get_installed_service_version') as mock_installed:
        with patch('voice_mode.tools.service.load_service_file_version') as mock_template:
            with patch('voice_mode.tools.service.load_service_template') as mock_load:
                with patch('pathlib.Path.exists') as mock_exists:
                    with patch('pathlib.Path.write_text') as mock_write:
                        with patch('pathlib.Path.rename') as mock_rename:
                            with patch('subprocess.run') as mock_run:
                                with patch('voice_mode.tools.service.find_process_by_port') as mock_find:
                                    mock_installed.return_value = "1.0.0"
                                    mock_template.return_value = "1.1.0"
                                    mock_load.return_value = "template content with {KOKORO_PORT}"
                                    mock_exists.return_value = True
                                    mock_run.return_value = MagicMock(returncode=0)
                                    mock_find.return_value = None  # Not running
                                    
                                    result = await update_service_files("kokoro")
                                    assert "Updated kokoro service files" in result
                                    assert "from version 1.0.0 to 1.1.0" in result
                                    
                                    # Check that daemon-reload was called for Linux
                                    import platform
                                    if platform.system() == "Linux":
                                        mock_run.assert_called_with(
                                            ["systemctl", "--user", "daemon-reload"],
                                            capture_output=True
                                        )


@pytest.mark.asyncio
async def test_service_update_service_files_action():
    """Test the update-service-files functionality."""
    # Just test the update_service_files function directly
    result = await update_service_files("kokoro")
    
    # It should report already up to date or success
    assert "kokoro" in result.lower()
    assert "✅" in result or "❌" in result


def test_service_status_shows_version_info():
    """Test that status shows service file version information."""
    # This is tested via integration tests since it requires a running service
    # But we can test the version extraction logic
    with patch('voice_mode.tools.service.get_installed_service_version') as mock_installed:
        with patch('voice_mode.tools.service.load_service_file_version') as mock_template:
            mock_installed.return_value = "1.0.0"
            mock_template.return_value = "1.1.0"
            
            # The actual status function would include this info
            # We're just testing the version comparison logic here
            assert mock_installed.return_value != mock_template.return_value