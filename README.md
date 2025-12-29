
# Energetic Epicenter Detector (EED)

An advanced computer vision engine designed to detect and triangulate the origin of energetic events (impacts, explosions, shockwaves) within video feeds. Unlike basic motion detection, EED uses fluid dynamics principles to map kinetic energy propagation.

## 🚀 The Core Idea
EED treats video frames as a fluid field. By calculating the **Divergence** (expansion), **Curl** (rotation), and **Strain Tensors** (deformation) of pixels, the system can distinguish between a simple moving object and a true energetic source.

## 🛠 Features
* **Kinetic Analysis:** Measures real-time energy propagation via Farneback Optical Flow.
* **Temporal Logic:** Weights early detections to find the *source* of an event, ignoring secondary smoke or debris.
* **AI-Ready:** Includes a specialized tool wrapper (`epicenter_tool.py`) for seamless integration into AI agents and forensic workflows.
* **Multi-View Support:** Framework included for 3D triangulation using multiple camera angles.
* **Comprehensive Testing:** Full test suite included for reliable operation.
* **Docker Support:** Containerized deployment with Docker and Docker Compose.

## 📦 Installation

### Quick Start (Recommended)

Run the automated setup script:

```bash
chmod +x setup.sh
./setup.sh
```

This will create a virtual environment, install all dependencies, and set up the package.

### Manual Installation

Ensure you have Python 3.8+ installed.

1. **Clone the repository**:
   ```bash
   git clone https://github.com/IAmSoThirsty/Optical-flow-epicenter-detection-.git
   cd Optical-flow-epicenter-detection-
   ```

2. **Create and activate virtual environment**:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate  # Linux/Mac
   # or
   .venv\Scripts\activate     # Windows
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   pip install -e .
   ```

### Docker Installation

Build and run using Docker:

```bash
# Build the image
docker-compose build

# Run interactive shell
docker-compose run eed bash

# Or analyze a video
docker-compose run eed-analyze python energetic_detector.py /videos/your_video.mp4
```

## 🖥 Usage

### As a Standalone Tool

To analyze a video and see the visual heatmap:

```bash
python energetic_detector.py path/to/your/video.mp4
```

With options:

```bash
# JSON output for AI integration
python energetic_detector.py path/to/video.mp4 --json

# Process every 3rd frame for faster analysis
python energetic_detector.py path/to/video.mp4 --skip 2

# Custom output directory
python energetic_detector.py path/to/video.mp4 --output-dir my_results
```

### Integration with an AI Agent

Using the epicenter tool:

```bash
# Get analysis in JSON format
python epicenter_tool.py path/to/video.mp4 --format json

# Get LLM-friendly text output
python epicenter_tool.py path/to/video.mp4 --format llm
```

### Python API

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

For AI integration:

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

## 📂 Project Structure

```
.
├── energetic_detector.py    # Main physics engine and CLI
├── epicenter_tool.py         # AI integration bridge
├── example_usage.py          # Usage examples with synthetic demo
├── setup.py                  # Package configuration
├── requirements.txt          # Python dependencies
├── setup.sh                  # Automated setup script
├── Dockerfile                # Docker container definition
├── docker-compose.yml        # Docker services configuration
├── .gitignore               # Git ignore patterns
├── .dockerignore            # Docker ignore patterns
├── tests/                    # Test suite
│   ├── __init__.py
│   ├── test_detector.py     # Detector tests
│   └── test_tool.py         # Tool wrapper tests
├── epicenter_analysis/       # Output directory (auto-created)
├── SETUP.md                  # Detailed setup guide
└── README.md                 # This file
```

## 🧪 Testing

Run the test suite:

```bash
# Activate virtual environment
source .venv/bin/activate

# Run all tests
python -m unittest discover tests

# Run with verbose output
python -m unittest discover tests -v

# Run specific test file
python -m unittest tests.test_detector
```

## 📚 Examples

Run the example script to see a demonstration with a synthetic explosion video:

```bash
python example_usage.py
```

This will:
1. Create a synthetic explosion video
2. Analyze it to detect the epicenter
3. Report the detection accuracy

## 🔧 Dependencies

Core dependencies:
- `opencv-python>=4.8.0` - Computer vision and video processing
- `numpy>=1.24.0` - Numerical computations
- `scipy>=1.11.0` - Scientific computing
- `matplotlib>=3.7.0` - Visualization

All dependencies are automatically installed via `requirements.txt`.

## 📖 Documentation

For detailed setup instructions, see [SETUP.md](SETUP.md).

## 🤝 Contributing

Contributions are welcome! Please ensure:
1. All tests pass: `python -m unittest discover tests`
2. Code follows existing style conventions
3. New features include appropriate tests

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🐛 Troubleshooting

### OpenCV Issues on Linux

If you encounter OpenCV errors:

```bash
sudo apt-get update
sudo apt-get install -y libglib2.0-0 libsm6 libxext6 libxrender-dev libgomp1 libgl1
```

### Import Errors

Ensure the package is installed:

```bash
pip install -e .
```

### Virtual Environment Issues

Make sure you've activated the virtual environment:

```bash
source .venv/bin/activate  # Linux/Mac
.venv\Scripts\activate     # Windows
```

## 📧 Support

For issues and questions:
1. Check the [SETUP.md](SETUP.md) guide
2. Review existing GitHub issues
3. Create a new issue with details about your environment


