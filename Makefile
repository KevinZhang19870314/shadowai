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
	black lib/ example/ scripts/
	isort lib/ example/ scripts/

lint: ## Check code quality
	black --check lib/
	isort --check-only lib/
	flake8 lib/
	mypy lib/ --ignore-missing-imports

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
	python scripts/publish.py --test --skip-tests

publish: build check ## Publish to PyPI
	python scripts/publish.py --skip-tests

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