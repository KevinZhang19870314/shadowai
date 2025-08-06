# ShadowAI Makefile
# Simplify common development, testing and publishing operations

.PHONY: help install install-dev test lint format clean build publish quickstart example

# Default target
help: ## Show help information
	@echo "ShadowAI Project Common Commands:"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

# Install dependencies
install: ## Install production dependencies
	pip install -r requirements.txt

install-dev: ## Install development dependencies
	pip install -r requirements-dev.txt

# Code quality
format: ## Format code
	black .
	isort .

lint: ## Check code quality
	black --check .
	isort --check-only .
	flake8 .
	mypy lib/

fix-formatting: ## Auto-fix formatting issues
	python scripts/fix_formatting.py

# Testing
test: ## Run tests
	python -m pytest tests/ -v

test-cov: ## Run tests and generate coverage report
	python -m pytest tests/ --cov=shadowai --cov-report=html --cov-report=term

# Cleanup
clean: ## Clean build files
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	rm -rf .pytest_cache/
	rm -rf htmlcov/
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

# Build
build: clean ## Build package
	python -m build

check: ## Check package
	python -m twine check dist/*

# Publishing
publish-test: build check ## Publish to test PyPI
	twine upload --repository testpypi dist/*

publish: build check ## Publish to PyPI (manual, prefer using release workflow)
	twine upload dist/*

# Release management
release: ## Create a new release (usage: make release VERSION=0.1.3)
	@if [ -z "$(VERSION)" ]; then echo "❌ VERSION is required. Usage: make release VERSION=0.1.3"; exit 1; fi
	python scripts/release.py $(VERSION)

release-check: ## Check if ready for release
	@echo "🔍 Checking release readiness..."
	@git status --porcelain | head -5
	@echo "📋 Recent commits:"
	@git log --oneline -5
	@echo "🏷️ Current version: $(shell make version)"
	@echo "📦 Current tags:"
	@git tag -l | tail -5

release-dry-run: ## Test release process without publishing
	@echo "🧪 Dry run: Testing release process"
	python -m build
	python -m twine check dist/*
	@echo "✅ Package build successful - ready for release"

# Quick start and examples
quickstart: ## Run quickstart wizard
	python scripts/quickstart.py

example-basic: ## Run basic example
	python example/basic_usage.py

example-custom: ## Run custom rules example
	python example/custom_rules.py

example-file: ## Run file operations example
	python example/file_loading.py

# Development
dev: install-dev format ## Setup development environment

# Version management
version: ## Show current version
	@grep 'version = ' pyproject.toml | cut -d'"' -f2

bump-patch: ## Increment patch version
	@echo "TODO: Implement automatic version increment"

bump-minor: ## Increment minor version
	@echo "TODO: Implement automatic version increment"

bump-major: ## Increment major version
	@echo "TODO: Implement automatic version increment"

# Documentation
docs: ## Generate documentation
	@echo "TODO: Implement documentation generation"

docs-serve: ## Start documentation server
	@echo "TODO: Implement documentation server"

# Complete workflow
all: clean format lint test build check ## Run complete CI workflow

# Project information
info: ## Show project information
	@echo "ShadowAI - AI-driven Mock data generation library"
	@echo "Version: $(shell make version)"
	@echo "Python: $(shell python --version)"
	@echo "Dependency check:"
	@python -c "import agno; print('  ✓ agno')" 2>/dev/null || echo "  ✗ agno"
	@python -c "import pydantic; print('  ✓ pydantic')" 2>/dev/null || echo "  ✗ pydantic"
	@python -c "import yaml; print('  ✓ pyyaml')" 2>/dev/null || echo "  ✗ pyyaml" 