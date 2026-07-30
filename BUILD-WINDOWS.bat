@echo off
echo =========================================
echo  School Manager - Windows Builder
echo =========================================
echo.
echo This will create a standalone .exe file
echo.

REM Check for Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python not found!
    echo Please install Python from https://python.org
    pause
    exit /b 1
)

REM Install PyInstaller
echo [1/4] Installing PyInstaller...
pip install pyinstaller -q
if errorlevel 1 (
    echo Failed to install PyInstaller
    pause
    exit /b 1
)

REM Create build folder
echo [2/4] Preparing build...
if not exist "build" mkdir build

REM Build executable
echo [3/4] Building SchoolManager.exe...
echo This may take 5-10 minutes...
pyinstaller --onefile --name SchoolManager --console demo.py --distpath . --workpath build --specpath . --clean

REM Check if successful
echo [4/4] Checking build...
if exist "SchoolManager.exe" (
    echo.
    echo =========================================
    echo  SUCCESS! 
    echo =========================================
    echo.
    echo Your executable is ready: SchoolManager.exe
    echo File size: 
    for %%A in (SchoolManager.exe) do echo   %%~zA bytes
    echo.
    echo Share this file with your friends!
    echo No installation needed - just double-click to run!
) else (
    echo.
    echo Build failed. Check the error messages above.
)

echo.
pause
