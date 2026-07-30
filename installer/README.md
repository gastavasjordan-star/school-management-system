# School Management System - Windows Installer

## Quick Start

### Option 1: Use Build Script (Recommended)
1. Run `BUILD.bat` - this compiles everything
2. Install Inno Setup from: https://jrsoftware.org/isinfo.php
3. Run `BUILD.bat` again
4. Share `SchoolManagement_Setup.exe`

### Option 2: Already have the compiled app?
1. Install Inno Setup from: https://jrsoftware.org/isinfo.php
2. Double-click `SchoolManagement.iss`
3. Your installer will be created!

## Files Included

| File | Description |
|------|-------------|
| `demo.py` | Main application source code |
| `SchoolManagement.iss` | Inno Setup script for installer |
| `BUILD.bat` | Build script |
| `data/` | Default configuration |
| `schemas/` | Database schema |
| `reports/` | Report templates |

## System Requirements

- Windows 7, 8, 10, or 11
- No Python required (compiled with PyInstaller)

## Default Login

| Username | Password | Role |
|----------|----------|------|
| Jordan | admin123 | Super Admin |
| Teacher | admin123 | Class Teacher |
| Bursar | admin123 | Bursar |

## Building the Installer

1. Install Python from python.org
2. Install Inno Setup from: https://jrsoftware.org/isinfo.php
3. Double-click `BUILD.bat`
4. `SchoolManagement_Setup.exe` will be created!

## Support

GitHub: https://github.com/gastavasjordan-star/school-management-system
