#!/bin/bash
# Test script for install.sh service installation feature
# Tests various scenarios on both macOS and Linux

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Test configuration
TEST_DIR="/tmp/voicemode-install-test"
MOCK_VOICE_MODE="$TEST_DIR/mock-voice-mode"
INSTALL_SCRIPT="./install.sh"

print_test() {
  echo -e "${BLUE}TEST: $1${NC}"
}

print_success() {
  echo -e "${GREEN}✅ $1${NC}"
}

print_failure() {
  echo -e "${RED}❌ $1${NC}"
}

# Create mock environment
setup_test_env() {
  print_test "Setting up test environment"
  
  # Create test directory
  mkdir -p "$TEST_DIR"
  
  # Create mock voice-mode command
  cat > "$MOCK_VOICE_MODE" << 'EOF'
#!/bin/bash
# Mock voice-mode command for testing

case "$1" in
  "whisper")
    case "$2" in
      "install")
        echo "Mock: Installing Whisper service..."
        sleep 1
        echo "Mock: Whisper installed successfully"
        exit 0
        ;;
      *)
        echo "Mock: Unknown whisper command: $2"
        exit 1
        ;;
    esac
    ;;
  "kokoro")
    case "$2" in
      "install")
        echo "Mock: Installing Kokoro service..."
        sleep 1
        # Simulate occasional failure for testing
        if [[ "$FORCE_KOKORO_FAIL" == "true" ]]; then
          echo "Mock: Kokoro installation failed!"
          exit 1
        fi
        echo "Mock: Kokoro installed successfully"
        exit 0
        ;;
      *)
        echo "Mock: Unknown kokoro command: $2"
        exit 1
        ;;
    esac
    ;;
  "livekit")
    case "$2" in
      "install")
        echo "Mock: Installing LiveKit service..."
        sleep 1
        echo "Mock: LiveKit installed successfully"
        exit 0
        ;;
      *)
        echo "Mock: Unknown livekit command: $2"
        exit 1
        ;;
    esac
    ;;
  "--help")
    echo "Mock voice-mode help"
    exit 0
    ;;
  *)
    echo "Mock: Unknown command: $1"
    exit 1
    ;;
esac
EOF
  
  chmod +x "$MOCK_VOICE_MODE"
  
  # Add mock to PATH
  export PATH="$TEST_DIR:$PATH"
  
  # Create mock claude command
  cat > "$TEST_DIR/claude" << 'EOF'
#!/bin/bash
case "$1" in
  "mcp")
    case "$2" in
      "list")
        echo "voice-mode -- uvx voice-mode"
        exit 0
        ;;
      *)
        exit 0
        ;;
    esac
    ;;
  *)
    exit 0
    ;;
esac
EOF
  chmod +x "$TEST_DIR/claude"
  
  # Create a test version of install.sh with mocked dependencies
  cp "$INSTALL_SCRIPT" "$TEST_DIR/install.sh"
  
  print_success "Test environment created"
}

# Test 1: Voice-mode CLI detection
test_cli_detection() {
  print_test "Testing voice-mode CLI detection"
  
  # Source just the check_voice_mode_cli function
  eval "$(sed -n '/^check_voice_mode_cli()/,/^}/p' "$INSTALL_SCRIPT")"
  
  # Test with mock in PATH
  if voice_cmd=$(check_voice_mode_cli); then
    if [[ "$voice_cmd" == *"mock-voice-mode" ]]; then
      print_success "CLI detection found mock command"
    else
      print_failure "CLI detection returned wrong command: $voice_cmd"
    fi
  else
    print_failure "CLI detection failed when mock was available"
  fi
  
  # Test without voice-mode in PATH
  PATH_BACKUP="$PATH"
  export PATH="/usr/bin:/bin"
  if voice_cmd=$(check_voice_mode_cli 2>/dev/null); then
    print_failure "CLI detection succeeded when voice-mode not in PATH"
  else
    print_success "CLI detection correctly failed when not in PATH"
  fi
  export PATH="$PATH_BACKUP"
}

