# -*- mode: python ; coding: utf-8 -*-
# PyInstaller spec for D2R Companion (Windows one-folder build).
# Used by .github/workflows/build-windows.yml; not intended for local use
# (PyInstaller must run on the target OS, i.e. Windows).
#
# Result: dist/D2RCompanion/D2RCompanion.exe  (zip up the folder to ship)

block_cipher = None

a = Analysis(
    ['d2rc.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=[],
    hookspath=[],
    runtime_hooks=[],
    excludes=[
        'scipy',      # removed from the codebase; never bundle it
        'Xlib',       # Linux-only hotkey backend, dead on Windows
        'tkinter.test',
        'unittest',
        'pydoc',
        'pydoc_data',
        'test',
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='D2RCompanion',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,                    # UPX triggers AV false positives; skip it
    console=False,                # GUI app: no console window on launch
    icon='d2r.ico',
    version='version_info.txt',
)
coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=False,
    name='D2RCompanion',
)
