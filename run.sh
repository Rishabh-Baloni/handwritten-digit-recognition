#!/bin/bash

echo "========================================"
echo " Handwritten Digit Recognition Setup"
echo "========================================"
echo

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed"
    echo "Please install Python 3.8+ from https://python.org"
    exit 1
fi

echo "[1/4] Python found - OK"
echo

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "[2/4] Creating virtual environment..."
    python3 -m venv venv
    if [ $? -ne 0 ]; then
        echo "Error: Failed to create virtual environment"
        exit 1
    fi
    echo "Virtual environment created successfully!"
else
    echo "[2/4] Virtual environment already exists - OK"
fi

echo
echo "[3/4] Activating virtual environment and installing dependencies..."
echo "This ensures nothing is installed globally on your system."
echo

# Activate virtual environment
source venv/bin/activate

# Upgrade pip in virtual environment
python -m pip install --upgrade pip

# Install requirements in virtual environment
pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "Error: Failed to install dependencies in virtual environment"
    exit 1
fi

echo
echo "[4/4] Starting the application..."
echo
echo "======================================="
echo " SUCCESS! All dependencies installed "
echo " in virtual environment (venv folder)"
echo "======================================="
echo
echo "The app will open in your default browser."
echo "If it doesn't open automatically, go to: http://localhost:8501"
echo
echo "Press Ctrl+C to stop the application."
echo "To run again, execute: ./run.sh"
echo

# Run the Streamlit app in virtual environment
streamlit run app.py

echo
echo "Application stopped."
