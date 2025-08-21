#!/bin/bash
# Format and lint all Python code

set -e

echo "🧹 Formatting and linting SmartDoc code..."

# Format with black
echo "Running black..."
black packages/ apps/ tests/ --line-length 88

# Sort imports with isort
echo "Running isort..."
isort packages/ apps/ tests/ --profile black

# Lint with ruff
echo "Running ruff..."
ruff check packages/ apps/ tests/ --fix

echo "✅ Code formatting and linting complete!"
