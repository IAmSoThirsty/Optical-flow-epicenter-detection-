#!/bin/bash
# Setup script for Energetic Epicenter Detector
# This script sets up the development environment

set -e

echo "=== Energetic Epicenter Detector Setup ==="
echo ""

# Check Python version
PYTHON_CMD="python3"
if ! command -v $PYTHON_CMD &> /dev/null; then
    PYTHON_CMD="python"
    if ! command -v $PYTHON_CMD &> /dev/null; then
        echo "Error: Python 3 is not installed"
        exit 1
    fi
fi

PYTHON_VERSION=$($PYTHON_CMD --version 2>&1 | awk '{print $2}')
echo "Found Python: $PYTHON_VERSION"

# Check if Python version is 3.8+
PYTHON_MAJOR=$($PYTHON_CMD -c "import sys; print(sys.version_info.major)")
PYTHON_MINOR=$($PYTHON_CMD -c "import sys; print(sys.version_info.minor)")

if [ "$PYTHON_MAJOR" -lt 3 ] || ([ "$PYTHON_MAJOR" -eq 3 ] && [ "$PYTHON_MINOR" -lt 8 ]); then
    echo "Error: Python 3.8 or higher is required"
    exit 1
fi

echo "✓ Python version is compatible"
echo ""

# Create virtual environment
echo "Creating virtual environment..."
if [ ! -d ".venv" ]; then
    $PYTHON_CMD -m venv .venv
    echo "✓ Virtual environment created"
else
    echo "✓ Virtual environment already exists"
fi
echo ""

# Activate virtual environment
echo "To activate the virtual environment, run:"
echo "  source .venv/bin/activate  (Linux/Mac)"
echo "  .venv\\Scripts\\activate     (Windows)"
echo ""

# Install dependencies
echo "Installing dependencies..."
if [ -f ".venv/bin/activate" ]; then
    source .venv/bin/activate
elif [ -f ".venv/Scripts/activate" ]; then
    source .venv/Scripts/activate
fi

pip install --upgrade pip
pip install -r requirements.txt
pip install -e .

echo "✓ Dependencies installed"
echo ""

# Create output directory
mkdir -p epicenter_analysis
echo "✓ Output directory created"
echo ""

echo "=== Setup Complete ==="
echo ""
echo "Next steps:"
echo "1. Activate the virtual environment (see command above)"
echo "2. Run the detector: python energetic_detector.py --help"
echo "3. Or use Docker: docker-compose build"
echo ""
