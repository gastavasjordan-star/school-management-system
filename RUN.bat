@echo off
title School Manager Demo
color 0A
echo.
echo ============================================
echo    SCHOOL MANAGER - DEMO VERSION
echo ============================================
echo.

REM Find Python with full path
set PYTHON=
if exist "C:\Users\Lenovo\AppData\Local\Programs\Python\Python311\python.exe" (
    set PYTHON=C:\Users\Lenovo\AppData\Local\Programs\Python\Python311\python.exe
) else if exist "C:\Users\Lenovo\AppData\Local\Programs\Python\Python312\python.exe" (
    set PYTHON=C:\Users\Lenovo\AppData\Local\Programs\Python\Python312\python.exe
) else if exist "C:\Users\Lenovo\AppData\Local\Programs\Python\Python310\python.exe" (
    set PYTHON=C:\Users\Lenovo\AppData\Local\Programs\Python\Python310\python.exe
)

if "%PYTHON%"=="" (
    echo ERROR: Python not found!
    echo.
    echo Please install Python from:
    echo https://www.python.org/downloads/
    echo.
    echo Make sure to check "Add Python to PATH"
    echo.
    pause
    exit /b 1
)

echo Found Python: %PYTHON%
echo.

REM Check if sqlite3 works
echo Testing Python...
"%PYTHON%" -c "import sqlite3; print('SQLite OK')" 2>nul
if errorlevel 1 (
    echo.
    echo WARNING: sqlite3 module not found
    echo This is included with Python but might be missing
)

echo.
echo ============================================
echo  Starting School Manager...
echo ============================================
echo.
echo Login: Jordan / admin123
echo.
echo.

REM Run the demo
set PYTHONPATH=%~dp0
"%PYTHON%" demo.py

echo.
echo ============================================
echo  Program closed
echo ============================================
pause
