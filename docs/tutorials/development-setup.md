# Development Setup

This guide covers setting up VoiceMode for development, including building from source, configuring your IDE, and contributing to the project.

## Prerequisites

- Python 3.10 or higher
- Git
- UV package manager (recommended) or pip
- Node.js 18+ (for frontend development)

## Setting Up UV

UV is a fast Python package manager written in Rust. It's the recommended tool for VoiceMode development:

```bash
# Install UV
curl -LsSf https://astral.sh/uv/install.sh | sh

# Or using pip
pip install uv
```

## Cloning the Repository

```bash
# Clone the repository
git clone https://github.com/your-username/voice-mode
cd voice-mode

# Install in development mode
uv pip install -e .

# Or using pip
pip install -e .
```

## Development Workflow

### Running from Source

```bash
# Run directly from project directory
uvx .

# Or explicitly specify the command
uvx --from . voice-mode

# Force refresh after code changes
uvx --refresh --from . voice-mode
```

### Building the Package

```bash
# Build the package
uv build

# This creates:
# dist/voice_mode-X.Y.Z-py3-none-any.whl
# dist/voice_mode-X.Y.Z.tar.gz

# Test the built package
uvx --from dist/voice_mode-*.whl voice-mode
```

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=voice_mode

# Run specific test file
pytest tests/test_converse.py

# Run with verbose output
pytest -v
```

## IDE Configuration

### VS Code Setup

Create `.vscode/mcp.json` in your workspace:

```json
{
  "servers": {
    "voice-mode": {
      "type": "stdio",
      "command": "uvx",
      "args": ["--from", ".", "voice-mode"],
      "env": {
        "OPENAI_API_KEY": "${input:openai-api-key}",
        "VOICEMODE_DEBUG": "true"
      }
    }
  },
  "inputs": [
    {
      "type": "promptString",
      "id": "openai-api-key",
      "description": "OpenAI API Key",
      "password": true
    }
  ]
}
```

### PyCharm/IntelliJ Setup

1. Open project settings
2. Configure Python interpreter to use virtual environment
3. Add environment variables:
   - `OPENAI_API_KEY`
   - `VOICEMODE_DEBUG=true`
4. Set working directory to project root

### Recommended Extensions

#### VS Code
- Python (Microsoft)
- Pylance
- Python Test Explorer
- GitLens
- EditorConfig

#### PyCharm
- Python (built-in)
- Markdown support
- .env files support

## Environment Setup

### Development Environment Variables

Create a `.env` file in the project root:

```bash
# Development settings
VOICEMODE_DEBUG=true
VOICEMODE_LOG_LEVEL=debug
VOICEMODE_SAVE_ALL=true

# API keys (optional for local development)
OPENAI_API_KEY=sk-...

# Local service URLs
VOICEMODE_TTS_BASE_URLS=http://127.0.0.1:8880/v1
VOICEMODE_STT_BASE_URLS=http://127.0.0.1:2022/v1

# Development paths
VOICEMODE_DATA_DIR=./dev-data
VOICEMODE_LOG_DIR=./dev-logs
```

### Using Local Services

For development without API keys:

```bash
# Install local services
make install-services

# Or manually
voice-mode whisper install
voice-mode kokoro install

# Start services
make start-services

# Or manually
voice-mode whisper start
voice-mode kokoro start
```

## Frontend Development

### Setup

```bash
# Navigate to frontend directory
cd voice_mode/frontend

# Install dependencies
npm install
# or
pnpm install

# Start development server
npm run dev
```

### Building Frontend

```bash
# Build for production
npm run build

