@echo off
echo ==========================================
echo Face Recognition Attendance System Setup
echo ==========================================
echo.

echo Checking Python installation...
python --version
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH!
    echo Please install Python 3.7 or higher from https://www.python.org/
    pause
    exit /b 1
)
echo.

echo Creating virtual environment...
python -m venv venv
if errorlevel 1 (
    echo ERROR: Failed to create virtual environment!
    pause
    exit /b 1
)
echo.

echo Activating virtual environment...
call venv\Scripts\activate.bat
echo.

echo Installing dependencies...
pip install --upgrade pip
pip install -r requirements.txt
if errorlevel 1 (
    echo.
    echo WARNING: Some packages failed to install!
    echo You may need to install Visual Studio Build Tools for Windows
    echo Download from: https://visualstudio.microsoft.com/downloads/
    echo Then select "Desktop development with C++" workload
    echo.
)
echo.

echo ==========================================
echo Setup Complete!
echo ==========================================
echo.
echo To run the application:
echo 1. Activate virtual environment: venv\Scripts\activate
echo 2. Run the program: python main.py
echo.
pause
