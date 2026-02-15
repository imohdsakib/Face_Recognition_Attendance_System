#!/bin/bash

echo "=========================================="
echo "Face Recognition Attendance System Setup"
echo "=========================================="
echo ""

echo "Checking Python installation..."
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python3 is not installed!"
    echo "Please install Python 3.7 or higher"
    exit 1
fi
python3 --version
echo ""

echo "Creating virtual environment..."
python3 -m venv venv
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to create virtual environment!"
    exit 1
fi
echo ""

echo "Activating virtual environment..."
source venv/bin/activate
echo ""

echo "Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo ""
    echo "WARNING: Some packages failed to install!"
    echo "You may need to install system dependencies:"
    echo ""
    echo "For Ubuntu/Debian:"
    echo "  sudo apt-get update"
    echo "  sudo apt-get install python3-dev cmake"
    echo ""
    echo "For Mac:"
    echo "  brew install cmake"
    echo ""
fi
echo ""

echo "=========================================="
echo "Setup Complete!"
echo "=========================================="
echo ""
echo "To run the application:"
echo "1. Activate virtual environment: source venv/bin/activate"
echo "2. Run the program: python3 main.py"
echo ""
