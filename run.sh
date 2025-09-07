#!/bin/bash

echo "========================================"
echo "  Handwritten Digit Recognition Setup"
echo "========================================"
echo ""
echo "The app will open in your default browser."
echo "If it doesn't open automatically, go to: http://localhost:5000"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null && ! command -v python &> /dev/null; then
    echo "Error: Python is not installed or not in PATH"
    echo "Please install Python 3.8+ from https://python.org"
    echo "On Ubuntu/Debian: sudo apt install python3 python3-pip python3-venv"
    echo "On macOS: brew install python3"
    exit 1
fi

# Use python3 if available, otherwise use python
if command -v python3 &> /dev/null; then
    PYTHON_CMD="python3"
    PIP_CMD="pip3"
else
    PYTHON_CMD="python"
    PIP_CMD="pip"
fi

echo "[1/4] Python found - OK"
echo ""

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "[2/4] Creating virtual environment..."
    $PYTHON_CMD -m venv venv
    if [ $? -ne 0 ]; then
        echo "Error: Failed to create virtual environment"
        exit 1
    fi
    echo "Virtual environment created successfully!"
else
    echo "[2/4] Virtual environment already exists - OK"
fi

echo ""
echo "[3/4] Activating virtual environment and installing dependencies..."
echo "This ensures nothing is installed globally on your system."
echo ""

# Activate virtual environment
source venv/bin/activate
if [ $? -ne 0 ]; then
    echo "Error: Failed to activate virtual environment"
    exit 1
fi

# Upgrade pip in virtual environment
python -m pip install --upgrade pip

# Install requirements in virtual environment
pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "Error: Failed to install dependencies in virtual environment"
    exit 1
fi

echo ""
echo "[4/4] Starting the application..."
echo ""
echo "======================================="
echo " SUCCESS! All dependencies installed "
echo " in virtual environment (venv folder)"
echo "======================================="
echo ""
echo "The app will open in your default browser."
echo "If it doesn't open automatically, go to: http://localhost:5000"
echo ""
echo "Press Ctrl+C to stop the application."
echo "To run again, execute: ./run.sh"
echo ""

# Run the Flask app in virtual environment
python app.py

echo ""
echo "Application stopped."