# The built files are included in the Python package
```

### Frontend Environment

Create `voice_mode/frontend/.env.local`:

```bash
# Development settings
NEXT_PUBLIC_LIVEKIT_URL=ws://localhost:7880
LIVEKIT_API_KEY=devkey
LIVEKIT_API_SECRET=secret
LIVEKIT_ACCESS_PASSWORD=dev123
```

## Project Structure

```
voice-mode/
├── voice_mode/           # Main package
│   ├── __init__.py
│   ├── server.py         # MCP server
│   ├── cli.py           # CLI commands
│   ├── config.py        # Configuration
│   ├── tools/           # MCP tools
│   │   ├── converse.py
│   │   └── services/    # Service installers
│   ├── providers.py     # Service providers
│   ├── frontend/        # Next.js frontend
│   └── templates/       # Service templates
├── tests/               # Test suite
├── docs/               # Documentation
├── scripts/            # Development scripts
├── Makefile           # Development tasks
└── pyproject.toml     # Project configuration
```

## Common Development Tasks

### Adding a New Tool

1. Create tool file in `voice_mode/tools/`
2. Implement tool class with MCP decorators
3. Add tests in `tests/tools/`
4. Update documentation

### Modifying Configuration

1. Update `voice_mode/config.py`
2. Add environment variable to docs
3. Update tests for new config
4. Add to example `.env` files

### Updating Dependencies

```bash
# Add a new dependency
uv add requests

# Add development dependency
uv add --dev pytest-mock

# Update all dependencies
uv sync
```

## Debugging

### Enable Debug Mode

```bash
export VOICEMODE_DEBUG=true
export VOICEMODE_LOG_LEVEL=debug
```

### Debug Output Locations

- Logs: `~/.voicemode/logs/`
- Audio files: `~/.voicemode/debug/`
- Event logs: `~/.voicemode/events.log`

### Common Debug Commands

```bash
# Test configuration
voice-mode config test

# Check service status
voice-mode whisper status
voice-mode kokoro status

# View logs
voice-mode logs --tail 50

# Test audio devices
voice-mode audio test
```

## Testing

### Unit Tests

```bash
# Run all unit tests
pytest tests/unit/

# Run with markers
pytest -m "not integration"
```

### Integration Tests

```bash
# Run integration tests
pytest tests/integration/

# Run specific service tests
pytest tests/integration/test_whisper.py
```

### Manual Testing

```bash
# Test voice conversation
voice-mode converse --debug

# Test specific tool
voice-mode test-tool converse

# Test with different providers
VOICEMODE_TTS_BASE_URLS=http://localhost:8880/v1 voice-mode converse
```

## Contributing

### Code Style

We use Black for formatting and Ruff for linting:

```bash
# Format code
black voice_mode tests

# Run linter
ruff check voice_mode tests

# Fix linting issues
ruff check --fix voice_mode tests
```

### Pre-commit Hooks

```bash
# Install pre-commit
pip install pre-commit

# Install hooks
pre-commit install

# Run manually
pre-commit run --all-files
```

### Commit Messages

Follow conventional commits:
- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation
- `test:` Tests
- `refactor:` Code refactoring
- `chore:` Maintenance

### Pull Request Process

1. Fork the repository
2. Create feature branch
3. Make changes with tests
4. Run test suite
5. Submit pull request

## Makefile Commands

```bash
# Development
make dev           # Install in dev mode
make test         # Run tests
make lint         # Run linters
make format       # Format code

# Building
make build        # Build package
make clean        # Clean build artifacts

# Services
make install-services  # Install local services
make start-services   # Start local services
make stop-services    # Stop local services

# Documentation
make docs         # Build documentation
make docs-serve   # Serve docs locally
```

## Troubleshooting Development Issues

### Import Errors

```bash
# Reinstall in editable mode
pip install -e .

# Or with uv
uv pip install -e .
```

### Service Connection Issues

```bash
# Check if ports are in use
lsof -i :8880  # Kokoro
lsof -i :2022  # Whisper
lsof -i :7880  # LiveKit

# Kill stuck processes
pkill -f kokoro
pkill -f whisper
```

### Frontend Build Issues

```bash
# Clean and rebuild
cd voice_mode/frontend
rm -rf node_modules .next
npm install
npm run build
```

## Additional Resources

- [VoiceMode Architecture](../concepts/architecture.md)
- [API Reference](../reference/api.md)
- [Service Development](../concepts/service-model.md)
- [Testing Guide](../guides/testing.md)