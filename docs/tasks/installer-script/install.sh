#!/bin/bash
# Voice Mode Universal Installer
# Usage: curl -sSf https://getvoicemode.com/install.sh | sh

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Global variables
OS=""
ARCH=""
HOMEBREW_INSTALLED=false
XCODE_TOOLS_INSTALLED=false

print_step() {
    echo -e "${BLUE}🔧 $1${NC}"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
    exit 1
}

detect_os() {
    print_step "Detecting operating system..."
    
    if [[ "$OSTYPE" == "darwin"* ]]; then
        OS="macos"
        ARCH=$(uname -m)
        local macos_version=$(sw_vers -productVersion)
        print_success "Detected macOS $macos_version on $ARCH"
    else
        print_error "Unsupported operating system: $OSTYPE. Currently only macOS is supported."
    fi
}

check_xcode_tools() {
    print_step "Checking for Xcode Command Line Tools..."
    
    if xcode-select -p >/dev/null 2>&1; then
        XCODE_TOOLS_INSTALLED=true
        print_success "Xcode Command Line Tools are already installed"
    else
        print_warning "Xcode Command Line Tools not found"
    fi
}

install_xcode_tools() {
    if [ "$XCODE_TOOLS_INSTALLED" = false ]; then
        print_step "Installing Xcode Command Line Tools..."
        echo "This will open a dialog to install Xcode Command Line Tools."
        echo "Please follow the prompts and re-run this installer after installation completes."
        
        xcode-select --install
        
        print_warning "Please complete the Xcode Command Line Tools installation and re-run this installer."
        exit 0
    fi
}

check_homebrew() {
    print_step "Checking for Homebrew..."
    
    if command -v brew >/dev/null 2>&1; then
        HOMEBREW_INSTALLED=true
        print_success "Homebrew is already installed"
    else
        print_warning "Homebrew not found"
    fi
}

confirm_action() {
    local action="$1"
    echo ""
    echo "About to: $action"
    read -p "Continue? (y/n): " choice
    case $choice in
        [Yy]*) return 0 ;;
        *) 
            echo "Skipping: $action"
            return 1 
            ;;
    esac
}

install_homebrew() {
    if [ "$HOMEBREW_INSTALLED" = false ]; then
        if confirm_action "Install Homebrew (this will also install Xcode Command Line Tools)"; then
            print_step "Installing Homebrew..."
            /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
            
            # Add Homebrew to PATH for current session
            if [[ "$ARCH" == "arm64" ]]; then
                eval "$(/opt/homebrew/bin/brew shellenv)"
            else
                eval "$(/usr/local/bin/brew shellenv)"
            fi
            
            print_success "Homebrew installed successfully"
            
            # Update the status variables since Homebrew installs Xcode tools
            HOMEBREW_INSTALLED=true
            XCODE_TOOLS_INSTALLED=true
        else
            print_error "Homebrew is required for Voice Mode dependencies. Installation aborted."
        fi
    fi
}

install_system_dependencies() {
    if confirm_action "Install system dependencies (portaudio, ffmpeg) via Homebrew"; then
        print_step "Installing system dependencies..."
        
        # Update Homebrew
        brew update
        
        # Install required packages
        local packages=("portaudio" "ffmpeg")
        
        for package in "${packages[@]}"; do
            if brew list "$package" >/dev/null 2>&1; then
                print_success "$package is already installed"
            else
                print_step "Installing $package..."
                brew install "$package"
                print_success "$package installed"
            fi
        done
    else
        print_warning "Skipping system dependencies. Voice Mode may not work properly without them."
    fi
}

check_python() {
    print_step "Checking Python installation..."
    
    if command -v python3 >/dev/null 2>&1; then
        local python_version=$(python3 --version | cut -d' ' -f2)
        print_success "Python 3 found: $python_version"
        
        # Check if pip3 is available
        if command -v pip3 >/dev/null 2>&1; then
            print_success "pip3 is available"
        else
            print_error "pip3 not found. Please install pip for Python 3."
        fi
    else
        print_error "Python 3 not found. Please install Python 3 first."
    fi
}

