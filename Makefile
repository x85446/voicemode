# Voice MCP Makefile

# Detect container runtime
CONTAINER_CMD := $(shell command -v podman 2> /dev/null || command -v docker 2> /dev/null)

.PHONY: help build-container push-container clean test login

# Default target
help:
	@echo "Voice MCP Container Build Targets:"
	@echo "  build-container  - Build the voice-mcp container image"
	@echo "  login           - Login to GitHub Container Registry"
	@echo "  push-container   - Push container to GitHub Container Registry"
	@echo "  test-container   - Test the container locally"
	@echo "  clean           - Remove local container images"
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