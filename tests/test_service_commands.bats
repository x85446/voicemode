#!/usr/bin/env bats

# Test that service commands can actually run without errors
# This catches runtime bugs that help tests might miss

setup() {
    # Set up test environment
    export PYTHONPATH="${BATS_TEST_DIRNAME}/..:${PYTHONPATH}"
    # Use python -m to run as module
    VOICE_MODE="python -m voice_mode"
}

@test "whisper status command runs without error" {
    # This should not crash with NameError or other runtime errors
    run $VOICE_MODE whisper status
    
    # Check that it didn't crash (exit code 0 or expected non-zero)
    # Note: Status might return non-zero if service is not running, that's OK
    # We're checking it doesn't crash with Python errors (typically exit code 1 with traceback)
    
    # If there's a Python error, it will have "Traceback" in output
    if [[ "$output" == *"Traceback"* ]]; then
        echo "Command crashed with Python error:"
        echo "$output"
        return 1
    fi
    
    # If there's a NameError, catch that specifically
    if [[ "$output" == *"NameError"* ]]; then
        echo "Command has NameError (missing import?):"
        echo "$output"
        return 1
    fi
    
    # Success - command ran without Python errors
    return 0
}

@test "kokoro status command runs without error" {
    run $VOICE_MODE kokoro status
    
    if [[ "$output" == *"Traceback"* ]]; then
        echo "Command crashed with Python error:"
        echo "$output"
        return 1
    fi
    
    if [[ "$output" == *"NameError"* ]]; then
        echo "Command has NameError (missing import?):"
        echo "$output"
        return 1
    fi
    
    return 0
}

@test "livekit status command runs without error" {
    run $VOICE_MODE livekit status
    
    if [[ "$output" == *"Traceback"* ]]; then
        echo "Command crashed with Python error:"
        echo "$output"
        return 1
    fi
    
    if [[ "$output" == *"NameError"* ]]; then
        echo "Command has NameError (missing import?):"
        echo "$output"
        return 1
    fi
    
    return 0
}

@test "config set command runs without error" {
    # Test with a dummy config setting
    run $VOICE_MODE config set TEST_KEY test_value
    
    if [[ "$output" == *"Traceback"* ]]; then
        echo "Command crashed with Python error:"
        echo "$output"
        return 1
    fi
    
    if [[ "$output" == *"NameError"* ]]; then
        echo "Command has NameError (missing import?):"
        echo "$output"
        return 1
    fi
    
    return 0
}

@test "exchanges tail command runs without error" {
    # This should work even if there are no exchanges
    run $VOICE_MODE exchanges tail --lines 1
    
    if [[ "$output" == *"Traceback"* ]]; then
        echo "Command crashed with Python error:"
        echo "$output"
        return 1
    fi
    
    if [[ "$output" == *"NameError"* ]]; then
        echo "Command has NameError (missing import?):"
        echo "$output"
        return 1
    fi
    
    return 0
}

@test "diag command runs without error" {
    run $VOICE_MODE diag
    
    # Diag might not have subcommands, so we just check it doesn't crash
    if [[ "$output" == *"Traceback"* ]] && [[ "$output" != *"Error: Missing command"* ]]; then
        echo "Command crashed with Python error:"
        echo "$output"
        return 1
    fi
    
    if [[ "$output" == *"NameError"* ]]; then
        echo "Command has NameError (missing import?):"
        echo "$output"
        return 1
    fi
    
    return 0
}

# Test that service start/stop/restart don't crash (they might fail due to permissions)
@test "whisper start command doesn't crash with Python errors" {
    run $VOICE_MODE whisper start
    
    # It's OK if it fails due to permissions or service issues
    # We just check it doesn't crash with Python errors
    if [[ "$output" == *"Traceback"* ]] && [[ "$output" != *"Permission denied"* ]]; then
        echo "Command crashed with Python error:"
        echo "$output"
        return 1
    fi
    
    if [[ "$output" == *"NameError"* ]]; then
        echo "Command has NameError (missing import?):"
        echo "$output"
        return 1
    fi
    
    return 0
}

@test "all services have consistent command structure" {
    # Check that all services have the same basic commands
    services=("whisper" "kokoro" "livekit")
    commands=("status" "start" "stop" "restart" "enable" "disable")
    
    for service in "${services[@]}"; do
        for cmd in "${commands[@]}"; do
            # Just check help works for each combination
            run $VOICE_MODE $service $cmd --help
            
            # Should either show help or say command doesn't exist
            # Should NOT crash with Python errors
            if [[ "$output" == *"Traceback"* ]] && [[ "$output" != *"No such command"* ]]; then
                echo "Command $service $cmd crashed:"
                echo "$output"
                return 1
            fi
        done
    done
    
    return 0
}