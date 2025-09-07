@echo off
echo ========================================
echo   Handwritten Digit Recognition Setup
echo ========================================
echo.
echo The app will open in your default browser.
echo If it doesn't open automatically, go to: http://localhost:5000
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Error: Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://python.org
    pause
    exit /b 1
)

echo [1/4] Python found - OK
echo.

REM Create virtual environment if it doesn't exist
if not exist "venv" (
    echo [2/4] Creating virtual environment...
    python -m venv venv
    if %errorlevel% neq 0 (
        echo Error: Failed to create virtual environment
        pause
        exit /b 1
    )
    echo Virtual environment created successfully!
) else (
    echo [2/4] Virtual environment already exists - OK
)

echo.
echo [3/4] Activating virtual environment and installing dependencies...
echo This ensures nothing is installed globally on your system.
echo.

REM Activate virtual environment and install dependencies
call venv\Scripts\activate.bat
if %errorlevel% neq 0 (
    echo Error: Failed to activate virtual environment
    pause
    exit /b 1
)

REM Upgrade pip in virtual environment
python -m pip install --upgrade pip

REM Install requirements in virtual environment
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo Error: Failed to install dependencies in virtual environment
    pause
    exit /b 1
)

echo.
echo [4/4] Starting the application...
echo.
echo =======================================
echo  SUCCESS! All dependencies installed 
echo  in virtual environment (venv folder)
echo =======================================
echo.
echo The app will open in your default browser.
echo If it doesn't open automatically, go to: http://localhost:5000
echo.
echo Press Ctrl+C to stop the application.
echo To run again, just double-click this file.
echo.

REM Run the Flask app in virtual environment
python app.py

echo.
echo Application stopped.
pause
