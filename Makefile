# Voice MCP Makefile

# Detect container runtime
CONTAINER_CMD := $(shell command -v podman 2> /dev/null || command -v docker 2> /dev/null)

.PHONY: help build-container push-container clean test login build-package test-package publish-test publish

# Default target
help:
	@echo "Voice MCP Build Targets:"
	@echo ""
	@echo "Container targets:"
	@echo "  build-container  - Build the voice-mcp container image"
	@echo "  login           - Login to GitHub Container Registry"
	@echo "  push-container   - Push container to GitHub Container Registry"
	@echo "  test-container   - Test the container locally"
	@echo "  clean           - Remove local container images"
	@echo ""
	@echo "Python package targets:"
	@echo "  build-package    - Build Python package for PyPI"
	@echo "  test-package     - Test package installation"
	@echo "  publish-test     - Publish to TestPyPI"
	@echo "  publish          - Publish to PyPI"
	@echo ""
	@echo "  help            - Show this help message"

# Build the container image
build-container:
	@echo "Building voice-mcp container..."
	$(CONTAINER_CMD) build -f Containerfile -t voice-mcp:latest .
	@echo "Container built successfully: voice-mcp:latest"

# Login to GitHub Container Registry
login:
	@echo "Logging in to GitHub Container Registry..."
	@echo "You'll need a GitHub Personal Access Token with 'write:packages' scope"
	@echo "Get one at: https://github.com/settings/tokens"
	@read -p "GitHub username: " username; \
	$(CONTAINER_CMD) login ghcr.io -u $$username
	@echo "Login successful!"

# Tag and push to GitHub Container Registry
push-container: build-container
	@echo "Tagging for GitHub Container Registry..."
	$(CONTAINER_CMD) tag voice-mcp:latest ghcr.io/mbailey/voice-mcp:latest
	@echo "Pushing to GitHub Container Registry..."
	$(CONTAINER_CMD) push ghcr.io/mbailey/voice-mcp:latest
	@echo "Container pushed successfully"

# Test the container locally
test-container: build-container
	@echo "Testing container with basic configuration..."
	@echo "Note: Requires OPENAI_API_KEY environment variable"
	$(CONTAINER_CMD) run --rm -e OPENAI_API_KEY=${OPENAI_API_KEY} -e VOICE_MCP_DEBUG=true voice-mcp:latest --help || echo "Container test complete"

# Clean up local images
clean:
	@echo "Removing local voice-mcp container images..."
	$(CONTAINER_CMD) rmi voice-mcp:latest ghcr.io/mbailey/voice-mcp:latest 2>/dev/null || true
	@echo "Cleanup complete"

# Python Package Targets

# Build Python package
build-package:
	@echo "Building Python package..."
	cd python-package && python -m build
	@echo "Package built successfully in python-package/dist/"

# Test package installation
test-package: build-package
	@echo "Testing package installation..."
	cd /tmp && \
	python -m venv test-env && \
	. test-env/bin/activate && \
	pip install $(CURDIR)/python-package/dist/voice_mcp-*.whl && \
	voice-mcp --help && \
	livekit-admin-mcp --help && \
	deactivate && \
	rm -rf test-env
	@echo "Package test successful!"

# Publish to TestPyPI
publish-test: build-package
	@echo "Publishing to TestPyPI..."
	@echo "Make sure you have configured ~/.pypirc with testpypi credentials"
	cd python-package && python -m twine upload --repository testpypi dist/*
	@echo "Published to TestPyPI. Install with:"
	@echo "  pip install --index-url https://test.pypi.org/simple/ voice-mcp"

# Publish to PyPI
publish: build-package
	@echo "Publishing to PyPI..."
	@echo "Make sure you have configured ~/.pypirc with pypi credentials"
	cd python-package && python -m twine upload dist/*
	@echo "Published to PyPI. Install with:"
	@echo "  pip install voice-mcp"