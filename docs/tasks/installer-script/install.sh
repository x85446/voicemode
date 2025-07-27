#!/bin/bash
# Voice Mode Universal Installer
# Usage: curl -sSf https://getvoicemode.com/install.sh | sh

set -e

# Reattach stdin to terminal for interactive prompts when run via curl | bash
[ -t 0 ] || exec </dev/tty # reattach keyboard to STDIN

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

check_system_dependencies() {
    print_step "Checking system dependencies..."
    
    local packages=("node" "portaudio" "ffmpeg")
    local missing_packages=()
    
    for package in "${packages[@]}"; do
        if brew list "$package" >/dev/null 2>&1; then
            print_success "$package is already installed"
        else
            missing_packages+=("$package")
        fi
    done
    
    if [ ${#missing_packages[@]} -eq 0 ]; then
        print_success "All system dependencies are already installed"
        return 0
    else
        echo "Missing packages: ${missing_packages[*]}"
        return 1
    fi
}

install_system_dependencies() {
    if ! check_system_dependencies; then
        if confirm_action "Install missing system dependencies via Homebrew"; then
            print_step "Installing system dependencies..."
            
            # Update Homebrew
            brew update
            
            # Install required packages
            local packages=("node" "portaudio" "ffmpeg")
            
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

setup_local_npm() {
    print_step "Setting up local npm configuration..."
    
    # Set up npm to use local directory (no sudo required)
    mkdir -p "$HOME/.npm-global"
    npm config set prefix "$HOME/.npm-global"
    
    # Add to PATH for current session
    export PATH="$HOME/.npm-global/bin:$PATH"
    
    # Add to shell profile if not already there
    local shell_profile=""
    if [[ "$SHELL" == *"zsh"* ]]; then
        shell_profile="$HOME/.zshrc"
    elif [[ "$SHELL" == *"bash"* ]]; then
        shell_profile="$HOME/.bash_profile"
    fi
    
    if [ -n "$shell_profile" ] && [ -f "$shell_profile" ]; then
        if ! grep -q "\.npm-global/bin" "$shell_profile"; then
            echo 'export PATH="$HOME/.npm-global/bin:$PATH"' >> "$shell_profile"
            print_success "Added npm global bin to PATH in $shell_profile"
        fi
    fi
    
    print_success "Local npm configuration complete"
}

configure_claude_voicemode() {
    if command -v claude >/dev/null 2>&1; then
        if confirm_action "Configure Voice Mode with Claude Code (adds MCP server)"; then
            print_step "Configuring Voice Mode with Claude Code..."
            
            if claude mcp add --scope user voice-mode -- uvx voice-mode; then
                print_success "Voice Mode configured with Claude Code"
                echo ""
                echo "🎉 Setup complete! You can now use voice commands in Claude Code:"
                echo "  claude converse"
                echo ""
                echo "Voice Mode will automatically install local speech services if needed."
            else
                print_error "Failed to configure Voice Mode with Claude Code"
            fi
        else
            print_step "Skipping Voice Mode configuration"
            echo "You can configure it later with:"
            echo "  claude mcp add --scope user voice-mode -- uvx voice-mode"
        fi
    else
        print_warning "Claude Code not found. Please install it first to use Voice Mode."
    fi
}

install_claude_if_needed() {
    if ! command -v claude >/dev/null 2>&1; then
        if confirm_action "Install Claude Code (required for Voice Mode)"; then
            print_step "Installing Claude Code..."
            if command -v npm >/dev/null 2>&1; then
                npm install -g @anthropic-ai/claude-code
                print_success "Claude Code installed"
            else
                print_error "npm not found. Please install Node.js first."
                return 1
            fi
        else
            print_warning "Claude Code is required for Voice Mode. Skipping configuration."
            return 1
        fi
    fi
    return 0
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
    
    # Install dependencies
    install_system_dependencies
    
    # Note: Homebrew's npm works for global installs without custom prefix setup
    
    # Install Claude Code if needed, then configure Voice Mode
    if install_claude_if_needed; then
        configure_claude_voicemode
    fi
    
    echo ""
    echo "For more information, visit: https://github.com/mbailey/voicemode"
}

# Run main function
main "$@"