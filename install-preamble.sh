#!/bin/bash
# Voice Mode Universal Installer
# Usage: curl -sSf https://getvoicemode.com/install.sh | sh

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
MAGENTA='\033[0;35m'
ORANGE='\033[38;5;208m' # Claude Code orange
BOLD='\033[1m'
DIM='\033[2m'
NC='\033[0m' # No Color

# Detect terminal capabilities
if [ -t 1 ] && command -v tput >/dev/null 2>&1; then
  TERM_WIDTH=$(tput cols 2>/dev/null || echo 80)
else
  TERM_WIDTH=80
fi

# Center text function
center_text() {
  local text="$1"
  local width=${2:-$TERM_WIDTH}
  local text_len=${#text}
  local padding=$(((width - text_len) / 2))
  printf "%*s%s\n" $padding "" "$text"
}

# Clear screen for clean presentation
clear

# Display Voice Mode ASCII art
echo ""
echo -e "${ORANGE}${BOLD}"
cat <<'EOF'
    ╔════════════════════════════════════════════╗
    ║                                            ║
    ║   ██╗   ██╗ ██████╗ ██╗ ██████╗███████╗    ║
    ║   ██║   ██║██╔═══██╗██║██╔════╝██╔════╝    ║
    ║   ██║   ██║██║   ██║██║██║     █████╗      ║
    ║   ╚██╗ ██╔╝██║   ██║██║██║     ██╔══╝      ║
    ║    ╚████╔╝ ╚██████╔╝██║╚██████╗███████╗    ║
    ║     ╚═══╝   ╚═════╝ ╚═╝ ╚═════╝╚══════╝    ║
    ║                                            ║
    ║   ███╗   ███╗ ██████╗ ██████╗ ███████╗     ║
    ║   ████╗ ████║██╔═══██╗██╔══██╗██╔════╝     ║
    ║   ██╔████╔██║██║   ██║██║  ██║█████╗       ║
    ║   ██║╚██╔╝██║██║   ██║██║  ██║██╔══╝       ║
    ║   ██║ ╚═╝ ██║╚██████╔╝██████╔╝███████╗     ║
    ║   ╚═╝     ╚═╝ ╚═════╝ ╚═════╝ ╚══════╝     ║
    ║                                            ║
    ║     🎙️  Voice Interaction for AI  🤖       ║
    ║                                            ║
    ╚════════════════════════════════════════════╝
EOF
echo -e "${NC}"

# Display welcome message
echo ""
center_text "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo -e "${BOLD}Welcome to Voice Mode!${NC}"
echo ""
echo "Voice Mode brings natural voice conversations to your AI assistant."
echo "Talk to Claude, ChatGPT, or any MCP-compatible AI using your voice."
echo ""
center_text "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Explain what this installer does
echo -e "${BLUE}${BOLD}What this installer will do:${NC}"
echo ""
echo "  📦 Install Voice Mode package using UV (modern Python package manager)"
echo "  🔧 Set up shell completions for easy command access"
echo "  🎤 Optionally install local speech services:"
echo "     • Whisper (speech-to-text) - runs privately on your machine"
echo "     • Kokoro (text-to-speech) - natural voices without cloud dependency"
echo "     • LiveKit (real-time communication) - for seamless conversations"
echo ""
echo "  ☁️  Cloud services (OpenAI, etc.) work out of the box - no setup needed!"
echo ""

# System detection early
echo -e "${BLUE}${BOLD}Detecting your system...${NC}"
echo ""

# Detect OS and architecture
OS=""
ARCH=""
IS_MACOS=false
IS_APPLE_SILICON=false

if [[ "$OSTYPE" == "darwin"* ]]; then
  OS="macos"
  IS_MACOS=true
  ARCH=$(uname -m)
  if [[ "$ARCH" == "arm64" ]]; then
    IS_APPLE_SILICON=true
  fi
  echo -e "${GREEN}✓${NC} Detected: macOS on $ARCH"

  # Special message for Apple Silicon
  if [[ "$IS_APPLE_SILICON" == "true" ]]; then
    echo -e "${CYAN}  🚀 Apple Silicon detected - CoreML acceleration available!${NC}"
  fi
elif [[ -f /etc/os-release ]]; then
  source /etc/os-release
  if [[ "$ID" == "ubuntu" ]] || [[ "$ID_LIKE" == *"ubuntu"* ]]; then
    OS="ubuntu"
    ARCH=$(uname -m)
    echo -e "${GREEN}✓${NC} Detected: Ubuntu on $ARCH"
  elif [[ "$ID" == "fedora" ]]; then
    OS="fedora"
    ARCH=$(uname -m)
    echo -e "${GREEN}✓${NC} Detected: Fedora on $ARCH"
  else
    echo -e "${YELLOW}⚠${NC} Detected: $ID (experimental support)"
    OS="linux"
    ARCH=$(uname -m)
  fi
else
  echo -e "${YELLOW}⚠${NC} Unknown operating system - proceeding with generic Linux"
  OS="linux"
  ARCH=$(uname -m)
fi

echo ""
center_text "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Privacy notice
echo -e "${GREEN}${BOLD}🔒 Privacy First:${NC}"
echo ""
echo "  • Local services process everything on YOUR machine"
echo "  • No audio leaves your computer when using local services"
echo "  • Cloud services are optional - you choose what to use"
echo "  • Open source - inspect the code anytime"
echo ""

# Ready to proceed
echo -e "${BOLD}Ready to install Voice Mode?${NC}"
echo ""
echo "The installer will guide you through each step."
echo "You can skip optional components if you prefer cloud-only setup."
echo ""
echo -n "Press Enter to continue or Ctrl+C to cancel... "
read -r

# Clear for main installation
clear

echo ""
echo -e "${CYAN}${BOLD}Starting Voice Mode Installation...${NC}"
echo ""
center_text "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Continue with rest of installation...

