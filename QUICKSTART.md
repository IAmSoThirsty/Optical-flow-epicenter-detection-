# Quick Reference Guide

## Installation

### One-Line Setup
```bash
chmod +x setup.sh && ./setup.sh && source .venv/bin/activate
```

### Manual Setup
```bash
python3 -m venv .venv
source .venv/bin/activate  # Linux/Mac
pip install -r requirements.txt
pip install -e .
```

### Using Make
```bash
make install
source .venv/bin/activate
```

## Usage

### Analyze a Video
```bash
# With visualization
python energetic_detector.py video.mp4

# JSON output
python energetic_detector.py video.mp4 --json

# Process every 3rd frame
python energetic_detector.py video.mp4 --skip 2
```

### CLI Tools (after installation)
```bash
energetic-detector video.mp4
epicenter-tool video.mp4 --format llm
```

### Python API
```python
from energetic_detector import EnergeticEpicenterDetector

detector = EnergeticEpicenterDetector("video.mp4")
results = detector.analyze_video()
detector.visualize_results()
```

### AI Integration
```python
from epicenter_tool import EpicenterTool

tool = EpicenterTool()
results = tool.analyze_video("video.mp4")
print(tool.format_for_llm(results))
```

## Testing

```bash
# All tests
python -m unittest discover tests

# Verbose
python -m unittest discover tests -v

# Specific test
python -m unittest tests.test_detector

# Using Make
make test
```

## Examples

```bash
# Run example with synthetic video
python example_usage.py

# Using Make
make example
```

## Docker

```bash
# Build
docker compose build

# Run interactively
docker compose run --rm eed bash

# Analyze a video
docker compose run --rm eed-analyze python energetic_detector.py /videos/video.mp4
```

## Development

```bash
# Run tests
make test

# Clean artifacts
make clean

# Get help
make help
```

## File Overview

| File | Purpose |
|------|---------|
| `energetic_detector.py` | Main detector engine |
| `epicenter_tool.py` | AI integration wrapper |
| `example_usage.py` | Usage examples |
| `requirements.txt` | Python dependencies |
| `setup.py` | Package configuration |
| `setup.sh` | Automated setup |
| `Dockerfile` | Container definition |
| `docker-compose.yml` | Docker services |
| `tests/` | Test suite |
| `README.md` | Full documentation |
| `SETUP.md` | Setup guide |
| `CONTRIBUTING.md` | Contribution guide |
| `Makefile` | Task automation |

## Common Commands

```bash
# Activate environment
source .venv/bin/activate

# Install package
pip install -e .

# Run tests
python -m unittest discover tests

# Run example
python example_usage.py

# Clean up
make clean
```

## Help

```bash
# CLI help
python energetic_detector.py --help
python epicenter_tool.py --help
energetic-detector --help
epicenter-tool --help

# Make help
make help
```

## Output

Default output directory: `epicenter_analysis/`

Generated files:
- `epicenter_heatmap.png` - Visualization with detected epicenters

## Requirements

- Python 3.8+
- opencv-python>=4.8.0
- numpy>=1.24.0
- scipy>=1.11.0
- matplotlib>=3.7.0

## Quick Troubleshooting

**Import Error**: `pip install -e .`

**OpenCV Error (Linux)**: 
```bash
sudo apt-get install libglib2.0-0 libsm6 libxext6 libxrender-dev libgomp1 libgl1
```

**Tests Fail**: Ensure all dependencies installed and environment activated

For more help, see README.md and SETUP.md
