# Development Environment Setup Guide

## Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Git (for version control)
- Docker (optional, for containerized deployment)

## Quick Start

### Option 1: Automated Setup (Recommended)

Run the setup script to automatically configure the environment:

```bash
chmod +x setup.sh
./setup.sh
```

This will:
- Create a virtual environment in `.venv/`
- Install all dependencies
- Install the package in development mode
- Create necessary directories

### Option 2: Manual Setup

1. **Create a virtual environment:**

```bash
python3 -m venv .venv
```

2. **Activate the virtual environment:**

Linux/Mac:
```bash
source .venv/bin/activate
```

Windows:
```bash
.venv\Scripts\activate
```

3. **Install dependencies:**

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

4. **Install the package:**

```bash
pip install -e .
```

### Option 3: Docker Setup

Build and run using Docker:

```bash
# Build the image
docker-compose build

# Run interactive shell
docker-compose run eed bash

# Or analyze a video directly
docker-compose run eed-analyze python energetic_detector.py /videos/your_video.mp4
```

## Project Structure

```
.
├── energetic_detector.py    # Main physics engine and CLI
├── epicenter_tool.py         # AI integration bridge
├── setup.py                  # Package configuration
├── requirements.txt          # Python dependencies
├── setup.sh                  # Automated setup script
├── example_usage.py          # Usage examples
├── Dockerfile                # Docker container definition
├── docker-compose.yml        # Docker services configuration
├── tests/                    # Test suite
│   ├── __init__.py
│   ├── test_detector.py
│   └── test_tool.py
├── epicenter_analysis/       # Output directory (auto-created)
└── README.md                 # Project documentation
```

## Running Tests

After setting up the environment, run the test suite:

```bash
# Activate virtual environment first
source .venv/bin/activate  # or .venv\Scripts\activate on Windows

# Run all tests
python -m unittest discover tests

# Run specific test file
python -m unittest tests.test_detector

# Run with verbose output
python -m unittest discover tests -v
```

## Usage Examples

### Basic Command-Line Usage

```bash
# Analyze a video and show visualizations
python energetic_detector.py path/to/video.mp4

# JSON output for AI integration
python energetic_detector.py path/to/video.mp4 --json

# Process every 3rd frame for faster analysis
python energetic_detector.py path/to/video.mp4 --skip 2

# Custom output directory
python energetic_detector.py path/to/video.mp4 --output-dir my_analysis
```

### Python API Usage

```python
from energetic_detector import EnergeticEpicenterDetector

# Create detector
detector = EnergeticEpicenterDetector(
    "video.mp4",
    output_dir="results",
    skip_frames=1
)

# Analyze video
results = detector.analyze_video(json_output=False)

# Create visualizations
detector.visualize_results()
```

### AI Integration

```python
from epicenter_tool import EpicenterTool

# Create tool
tool = EpicenterTool(output_dir="analysis")

# Analyze single video
results = tool.analyze_video("video.mp4", skip_frames=2)

# Get top epicenter
top = tool.get_top_epicenter("video.mp4")

# Batch process
results = tool.batch_analyze(["video1.mp4", "video2.mp4"])

# Format for LLM
text = tool.format_for_llm(results)
```

## Running Example Code

Try the example script:

```bash
python example_usage.py
```

This will create a synthetic explosion video and demonstrate detection.

## Development Workflow

1. **Activate virtual environment:**
   ```bash
   source .venv/bin/activate
   ```

2. **Make code changes**

3. **Run tests:**
   ```bash
   python -m unittest discover tests
   ```

4. **Test your changes:**
   ```bash
   python energetic_detector.py test_video.mp4
   ```

## Troubleshooting

### OpenCV Issues

If you encounter OpenCV errors on Linux:

```bash
sudo apt-get update
sudo apt-get install -y libglib2.0-0 libsm6 libxext6 libxrender-dev libgomp1 libgl1-mesa-glx
```

### Virtual Environment Not Found

Make sure you've run `setup.sh` or created it manually:

```bash
python3 -m venv .venv
```

### Import Errors

Ensure the package is installed in development mode:

```bash
pip install -e .
```

### Video Codec Issues

If you have trouble with video files, install additional codecs:

```bash
pip install opencv-python-headless  # Alternative without GUI dependencies
```

## Dependencies

Core dependencies (from requirements.txt):
- `opencv-python>=4.8.0` - Computer vision and video processing
- `numpy>=1.24.0` - Numerical computations
- `scipy>=1.11.0` - Scientific computing (for image processing)
- `matplotlib>=3.7.0` - Visualization

## Additional Resources

- [OpenCV Documentation](https://docs.opencv.org/)
- [Optical Flow Tutorial](https://docs.opencv.org/4.x/d4/dee/tutorial_optical_flow.html)
- [Project Repository](https://github.com/IAmSoThirsty/Optical-flow-epicenter-detection-)

## Support

For issues and questions:
1. Check this SETUP.md guide
2. Review the main README.md
3. Check existing GitHub issues
4. Create a new issue with details about your environment and error
