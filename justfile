set shell := ["powershell.exe", "-c"]

# Show help message
PHONY: help
help:
	@echo "🌟 Welcome to the Awesome Justfile! 🌟"
	@echo ""
	@echo "Available targets:"
	@echo "  - ruff      : Run ruff check without fix 🐶"
	@echo "  - mypy      : Run mypy 🧐"
	@echo "  - isort     : Run isort 🔄"
	@echo "  - audit     : Audit packages 🔍"
	@echo "  - help      : Show this help message ℹ️"

# Run ruff without fix
ruff:
	@echo "🐶 Running ruff check..."
	@ruff check $(git ls-files '*.py')

# Run mypy
mypy:
	@echo "🧐 Running mypy..."
	@poetry run mypy $(git ls-files '*.py')

# Run isort
isort:
	@echo "🔄 Running isort..."
	@poetry run isort $(git ls-files '*.py')

# Audit packages
audit:
	@echo "🔍 Auditing packages..."
	@pip-audit .