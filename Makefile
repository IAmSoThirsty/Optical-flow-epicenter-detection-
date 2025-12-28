.PHONY: help install test clean run example docker-build docker-run

help:
	@echo "Energetic Epicenter Detector - Make Commands"
	@echo ""
	@echo "Available commands:"
	@echo "  make install      - Set up virtual environment and install dependencies"
	@echo "  make test         - Run test suite"
	@echo "  make example      - Run example usage script"
	@echo "  make clean        - Remove build artifacts and cache files"
	@echo "  make docker-build - Build Docker image"
	@echo "  make docker-run   - Run Docker container interactively"
	@echo ""

install:
	@echo "Setting up virtual environment..."
	python3 -m venv .venv
	@echo "Installing dependencies..."
	. .venv/bin/activate && pip install --upgrade pip
	. .venv/bin/activate && pip install -r requirements.txt
	. .venv/bin/activate && pip install -e .
	@echo "✓ Installation complete!"
	@echo "Activate with: source .venv/bin/activate"

test:
	@echo "Running tests..."
	. .venv/bin/activate && python -m unittest discover tests -v

example:
	@echo "Running example script..."
	. .venv/bin/activate && python example_usage.py

clean:
	@echo "Cleaning up..."
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info
	rm -rf .pytest_cache/
	rm -rf .coverage
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	rm -rf epicenter_analysis/
	rm -f synthetic_explosion.mp4
	@echo "✓ Cleanup complete!"

docker-build:
	@echo "Building Docker image..."
	docker compose build

docker-run:
	@echo "Running Docker container..."
	docker compose run --rm eed bash
