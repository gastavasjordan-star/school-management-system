#!/bin/bash

# School Manager - Build Script
# Builds standalone Windows executable using PyInstaller

echo "====================================="
echo "School Manager - Build Script"
echo "====================================="

# Set script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Create build directory
mkdir -p build dist

echo ""
echo "Step 1: Installing dependencies..."
pip install -r requirements.txt 2>/dev/null || true

echo ""
echo "Step 2: Building executable..."
echo ""

# Run PyInstaller with windowed mode (no console)
pyinstaller \
    --name="SchoolManager" \
    --windowed \
    --onedir \
    --noconfirm \
    --add-data "school_manager:school_manager" \
    --hidden-import="PyQt6.QtCore" \
    --hidden-import="PyQt6.QtGui" \
    --hidden-import="PyQt6.QtWidgets" \
    --hidden-import="sqlalchemy" \
    --hidden-import="reportlab" \
    --hidden-import="PIL" \
    --hidden-import="qrcode" \
    --hidden-import="cryptography" \
    --hidden-import="google_api_python_client" \
    --hidden-import="openpyxl" \
    --hidden-import="plyer" \
    --hidden-import="wmi" \
    --hidden-import="aiohttp" \
    --hidden-import="schedule" \
    school_manager/app.py

echo ""
echo "====================================="
echo "Build Complete!"
echo "====================================="
echo ""
echo "Executable location:"
echo "  dist/SchoolManager/SchoolManager.exe"
echo ""
echo "To run the application:"
echo "  ./dist/SchoolManager/SchoolManager.exe"
echo ""
