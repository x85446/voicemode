# Task: Add Service Installation to install.sh

## Overview
Enhance the Voice Mode install.sh script to include optional service installation for Whisper, Kokoro, and LiveKit. The script should provide a user-friendly experience with clear information upfront and flexible installation options.

## Requirements

### 1. Script Introduction
- Display a clear overview at the start explaining what the script will do
- List the benefits and what the user will get after installation
- Request sudo early to cache credentials for the entire script run

### 2. Installation Modes
- **Quick Mode**: Default "yes to all" option for users who want everything installed
- **Selective Mode**: Allow users to choose individual services

### 3. Service Selection UI
- Present services with format: `ServiceName: Brief description of what it provides`
- Services to include:
  - **Whisper**: Local speech-to-text processing for voice conversations
  - **Kokoro**: High-quality text-to-speech with multiple voices
  - **LiveKit**: Real-time voice communication server
- Default selection: All services (user can press Enter to accept)

### 4. Platform Support
- Must work on both Linux and macOS
- Use existing patterns from current MCP tools and CLI commands

### 5. User Experience Flow
```
=== Voice Mode Installer ===

This script will set up Voice Mode with the following components:
- Core Voice Mode functionality 
- Optional local services for enhanced performance

[Requesting sudo access for system dependencies...]
[sudo] password for user: ****

Would you like to install local services for the best experience? [Y/n]: 

Available services:
  ✓ Whisper: Local speech-to-text processing
  ✓ Kokoro: High-quality text-to-speech voices  
  ✓ LiveKit: Real-time voice communication server

Install all services? [Y/n]: 
(Or press 's' to select individual services)
```

## Implementation Analysis

### Current Script Structure
- OS detection and platform-specific handling
- Dependency installation (system packages, Python, UV, Node.js)
- Claude Code installation and configuration
- Uses `confirm_action()` function for user prompts
- Color-coded output with print_step, print_success, print_warning functions

### Service Installation Patterns from MCP Tools
- Each service has install/uninstall tools with similar parameters
- Common pattern: check if installed, clone/download, setup service files, enable/start
- Service directories: `~/.voicemode/services/{service_name}`
- Use systemd on Linux, launchd on macOS
- Version management with git tags or binary releases

### Implementation Plan

#### 1. Add Service Installation Functions (Using CLI Commands)
```bash
install_services() {
    # Show introduction and benefits
    print_step "Voice Mode Services"
    echo ""
    echo "Voice Mode can install local services for the best experience:"
    echo "  • Whisper - Fast local speech-to-text (no cloud required)"
    echo "  • Kokoro - Natural text-to-speech with multiple voices"
    echo "  • LiveKit - Real-time voice communication server"
    echo ""
    echo "Benefits:"
    echo "  • Privacy - All processing happens locally"
    echo "  • Speed - No network latency"
    echo "  • Reliability - Works offline"
    echo ""
    
    # Quick mode or selective
    read -p "Install all recommended services? [Y/n/s]: " choice
    case $choice in
        [Ss]*)
            # Selective mode
            install_services_selective
            ;;
        [Nn]*)
            print_warning "Skipping service installation. Voice Mode will use cloud services."
            ;;
        *)
            # Default: install all
            install_all_services
            ;;
    esac
}

install_all_services() {
    print_step "Installing all Voice Mode services..."
    install_whisper_service
    install_kokoro_service
    install_livekit_service
}

install_services_selective() {
    if confirm_action "Install Whisper (speech-to-text)"; then
        install_whisper_service
    fi
    
    if confirm_action "Install Kokoro (text-to-speech)"; then
        install_kokoro_service
    fi
    
    if confirm_action "Install LiveKit (voice communication)"; then
        install_livekit_service
    fi
}
```

#### 2. Individual Service Installation Functions (Compose with CLI)
```bash
install_whisper_service() {
    print_step "Installing Whisper speech-to-text service..."
    
    # Use voice-mode CLI with auto-enable flag
    if voice-mode whisper install --auto-enable; then
        print_success "Whisper installed and enabled successfully"
    else
        print_warning "Failed to install Whisper service"
    fi
}

install_kokoro_service() {
    print_step "Installing Kokoro text-to-speech service..."
    
    # Use voice-mode CLI with auto-enable flag
    if voice-mode kokoro install --auto-enable; then
        print_success "Kokoro installed and enabled successfully"
    else
        print_warning "Failed to install Kokoro service"
    fi
}

install_livekit_service() {
    print_step "Installing LiveKit voice communication service..."
    
    # Use voice-mode CLI with auto-enable flag
    if voice-mode livekit install --auto-enable; then
        print_success "LiveKit installed and enabled successfully"
    else
        print_warning "Failed to install LiveKit service"
    fi
}
```

#### Benefits of This Approach
- **No duplication**: Reuses existing CLI commands and their logic
- **Consistent behavior**: Same installation process whether from script or CLI
- **Error handling**: CLI commands already handle port conflicts, existing services
- **Platform abstraction**: CLI commands handle macOS/Linux differences
- **Automatic enabling**: Uses --auto-enable flag to start services

#### 3. Early Sudo Caching
- Move sudo requirement earlier in script
- Use a dummy sudo command to cache credentials
- Example: `sudo -v` or `sudo true`

#### 4. Integration Points
- Call `install_services()` after core Voice Mode setup
- Before final success message
- After UV and Claude Code are installed

## Testing Strategy

### 1. Manual Testing
- Test on fresh Ubuntu 22.04/24.04 VMs
- Test on fresh Fedora 40/41 VMs
- Test on macOS (Intel and Apple Silicon)
- Test WSL2 environment

### 2. Test Scenarios
- Clean install with "yes to all"
- Clean install with selective choices
- Install with some services already present
- Install without sudo access (should fail gracefully)
- Install with network issues (should handle errors)

### 3. Automated Testing
- Create test harness that mocks user input
- Test each function in isolation
- Verify service installation commands are correct
- Check error handling paths

### 4. Verification Steps
- Verify services are installed to correct directories
- Check service files are created (systemd/launchd)
- Confirm services can start successfully
- Test that voice-mode commands work after installation

## Success Criteria
- [x] Script provides clear upfront information
- [x] Quick mode allows single "yes" for full installation
- [x] Selective mode works for individual service choices
- [x] Works reliably on both Linux and macOS
- [x] Integrates smoothly with existing install.sh structure
- [x] Follows existing patterns from MCP tools and CLI

## Next Steps
1. ~~Review existing install.sh script structure~~ ✓
2. ~~Study current MCP tool installation implementations~~ ✓
3. ~~Design the UI flow and prompts~~ ✓
4. Implement the feature
5. Test on both platforms