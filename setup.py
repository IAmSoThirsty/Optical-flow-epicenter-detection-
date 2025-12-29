#!/usr/bin/env python3
"""Setup script for Energetic Epicenter Detector."""

from setuptools import setup, find_packages
from pathlib import Path

# Read README
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name="energetic-epicenter-detector",
    version="1.0.0",
    description="An advanced computer vision engine for detecting energetic event origins in video",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="EED Team",
    author_email="",
    url="https://github.com/IAmSoThirsty/Optical-flow-epicenter-detection-",
    license="MIT",
    
    # Package configuration
    py_modules=["energetic_detector", "epicenter_tool"],
    python_requires=">=3.8",
    
    # Dependencies
    install_requires=[
        "opencv-python>=4.8.0",
        "numpy>=1.24.0",
        "scipy>=1.11.0",
        "matplotlib>=3.7.0",
    ],
    
    # Entry points for command-line tools
    entry_points={
        "console_scripts": [
            "energetic-detector=energetic_detector:main",
            "epicenter-tool=epicenter_tool:main",
        ],
    },
    
    # Classifiers
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Scientific/Engineering :: Image Recognition",
        "Topic :: Scientific/Engineering :: Physics",
        "Topic :: Multimedia :: Video :: Analysis",
    ],
    
    keywords="computer-vision video-analysis optical-flow epicenter-detection fluid-dynamics",
)
