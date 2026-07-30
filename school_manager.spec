# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['school_manager/app.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('school_manager/views/styles.py', 'school_manager/views'),
        ('school_manager/views/components.py', 'school_manager/views'),
    ],
    hiddenimports=[
        'PyQt6.QtCore',
        'PyQt6.QtGui',
        'PyQt6.QtWidgets',
        'sqlalchemy',
        'reportlab',
        'PIL',
        'qrcode',
        'cryptography',
        'google_api_python_client',
        'openpyxl',
        'plyer',
        'wmi',
        'aiohttp',
        'schedule',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pkgs, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='SchoolManager',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,  # No console window
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,  # Add icon.ico path here
)

coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='SchoolManager',
)

# Create single-file executable
# pyinstaller --onedir --noconfirm --windowed school_manager/app.py
