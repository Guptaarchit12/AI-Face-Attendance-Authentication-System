#!/bin/bash

# Face Attendance System - Setup Script
# This script automates the installation process

echo "=================================================="
echo "  Face Attendance System - Setup"
echo "=================================================="
echo ""

# Check Python version
echo "Checking Python version..."
python3 --version

if [ $? -ne 0 ]; then
    echo "Error: Python 3 is not installed. Please install Python 3.7 or higher."
    exit 1
fi

# Create virtual environment
echo ""
echo "Creating virtual environment..."
python3 -m venv venv

if [ $? -ne 0 ]; then
    echo "Error: Failed to create virtual environment."
    exit 1
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo ""
echo "Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo ""
echo "Installing dependencies..."
echo "This may take several minutes..."

# Install cmake first (required for dlib)
pip install cmake

# Install numpy (required for face_recognition)
pip install numpy

# Install dlib
echo ""
echo "Installing dlib (this may take a while)..."
pip install dlib

if [ $? -ne 0 ]; then
    echo ""
    echo "Warning: dlib installation failed."
    echo "You may need to install system dependencies first:"
    echo ""
    echo "For Ubuntu/Debian:"
    echo "  sudo apt-get update"
    echo "  sudo apt-get install -y build-essential cmake"
    echo "  sudo apt-get install -y python3-dev"
    echo ""
    echo "For macOS:"
    echo "  brew install cmake"
    echo ""
    echo "Then run this script again."
    exit 1
fi

# Install remaining packages
pip install opencv-python
pip install face-recognition
pip install pillow

# Create data directory
echo ""
echo "Creating data directory..."
mkdir -p data

# Test installation
echo ""
echo "Testing installation..."
python3 -c "import cv2; import face_recognition; print('✓ All packages installed successfully!')"

if [ $? -eq 0 ]; then
    echo ""
    echo "=================================================="
    echo "  Setup Complete!"
    echo "=================================================="
    echo ""
    echo "To run the system:"
    echo "  1. Activate virtual environment: source venv/bin/activate"
    echo "  2. Run the program: python attendance_system.py"
    echo ""
    echo "To run the demo (without camera): python demo.py"
    echo ""
else
    echo ""
    echo "Error: Installation test failed."
    echo "Please check the error messages above."
    exit 1
fi
