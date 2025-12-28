FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies for OpenCV
RUN apt-get update && apt-get install -y \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libgomp1 \
    libgl1-mesa-glx \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY energetic_detector.py .
COPY epicenter_tool.py .
COPY setup.py .
COPY README.md .

# Create output directory
RUN mkdir -p epicenter_analysis

# Install the package
RUN pip install -e .

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Default command
CMD ["python", "energetic_detector.py", "--help"]
