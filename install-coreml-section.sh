#!/bin/bash
# CoreML Acceleration Setup Section for install.sh
# This section should be inserted after Whisper service installation

# Check if we're on Apple Silicon Mac
if [[ "$OS" == "macos" ]] && [[ "$ARCH" == "arm64" ]]; then
    echo ""
    echo -e "${CYAN}${BOLD}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo ""
    echo -e "${BLUE}${BOLD}🚀 CoreML Acceleration Available${NC}"
    echo ""
    echo "Your Mac supports CoreML acceleration for Whisper!"
    echo ""
    echo -e "${GREEN}Benefits:${NC}"
    echo "  • 2-3x faster transcription than Metal-only"
    echo "  • Lower CPU usage during speech recognition"
    echo "  • Better battery life on MacBooks"
    echo ""
    echo -e "${YELLOW}Requirements:${NC}"
    echo "  • PyTorch package (~2.5GB download)"
    echo "  • CoreMLTools and dependencies (~100MB)"
    echo "  • Full Xcode installation (~10GB from Mac App Store)"
    echo ""
    
    # Check for Xcode
    XCODE_AVAILABLE=false
    if [[ -f "/Applications/Xcode.app/Contents/Developer/Toolchains/XcodeDefault.xctoolchain/usr/bin/coremlc" ]]; then
        echo -e "${GREEN}✓${NC} Full Xcode detected"
        XCODE_AVAILABLE=true
    else
        echo -e "${YELLOW}⚠${NC} Full Xcode not found (Command Line Tools alone won't work)"
        echo ""
        echo "  Without Xcode, Whisper will still use Metal acceleration (fast)"
        echo "  To enable CoreML later:"
        echo "    1. Install Xcode from Mac App Store"
        echo "    2. Open Xcode once to accept license"
        echo "    3. Run: sudo xcode-select -s /Applications/Xcode.app/Contents/Developer"
        echo "    4. Run: voice-mode whisper model-install --install-torch"
    fi
    
    echo ""
    
    # Only offer to install if Xcode is available
    if [[ "$XCODE_AVAILABLE" == "true" ]]; then
        echo -e "${BOLD}Install CoreML acceleration now?${NC}"
        echo ""
        echo "This will download PyTorch (~2.5GB) and configure CoreML."
        echo "You can always add this later with: voice-mode whisper model-install --install-torch"
        echo ""
        read -p "Install CoreML acceleration? [y/N]: " -n 1 -r
        echo ""
        
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            echo ""
            print_step "Installing CoreML dependencies..."
            echo "This may take several minutes due to the large download size..."
            echo ""
            
            # Run the whisper model-install command with torch installation
            if uvx voice-mode whisper model-install large-v2 --install-torch --yes; then
                print_success "CoreML acceleration installed successfully!"
                echo ""
                echo "Whisper will now use CoreML for maximum performance."
            else
                print_warning "CoreML installation encountered issues."
                echo "Whisper will use Metal acceleration (still fast)."
                echo ""
                echo "You can retry later with:"
                echo "  voice-mode whisper model-install --install-torch"
            fi
        else
            echo ""
            echo "Skipping CoreML setup. Whisper will use Metal acceleration."
            echo ""
            echo -e "${DIM}To add CoreML later, run: voice-mode whisper model-install --install-torch${NC}"
        fi
    else
        echo -e "${DIM}Skipping CoreML - Xcode not installed${NC}"
        echo "Whisper will use Metal acceleration (still performs well)"
    fi
    
    echo ""
    echo -e "${CYAN}${BOLD}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
fi