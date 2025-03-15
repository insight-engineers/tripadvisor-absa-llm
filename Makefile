.PHONY: install format demo

install:
	@echo "Installing..."
	@uv sync

format:
	@echo "Formatting with ruff, isort, and black..."
	@uv run ruff format absa
	@uv run black absa
	@uv run isort --profile black absa

demo:
	@echo "Starting UI..."
	@uv run python3 absa/demo.py