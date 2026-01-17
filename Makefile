.PHONY: help install install-dev install-all setup test test-cov lint format typecheck clean build publish

PYTHON := python3
PIP := pip

help:
	@echo "taocore-human - Development Commands"
	@echo ""
	@echo "Setup:"
	@echo "  make install       Install package (basic)"
	@echo "  make install-dev   Install with dev dependencies"
	@echo "  make install-all   Install with all optional dependencies"
	@echo "  make setup         Full dev setup (install-all + pre-commit)"
	@echo ""
	@echo "Testing:"
	@echo "  make test          Run tests"
	@echo "  make test-cov      Run tests with coverage report"
	@echo "  make test-verbose  Run tests with verbose output"
	@echo ""
	@echo "Code Quality:"
	@echo "  make lint          Run linter (ruff)"
	@echo "  make format        Format code (ruff)"
	@echo "  make typecheck     Run type checker (mypy)"
	@echo "  make check         Run all checks (lint + typecheck + test)"
	@echo ""
	@echo "Build & Publish:"
	@echo "  make build         Build package"
	@echo "  make publish       Publish to PyPI"
	@echo "  make publish-test  Publish to TestPyPI"
	@echo ""
	@echo "Maintenance:"
	@echo "  make clean         Remove build artifacts"
	@echo "  make clean-all     Remove all generated files"

# Setup targets
install:
	$(PIP) install -e .

install-dev:
	$(PIP) install -e ".[dev]"

install-image:
	$(PIP) install -e ".[image]"

install-video:
	$(PIP) install -e ".[video]"

install-ml:
	$(PIP) install -e ".[ml]"

install-all:
	$(PIP) install -e ".[dev,video,ml]"

setup: install-all
	@echo "Development environment ready!"

# Testing targets
test:
	pytest tests/ -v

test-cov:
	pytest tests/ -v --cov=src/taocore_human --cov-report=term-missing --cov-report=html

test-verbose:
	pytest tests/ -vv -s

test-fast:
	pytest tests/ -v -x --ff

# Code quality targets
lint:
	ruff check src/ tests/

lint-fix:
	ruff check src/ tests/ --fix

format:
	ruff format src/ tests/

format-check:
	ruff format src/ tests/ --check

typecheck:
	mypy src/taocore_human

check: lint typecheck test
	@echo "All checks passed!"

# Build targets
build: clean
	$(PYTHON) -m build

publish: build
	twine upload dist/*

publish-test: build
	twine upload --repository testpypi dist/*

# Clean targets
clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	rm -rf src/*.egg-info/
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true

clean-all: clean
	rm -rf .pytest_cache/
	rm -rf .mypy_cache/
	rm -rf .ruff_cache/
	rm -rf htmlcov/
	rm -rf .coverage
	rm -rf .tox/
	rm -rf .venv/
