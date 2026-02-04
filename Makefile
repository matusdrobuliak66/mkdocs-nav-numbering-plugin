.PHONY: help install install-dev serve build clean lint format test

# Default target
help:
	@echo "Available commands:"
	@echo "  make install      - Install the plugin in editable mode"
	@echo "  make install-dev  - Install with dev dependencies (lint, test, etc.)"
	@echo "  make serve        - Start MkDocs dev server"
	@echo "  make build        - Build the documentation site"
	@echo "  make clean        - Remove build artifacts"
	@echo "  make lint         - Run linters (ruff)"
	@echo "  make format       - Format code (ruff)"
	@echo "  make test         - Run tests"

# Install plugin in editable mode
install:
	pip install -e .

# Install with development dependencies
install-dev:
	pip install -e ".[dev]"
	pip install ruff pytest pytest-cov

# Start MkDocs development server
serve:
	mkdocs serve

# Build documentation site
build:
	mkdocs build

# Clean build artifacts
clean:
	rm -rf site/
	rm -rf dist/
	rm -rf build/
	rm -rf *.egg-info/
	rm -rf src/*.egg-info/
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete

# Lint code
lint:
	ruff check src/

# Format code
format:
	ruff format src/
	ruff check --fix src/

# Run tests
test:
	pytest tests/ -v

# Run tests with coverage
test-cov:
	pytest tests/ -v --cov=src/mkdocs_nav_numbering_plugin --cov-report=html

