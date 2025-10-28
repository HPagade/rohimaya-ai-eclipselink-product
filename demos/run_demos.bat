@echo off
REM EclipseLink AI Demo Runner for Windows
REM Quick start script for running the demo suite locally

echo.
echo 🦚 EclipseLink AI - Demo Suite
echo ================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed. Please install Python 3.8 or higher.
    pause
    exit /b 1
)

echo ✅ Python detected
echo.

REM Check if pip is installed
pip --version >nul 2>&1
if errorlevel 1 (
    echo ❌ pip is not installed. Please install pip.
    pause
    exit /b 1
)

echo ✅ pip detected
echo.

REM Check if in demos directory
if not exist "Home.py" (
    echo ❌ Error: Home.py not found. Please run this script from the demos directory.
    echo    cd demos
    echo    run_demos.bat
    pause
    exit /b 1
)

REM Check if virtual environment exists
if not exist "venv\" (
    echo 📦 Creating virtual environment...
    python -m venv venv
    echo ✅ Virtual environment created
    echo.
)

REM Activate virtual environment
echo 🔄 Activating virtual environment...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo ⚠️  Could not activate virtual environment.
    echo    Please activate manually: venv\Scripts\activate.bat
    pause
    exit /b 1
)
echo ✅ Virtual environment activated
echo.

REM Install/upgrade dependencies
echo 📦 Installing dependencies from requirements.txt...
python -m pip install --quiet --upgrade pip
pip install --quiet -r requirements.txt
echo ✅ Dependencies installed
echo.

REM Display info
echo ================================
echo 🚀 Starting Streamlit Demo Suite
echo ================================
echo.
echo The demo suite will open in your browser at:
echo 👉 http://localhost:8501
echo.
echo Available demos:
echo   🎙️  Voice-to-SBAR Demo
echo   📊 Clinical Dashboard
echo   💰 ROI Calculator
echo.
echo Press Ctrl+C to stop the server
echo.
echo ================================
echo.

REM Run streamlit
streamlit run Home.py

REM Deactivate virtual environment on exit
deactivate
