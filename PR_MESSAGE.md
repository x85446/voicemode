# feat: Add system dependency checking and installation for VoiceMode

## Summary

Implements a lazy-loading dependency management system that checks and installs system dependencies on-demand, replacing the previous monolithic install script approach. This provides a fast initial setup (< 2 minutes) followed by optional enhancements, with automatic detection and installation of missing system packages.

Related: VM-159

## Problem

Users encountered installation failures due to missing system dependencies:
- **webrtcvad compilation failures**: C compiler (gcc) and Python headers required for silence detection
- **Whisper build failures**: Missing cmake, build tools, or audio libraries
- **Kokoro failures on ARM64**: Missing Rust/cargo for compiling sudachipy
- **No feedback**: Users didn't know what was missing or how to fix it
- **WSL audio issues**: PulseAudio not installed or running

## Solution

Implemented a three-phase approach:

### Phase 1: Infrastructure ✅
- **Single source of truth**: `voice_mode/dependencies.yaml` with platform-specific package definitions
- **Dependency checker**: `voice_mode/utils/dependencies/checker.py` with smart in-memory caching
- **Package manager abstraction**: Support for brew (macOS), apt (Debian/Ubuntu), dnf (Fedora)
- **CLI command**: `voicemode deps` to check status and install missing dependencies

### Phase 2: Integration ✅
- **Automatic checks** before service installations:
  - `voicemode converse` → checks core runtime deps (portaudio, ffmpeg, gcc for webrtcvad)
  - `voicemode whisper install` → checks build tools (cmake, gcc, g++, audio dev libs)
  - `voicemode kokoro install` → checks Rust on ARM64, git for cloning
- **Interactive prompts** to install missing dependencies
- **Skip flag**: `--skip-deps` for advanced users who want to handle dependencies manually
- **MCP context detection**: Avoids interactive prompts when running as MCP server

### Phase 3: Testing & Validation ✅
- **18 unit tests** covering dependency detection, caching, and package managers
- **Manual testing on Fedora VM** with clean installation
- **Critical findings**:
  - webrtcvad requires gcc (not g++) + python3-dev(el) for all installations
  - git required for Kokoro (clones repository)
  - Fedora needs gcc-c++ for Whisper builds

## Key Features

### Smart Caching
- **Cache present deps**: Don't recheck if already installed (~2-3ms per check)
- **Recheck missing deps**: In case user installs them externally
- **In-memory only**: No persistent cache needed

### User Experience
```bash
$ voicemode deps
Checking dependencies...
✓ cmake (installed)
✓ gcc (installed)
✗ portaudio-devel (missing) - Audio I/O library

Install missing dependencies? [Y/n]
```

### Platform Support
- **macOS**: Homebrew package manager
- **Ubuntu/Debian**: APT package manager
- **Fedora/RHEL**: DNF package manager
- **WSL**: Automatic PulseAudio detection and setup

## Files Changed

### New Files
- `voice_mode/dependencies.yaml` - Platform-specific dependency manifest (358 lines)
- `voice_mode/utils/dependencies/__init__.py` - Module exports
- `voice_mode/utils/dependencies/cache.py` - In-memory caching logic
- `voice_mode/utils/dependencies/checker.py` - Core dependency checking (223 lines)
- `voice_mode/utils/dependencies/package_managers.py` - Platform abstraction (133 lines)
- `tests/test_dependencies.py` - Comprehensive unit tests (191 lines)

### Modified Files
- `voice_mode/cli.py` - Added dependency checks to commands (+104 lines)
- `voice_mode/tools/converse.py` - Core runtime dep checks (+19 lines)
- `voice_mode/tools/whisper/install.py` - Build tool checks (+30 lines)
- `voice_mode/tools/kokoro/install.py` - Rust/git checks (+38 lines)
- `voice_mode/tools/providers.py` - Terminal context detection (+39 lines)
- `docs/web/install.sh` - Updated Fedora package lists
- Multiple test files - Improved reliability and error messages

## Testing

### Unit Tests (18 tests, all passing)
- Dependency cache behavior (stores present, not missing)
- Platform detection (macOS, Debian, Fedora)
- Package manager abstraction
- Component-specific dependency filtering

### Manual Testing
- ✅ **Fedora 42 VM**: Clean install, deps detection, interactive installation
- ✅ **Critical finding**: Confirmed gcc requirement for webrtcvad compilation
- Pending: Ubuntu VM, macOS, WSL2

### Test Commands
```bash
# Run all dependency tests
uv run pytest tests/test_dependencies.py -v

# Run critical path tests
uv run pytest tests/test_converse_critical_path.py -v

# Full test suite
make test
```

## Breaking Changes

None. All changes are additive:
- Existing commands work unchanged
- New `--skip-deps` flag for opting out
- Automatic dependency checks provide better UX

## Migration Notes

For users upgrading:
1. No action required for basic usage
2. Missing system deps will be auto-detected and offered for installation
3. Use `voicemode deps` to see status of all dependencies
4. Use `--skip-deps` flag if you manage dependencies manually

## Future Work

- [ ] Complete manual testing on Ubuntu VM and WSL2
- [ ] Add dependency checking to LiveKit installer
- [ ] Consider persistent cache file for faster startup
- [ ] Support for more package managers (pacman, zypper)

## Checklist

- [x] Implementation complete and tested
- [x] Unit tests added and passing
- [x] Manual testing on at least one platform
- [x] Documentation updated (dependencies.yaml is self-documenting)
- [x] No breaking changes
- [x] Follows lazy-loading design philosophy
- [x] MCP context detection prevents interactive prompts