# Voice MCP Makefile

.PHONY: help build-package test test-package publish-test publish release install dev-install clean

# Default target
help:
	@echo "Voice MCP Build Targets:"
	@echo ""
	@echo "Development targets:"
	@echo "  install       - Install package in normal mode"
	@echo "  dev-install   - Install package in editable mode with dev dependencies"
	@echo "  test          - Run unit tests with pytest"
	@echo "  clean         - Remove build artifacts and caches"
	@echo ""
	@echo "Python package targets:"
	@echo "  build-package - Build Python package for PyPI"
	@echo "  test-package  - Test package installation"
	@echo "  publish-test  - Publish to TestPyPI"
	@echo "  publish       - Publish to PyPI"
	@echo ""
	@echo "Release targets:"
	@echo "  release       - Create a new release (tags, pushes, triggers GitHub workflow)"
	@echo ""
	@echo "  help          - Show this help message"

# Install package
install:
	@echo "Installing voice-mcp..."
	uv pip install -e .
	@echo "Installation complete!"

# Install package with development dependencies
dev-install:
	@echo "Installing voice-mcp with development dependencies..."
	uv pip install -e ".[dev,test]"
	@echo "Development installation complete!"

# Build Python package
build-package:
	@echo "Building Python package..."
	python -m build
	@echo "Package built successfully in dist/"

# Run unit tests
test:
	@echo "Running unit tests..."
	@if [ ! -d ".venv" ]; then \
		echo "Creating virtual environment..."; \
		uv venv; \
	fi
	@echo "Installing test dependencies..."
	@uv pip install -e ".[test]" -q
	@echo "Running tests..."
	@uv run pytest tests/ -v --tb=short
	@echo "Tests completed!"

# Test package installation
test-package: build-package
	@echo "Testing package installation..."
	cd /tmp && \
	python -m venv test-env && \
	. test-env/bin/activate && \
	pip install $(CURDIR)/dist/voice_mcp-*.whl && \
	voice-mcp --help && \
	deactivate && \
	rm -rf test-env
	@echo "Package test successful!"

# Publish to TestPyPI
publish-test: build-package
	@echo "Publishing to TestPyPI..."
	@echo "Make sure you have configured ~/.pypirc with testpypi credentials"
	python -m twine upload --repository testpypi dist/*
	@echo "Published to TestPyPI. Install with:"
	@echo "  pip install --index-url https://test.pypi.org/simple/ voice-mcp"

# Publish to PyPI
publish: build-package
	@echo "Publishing to PyPI..."
	@echo "Make sure you have configured ~/.pypirc with pypi credentials"
	python -m twine upload dist/*
	@echo "Published to PyPI. Install with:"
	@echo "  pip install voice-mcp"

# Clean build artifacts
clean:
	@echo "Cleaning build artifacts..."
	rm -rf dist/ build/ *.egg-info .pytest_cache __pycache__
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	@echo "Cleanup complete!"

# Release - Create a new release and tag
release:
	@echo "Creating a new release..."
	@echo ""
	@echo "Current version: $$(grep -E '^__version__ = ' voice_mcp/__version__.py | cut -d'"' -f2)"
	@echo ""
	@read -p "Enter new version (e.g., 0.1.3): " version; \
	if [ -z "$$version" ]; then \
		echo "Error: Version cannot be empty"; \
		exit 1; \
	fi; \
	echo "Updating version to $$version..."; \
	sed -i.bak 's/^__version__ = .*/__version__ = "'$$version'"/' voice_mcp/__version__.py && \
	rm voice_mcp/__version__.py.bak; \
	git add voice_mcp/__version__.py && \
	git commit -m "chore: bump version to $$version" && \
	git tag -a "v$$version" -m "Release v$$version" && \
	echo "" && \
	echo "✅ Version bumped and tagged!" && \
	echo "" && \
	echo "Pushing to GitHub..." && \
	git push origin && \
	git push origin "v$$version" && \
	echo "" && \
	echo "🚀 Release pipeline triggered!" && \
	echo "" && \
	echo "GitHub Actions will now:" && \
	echo "1. Create a GitHub release with changelog" && \
	echo "2. Publish to PyPI" && \
	echo "" && \
	echo "Monitor progress at: https://github.com/mbailey/voice-mcp/actions"