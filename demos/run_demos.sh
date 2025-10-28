#!/bin/bash

# EclipseLink AI Demo Runner
# Quick start script for running the demo suite locally

set -e

echo "🦚 EclipseLink AI - Demo Suite"
echo "================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

echo "✅ Python $(python3 --version) detected"
echo ""

# Check if pip is installed
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 is not installed. Please install pip."
    exit 1
fi

echo "✅ pip detected"
echo ""

# Check if in demos directory
if [ ! -f "Home.py" ]; then
    echo "❌ Error: Home.py not found. Please run this script from the demos directory."
    echo "   cd demos && ./run_demos.sh"
    exit 1
fi

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
    echo "✅ Virtual environment created"
    echo ""
fi

# Activate virtual environment
echo "🔄 Activating virtual environment..."
source venv/bin/activate || . venv/Scripts/activate 2>/dev/null || {
    echo "⚠️  Could not activate virtual environment automatically."
    echo "   Please activate manually:"
    echo "   - On macOS/Linux: source venv/bin/activate"
    echo "   - On Windows: venv\\Scripts\\activate"
    exit 1
}
echo "✅ Virtual environment activated"
echo ""

# Install/upgrade dependencies
echo "📦 Installing dependencies from requirements.txt..."
pip install -q --upgrade pip
pip install -q -r requirements.txt
echo "✅ Dependencies installed"
echo ""

# Display info
echo "================================"
echo "🚀 Starting Streamlit Demo Suite"
echo "================================"
echo ""
echo "The demo suite will open in your browser at:"
echo "👉 http://localhost:8501"
echo ""
echo "Available demos:"
echo "  🎙️  Voice-to-SBAR Demo"
echo "  📊 Clinical Dashboard"
echo "  💰 ROI Calculator"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""
echo "================================"
echo ""

# Run streamlit
streamlit run Home.py

# Deactivate virtual environment on exit
deactivate