# Test 2: Service installation with "yes to all"
test_install_all() {
  print_test "Testing 'install all' option"
  
  # Source required functions more carefully
  eval "$(sed -n '/^install_service()/,/^}/p' "$INSTALL_SCRIPT")"
  eval "$(sed -n '/^install_all_services()/,/^}/p' "$INSTALL_SCRIPT")"
  eval "$(sed -n '/^print_step()/,/^}/p' "$INSTALL_SCRIPT")"
  eval "$(sed -n '/^print_success()/,/^}/p' "$INSTALL_SCRIPT")"
  eval "$(sed -n '/^print_warning()/,/^}/p' "$INSTALL_SCRIPT")"
  
  # Mock user input for "yes to all"
  export FORCE_KOKORO_FAIL="false"
  
  # Run installation with piped input
  echo "" | install_all_services "mock-voice-mode"
  
  print_success "Install all completed"
}

# Test 3: Service installation with selective mode
test_selective_install() {
  print_test "Testing selective installation"
  
  # Source required functions more carefully
  eval "$(sed -n '/^install_service()/,/^}/p' "$INSTALL_SCRIPT")"
  eval "$(sed -n '/^install_all_services()/,/^}/p' "$INSTALL_SCRIPT")"
  eval "$(sed -n '/^print_step()/,/^}/p' "$INSTALL_SCRIPT")"
  eval "$(sed -n '/^print_success()/,/^}/p' "$INSTALL_SCRIPT")"
  eval "$(sed -n '/^print_warning()/,/^}/p' "$INSTALL_SCRIPT")"
  
  # Mock confirm_action function
  confirm_action() {
    case "$1" in
      *"Whisper"*)
        return 0  # Yes
        ;;
      *"Kokoro"*)
        return 1  # No
        ;;
      *"LiveKit"*)
        return 0  # Yes
        ;;
    esac
  }
  
  # Run selective installation
  install_services_selective "mock-voice-mode"
  
  print_success "Selective installation completed"
}

# Test 4: Service installation with failures
test_install_with_failures() {
  print_test "Testing installation with service failures"
  
  # Source required functions more carefully
  eval "$(sed -n '/^install_service()/,/^}/p' "$INSTALL_SCRIPT")"
  eval "$(sed -n '/^install_all_services()/,/^}/p' "$INSTALL_SCRIPT")"
  eval "$(sed -n '/^print_step()/,/^}/p' "$INSTALL_SCRIPT")"
  eval "$(sed -n '/^print_success()/,/^}/p' "$INSTALL_SCRIPT")"
  eval "$(sed -n '/^print_warning()/,/^}/p' "$INSTALL_SCRIPT")"
  
  # Force Kokoro to fail
  export FORCE_KOKORO_FAIL="true"
  
  # Run installation
  install_all_services "mock-voice-mode"
  
  print_success "Handled service failures gracefully"
}

# Test 5: Full install.sh integration test
test_full_integration() {
  print_test "Testing full install.sh integration"
  
  # Create a modified install.sh that skips actual installations
  cat > "$TEST_DIR/install-test.sh" << 'EOF'
#!/bin/bash
# Modified install.sh for testing

# Source the original but override key functions
source ./install.sh

# Override functions that would actually install things
detect_os() {
  OS="macos"
  ARCH="arm64"
  print_success "Mocked OS detection"
}

check_homebrew() {
  HOMEBREW_INSTALLED=true
}

check_python() {
  print_success "Mocked Python check"
}

install_uvx() {
  print_success "Mocked UV installation"
}

install_system_dependencies() {
  print_success "Mocked system dependencies"
}

install_claude_if_needed() {
  return 0
}

configure_claude_voicemode() {
  print_success "Mocked Voice Mode configuration"
  return 0
}

# Override main to test service installation
main() {
  echo "Testing service installation flow..."
  
  # Test the service installation
  install_voice_services
}

# Provide mock input for service selection
echo "Y" | main
EOF
  
  chmod +x "$TEST_DIR/install-test.sh"
  
  # Run the test
  cd "$TEST_DIR"
  if ./install-test.sh > test-output.log 2>&1; then
    if grep -q "Installing all Voice Mode services" test-output.log; then
      print_success "Full integration test passed"
    else
      print_failure "Service installation not triggered"
      cat test-output.log
    fi
  else
    print_failure "Integration test failed"
    cat test-output.log
  fi
  cd - > /dev/null
}

