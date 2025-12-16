

# Energetic Epicenter Detector (EED)

An advanced computer vision engine designed to detect and triangulate the origin of energetic events (impacts, explosions, shockwaves) within video feeds. Unlike basic motion detection, EED uses fluid dynamics principles to map kinetic energy propagation.

## 🚀 The Core Idea
EED treats video frames as a fluid field. By calculating the **Divergence** (expansion), **Curl** (rotation), and **Strain Tensors** (deformation) of pixels, the system can distinguish between a simple moving object and a true energetic source.

## 🛠 Features
* **Kinetic Analysis:** Measures real-time energy propagation via Farneback Optical Flow.
* **Temporal Logic:** Weights early detections to find the *source* of an event, ignoring secondary smoke or debris.
* **AI-Ready:** Includes a specialized tool wrapper (`epicenter_tool.py`) for seamless integration into AI agents and forensic workflows.
* **Multi-View Support:** Framework included for 3D triangulation using multiple camera angles.

## 📦 Installation

Ensure you have Python 3.8+ installed.

1. **Clone or download** this repository.
2. **Install the dependencies**:
   ```bash
   pip install opencv-python numpy scipy matplotlib

🖥 Usage
As a Standalone Tool
To analyze a video and see the visual heatmap:
python energetic_detector.py path/to/your/video.mp4

Integration with an AI Agent
To run the detector in "Silent/JSON" mode so your AI can read the data:
python energetic_detector.py path/to/video.mp4 --json --skip 2

📂 Project Structure
 * energetic_detector.py: The main physics engine and CLI.
 * epicenter_tool.py: The bridge class for AI integration.
 * epicenter_analysis/: Default directory for output heatmaps and trajectory plots.


