@echo off
REM School Manager - Build Script for Windows
REM Build standalone Windows executable using PyInstaller

echo =====================================
echo School Manager - Build Script
echo =====================================

REM Install dependencies
echo.
echo Step 1: Installing dependencies...
pip install -r requirements.txt

REM Build executable
echo.
echo Step 2: Building executable...
echo.

REM Run PyInstaller with windowed mode (no console)
pyinstaller ^
    --name="SchoolManager" ^
    --windowed ^
    --onedir ^
    --noconfirm ^
    --add-data "school_manager;school_manager" ^
    --hidden-import="PyQt6.QtCore" ^
    --hidden-import="PyQt6.QtGui" ^
    --hidden-import="PyQt6.QtWidgets" ^
    --hidden-import="sqlalchemy" ^
    --hidden-import="reportlab" ^
    --hidden-import="PIL" ^
    --hidden-import="qrcode" ^
    --hidden-import="cryptography" ^
    --hidden-import="google_api_python_client" ^
    --hidden-import="openpyxl" ^
    --hidden-import="plyer" ^
    --hidden-import="wmi" ^
    --hidden-import="aiohttp" ^
    --hidden-import="schedule" ^
    school_manager/app.py

echo.
echo =====================================
echo Build Complete!
echo =====================================
echo.
echo Executable location:
echo   dist\SchoolManager\SchoolManager.exe
echo.
echo To run the application:
echo   dist\SchoolManager\SchoolManager.exe
echo.
pause
