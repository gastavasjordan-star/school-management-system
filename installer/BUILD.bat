@echo off
title School Management System - Builder
color 0A
echo.
echo  =============================================================
echo           SCHOOL MANAGEMENT SYSTEM - BUILD SCRIPT
echo  =============================================================
echo.
echo  This will:
echo   1. Compile the Python app with PyInstaller
echo   2. Create a Windows installer with Inno Setup
echo.
echo  =============================================================
echo.

REM Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python not found!
    echo Please install Python from https://python.org
    pause
    exit /b 1
)

REM Install dependencies
echo [1/4] Installing dependencies...
pip install pyinstaller sqlalchemy Pillow reportlab qrcode cryptography plyer -q
if errorlevel 1 (
    echo Failed to install dependencies
    pause
    exit /b 1
)
echo  Dependencies installed

REM Create dist folder
echo [2/4] Creating dist folder...
if not exist "dist" mkdir dist

REM Compile with PyInstaller
echo [3/4] Compiling application...
echo This may take 5-10 minutes...
pyinstaller --onefile --name SchoolManager --console --distpath dist demo.py --workpath build --specpath . --clean

REM Check if compilation successful
if not exist "dist\SchoolManager.exe" (
    echo.
    echo ERROR: Compilation failed!
    echo.
    pause
    exit /b 1
)

echo  Application compiled successfully!

REM Check for Inno Setup
echo [4/4] Checking for Inno Setup...
where iscc >nul 2>&1
if errorlevel 1 (
    echo.
    echo Inno Setup not found!
    echo.
    echo Download from: https://jrsoftware.org/isinfo.php
    echo.
    echo After installing Inno Setup, run this script again:
    echo   BUILD.bat
    echo.
    echo Your compiled app is ready at: dist\SchoolManager.exe
    echo.
    echo Press any key to open download page...
    pause >nul
    start https://jrsoftware.org/isinfo.php
    exit /b 1
)

REM Compile installer
echo Creating installer...
iscc SchoolManagement.iss

if exist "SchoolManagement_Setup.exe" (
    echo.
    echo  =============================================================
    echo              BUILD COMPLETE!
    echo  =============================================================
    echo.
    echo  Your installer is ready:
    echo   SchoolManagement_Setup.exe
    echo.
    echo  Share this file with your friends!
    echo  They can install the app with one click!
    echo.
) else (
    echo.
    echo Installer build failed. Check Inno Setup output above.
)

echo.
pause
