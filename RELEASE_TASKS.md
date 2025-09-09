# Voice Mode Release Tasks

## Decisions from Discussion

### Issue 1: Installation Difficulty
**Solution**: Simple, reliable path using cloud services first
- UV as primary install method (`uvx voicemode` or `uvx --refresh voicemode`)
- pip install as fallback for those who prefer it
- NO local services in initial setup

### Issue 2: Rate Limiting & Server Issues
**Solution**: Separate install scripts, make local services optional
- Users must explicitly choose to install local services
- Clear documentation that users are responsible for managing them
- OpenAI API is the default and recommended path

### Issue 3: Complex Setup
**Solution**: Already addressed by simplified path above

### Issue 4: Token Overhead (10k+ tokens)
**Solution**: Use VOICEMODE_TOOLS environment variable
- Already implemented in safety-commit-2025-01-09 branch
- Allows loading only specific tools (e.g., just `converse`)
- Saves ~20,000 tokens

### Issue 5: Servers Not Gracefully Shutting Down
**Solution**: Don't auto-install services
- Services are system-level (launchd/systemd)
- Users must explicitly install and understand implications
- Problem avoided by not including in default install

### Issue 6: Docker Environment
**Decision**: NO Docker
- Would lose Apple Silicon acceleration on Mac
- Creates worse experience than native install
- Not recommended

## Priority 1: Simplify Initial Setup

### Installation Simplification
- [ ] Focus README primarily on Claude Code installation methods
  - `uvx voicemode` or `uvx --refresh voicemode` (preferred for auto-updates)
  - `uv tool install voicemode`
  - `pip install voicemode` (as fallback)
- [ ] Remove curl|bash from primary docs (keep but de-emphasize)
- [ ] Make OpenAI API the only initial path
- [ ] Add clear messaging: "Cloud first, local services are advanced option"

### Documentation Updates
- [ ] Streamline README.md
  - Quick start with UV/pip only
  - OpenAI API setup as the primary path
  - Move ALL local services to "Advanced" section
  - Focus entirely on Claude Code users
- [ ] Document VOICEMODE_TOOLS environment variable prominently
  - Example: `VOICEMODE_TOOLS=converse` saves 20k tokens
- [ ] Remove local services from main documentation flow

## Priority 2: Better Error Handling & Support

### GitHub Issue Template
- [ ] Create `.github/ISSUE_TEMPLATE/setup-problem.md`
- [ ] Include diagnostic commands
- [ ] Capture OS, Python version, installation method
- [ ] Add checklist for common issues

### Telemetry (Privacy-Respecting)
- [ ] Add opt-in telemetry for installation success/failure
- [ ] Track: OS type, Python version, installation method, Claude Code vs other
- [ ] No personal data, no usage tracking
- [ ] Install script writes log to file
- [ ] Ask user permission to upload log after install
- [ ] Allow user to view log contents before deciding
- [ ] Help identify common setup problems
- [ ] Consider usage telemetry for failures (with consent)

## Priority 3: Technical Improvements

### Core Changes
- [ ] Merge safety-commit-2025-01-09 branch for VOICEMODE_TOOLS
- [ ] Remove local services from install.sh completely
- [ ] Create separate documentation for local services installation

### Installation Flow
- [ ] Simplify install.sh to ONLY install the Python package
- [ ] Add OpenAI API key configuration helper
- [ ] Test audio devices on first run
- [ ] NO automatic service installation

## Priority 4: Infrastructure

### voicemode.sh Domain
- [ ] Set up voicemode.sh for curl|bash installation
- [ ] Configure DNS and hosting
- [ ] Create install script that redirects to GitHub
- [ ] Add version detection and upgrade path

## Testing Checklist
- [ ] Test fresh install with `uvx voicemode`
- [ ] Test fresh install with `pip install voicemode`
- [ ] Test upgrade path from previous version
- [ ] Test fallback from local services to OpenAI
- [ ] Test on macOS, Linux, WSL
- [ ] Verify Claude Code integration works smoothly

## Release Steps
1. Complete Priority 1 & 2 items
2. Run test checklist
3. Bump version in pyproject.toml
4. Update CHANGELOG.md
5. Create git tag
6. Push to GitHub
7. Publish to PyPI
8. Update voicemode.sh install script
9. Submit updated PR to awesome-claude-code

## Notes from mbailey's Comment
- Focus on making it work "out of the box" with OpenAI API
- Local services become an optional upgrade for privacy
- Issue template helps gather debugging info
- VOICEMODE_TOOLS helps with token efficiency
- 4-day weekend work on whisper/kokoro single script installer