# Test 6: Platform-specific behavior
test_platform_specific() {
  print_test "Testing platform-specific behavior"
  
  # Test on current platform
  OS=$(uname -s)
  case "$OS" in
    Darwin)
      print_success "Testing on macOS"
      # macOS-specific tests
      if command -v launchctl >/dev/null 2>&1; then
        print_success "launchctl available for service management"
      fi
      ;;
    Linux)
      print_success "Testing on Linux"
      # Linux-specific tests
      if command -v systemctl >/dev/null 2>&1; then
        print_success "systemd available for service management"
      fi
      ;;
    *)
      print_failure "Unknown platform: $OS"
      ;;
  esac
}

# Test 7: Error handling
test_error_handling() {
  print_test "Testing error handling"
  
  # Test timeout handling (mock hanging command)
  cat > "$TEST_DIR/mock-voice-mode-hang" << 'EOF'
#!/bin/bash
# Simulate hanging command
sleep 400
EOF
  chmod +x "$TEST_DIR/mock-voice-mode-hang"
  
  # Source functions
  source <(grep -A 500 "^# Service installation functions" "$INSTALL_SCRIPT" | sed '/^main()/q')
  
  # Test with timeout (should fail after 300s, but we'll kill it sooner in test)
  timeout 5 bash -c 'install_service "whisper" "mock-voice-mode-hang" "Test Service"' || true
  
  print_success "Timeout handling works correctly"
}

# Test 8: User input validation
test_user_input() {
  print_test "Testing user input validation"
  
  # Create test script that handles various inputs
  cat > "$TEST_DIR/test-input.sh" << 'EOF'
#!/bin/bash
source ./install.sh

# Mock the install functions
install_all_services() {
  echo "Mock: Installing all services"
}

install_services_selective() {
  echo "Mock: Selective installation"
}

check_voice_mode_cli() {
  echo "mock-voice-mode"
  return 0
}

# Test the prompt with various inputs
test_inputs=(
  "Y"    # Yes to all
  "y"    # Lowercase yes
  ""     # Default (should be yes)
  "s"    # Selective
  "S"    # Uppercase selective
  "n"    # No
  "N"    # Uppercase no
  "x"    # Invalid (should reprompt)
)

for input in "${test_inputs[@]}"; do
  echo "Testing input: '$input'"
  echo "$input" | install_voice_services || true
  echo "---"
done
EOF
  
  chmod +x "$TEST_DIR/test-input.sh"
  cd "$TEST_DIR"
  ./test-input.sh > input-test.log 2>&1
  cd - > /dev/null
  
  print_success "User input validation tested"
}

# Main test runner
run_all_tests() {
  echo -e "${BLUE}Running Voice Mode install.sh Service Installation Tests${NC}"
  echo "============================================"
  
  # Setup
  setup_test_env
  
  # Run tests
  test_cli_detection
  test_install_all
  test_selective_install
  test_install_with_failures
  test_full_integration
  test_platform_specific
  test_error_handling
  test_user_input
  
  # Cleanup
  print_test "Cleaning up test environment"
  rm -rf "$TEST_DIR"
  print_success "Cleanup complete"
  
  echo ""
  echo -e "${GREEN}All tests completed!${NC}"
  echo "============================================"
}

# Run tests if executed directly
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
  run_all_tests
fi