install_voicemode() {
    if confirm_action "Install Voice Mode Python package"; then
        print_step "Installing Voice Mode..."
        
        # Ask user if they want beta version
        echo "Which version would you like to install?"
        echo "1) Stable (recommended)"
        echo "2) Beta (latest features)"
        read -p "Enter choice (1 or 2): " version_choice
        
        case $version_choice in
            2)
                print_step "Installing Voice Mode beta from TestPyPI..."
                pip3 install --index-url https://test.pypi.org/simple/ voice-mode
                ;;
            *)
                print_step "Installing Voice Mode stable version..."
                pip3 install voice-mode
                ;;
        esac
        
        # Verify installation
        if command -v voice-mode >/dev/null 2>&1; then
            local vm_version=$(voice-mode --version 2>/dev/null || echo "unknown")
            print_success "Voice Mode installed successfully: $vm_version"
        else
            print_error "Voice Mode installation failed"
        fi
    else
        print_error "Voice Mode is required for this installer. Installation aborted."
    fi
}

setup_claude_integration() {
    print_step "Checking for Claude Code..."
    
    if command -v claude >/dev/null 2>&1; then
        print_success "Claude Code found"
        
        echo "Would you like to configure Voice Mode with Claude Code? (y/n)"
        read -p "Enter choice: " claude_choice
        
        case $claude_choice in
            [Yy]*)
                print_step "Configuring Claude Code integration..."
                
                # Check if user has OPENAI_API_KEY
                if [ -z "$OPENAI_API_KEY" ]; then
                    print_warning "OPENAI_API_KEY not set in environment"
                    echo "Please set your OpenAI API key:"
                    echo "export OPENAI_API_KEY='your-api-key-here'"
                    echo ""
                    echo "Then configure Voice Mode with Claude:"
                    echo "claude mcp add voice-mode -- uvx voice-mode"
                else
                    # Add MCP server with API key
                    claude mcp add voice-mode --env OPENAI_API_KEY="$OPENAI_API_KEY" -- uvx voice-mode
                    print_success "Claude Code integration configured"
                fi
                ;;
            *)
                print_step "Skipping Claude Code integration"
                ;;
        esac
    else
        print_warning "Claude Code not found"
        echo "Would you like to install Claude Code? (y/n)"
        read -p "Enter choice: " install_claude
        
        case $install_claude in
            [Yy]*)
                print_step "Installing Claude Code..."
                npm install -g @anthropic-ai/claude-code
                print_success "Claude Code installed"
                
                echo "Please set your OpenAI API key and run:"
                echo "claude mcp add voice-mode -- uvx voice-mode"
                ;;
            *)
                print_step "Skipping Claude Code installation"
                echo "You can install it later with:"
                echo "npm install -g @anthropic-ai/claude-code"
                ;;
        esac
    fi
}

main() {
    echo -e "${BLUE}🎤 Voice Mode Universal Installer${NC}"
    echo "This installer will set up Voice Mode and its dependencies on your system."
    echo ""
    
    # Pre-flight checks
    detect_os
    check_homebrew
    
    # Skip Xcode tools check if Homebrew will handle it
    if [ "$HOMEBREW_INSTALLED" = false ]; then
        install_homebrew  # This installs Xcode tools automatically
    fi
    
    check_python
    
    # Install dependencies and Voice Mode
    install_system_dependencies
    install_voicemode
    
    # Optional Claude integration
    setup_claude_integration
    
    echo ""
    print_success "🎉 Voice Mode installation complete!"
    echo ""
    echo "Next steps:"
    echo "1. Set your OpenAI API key: export OPENAI_API_KEY='your-key'"
    echo "2. Test voice mode: voice-mode --help"
    echo "3. Configure with Claude: claude mcp add voice-mode -- uvx voice-mode"
    echo ""
    echo "For more information, visit: https://github.com/mbailey/voicemode"
}

# Run main function
main "$@"