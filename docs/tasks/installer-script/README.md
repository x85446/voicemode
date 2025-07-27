# Voice Mode Universal Installer Script

Create a universal installer script that handles system dependencies and voice-mode installation across different platforms.

## Overview

A shell script that can be executed with `curl -sSf https://getvoicemode.com/install.sh | sh` to automatically:

1. Detect the operating system
2. Install required system dependencies
3. Install voice-mode
4. Optionally configure Claude Code integration

## Phase 1: macOS Support

Initial implementation focuses on macOS with the following requirements:

### System Detection
- Detect macOS version
- Check for Apple Silicon vs Intel

### Dependencies Installation
- **Xcode Command Line Tools**: `xcode-select --install`
- **Homebrew**: Install if missing
- **System packages**: `portaudio`, `ffmpeg` via Homebrew

### Voice Mode Installation
- Install voice-mode via pip3 or uvx
- Support both stable and beta versions
- Handle TestPyPI installation for testing

### Optional Claude Integration
- Detect if Claude Code is installed
- Offer to install Claude Code if missing
- Configure MCP connection automatically

## Implementation Plan

### Step 1: Basic macOS Installer
```bash
#!/bin/bash
# install.sh - Voice Mode Universal Installer

set -e

detect_os() {
    # Detect macOS, version, architecture
}

install_xcode_tools() {
    # Check if already installed, prompt for installation
}

install_homebrew() {
    # Install Homebrew if missing
}

install_system_deps() {
    # Install portaudio, ffmpeg via Homebrew
}

install_voicemode() {
    # Install voice-mode package
}

main() {
    echo "🎤 Voice Mode Installer"
    detect_os
    install_xcode_tools
    install_homebrew
    install_system_deps
    install_voicemode
    echo "✅ Installation complete!"
}
```

### Step 2: Claude Code Integration
- Auto-detect Claude Code installation
- Offer installation via npm if missing
- Configure MCP connection in Claude's config file

### Step 3: Platform Expansion
- Add Linux support (Ubuntu/Debian, Fedora/RHEL)
- Add Windows/WSL support
- Add NixOS support

## Testing Strategy

1. Test on fresh Mac Mini with no development tools
2. Test with existing Homebrew installation
3. Test with existing Xcode tools
4. Test Claude Code integration flow
5. Test error handling and recovery

## Hosting

Host the installer script at `https://getvoicemode.com/install.sh` for easy access.

## Future Enhancements

- Interactive mode with user prompts
- Quiet mode for automated installations
- Support for installing specific versions
- Uninstallation script
- Update mechanism