# -*- mode: python ; coding: utf-8 -*-
# PyInstaller spec for D2R Companion (Windows + Linux one-folder builds).
# Used by .github/workflows/build-release.yml; not intended for local use
# (PyInstaller must run on the target OS, i.e. Windows or Linux).
#
# Result: dist/D2RCompanion/D2RCompanion(.exe)  (zip up the folder to ship)

import sys

block_cipher = None

# platform-specific excludes: Xlib is the Linux hotkey backend, dead on Windows
excludes = [
    'scipy',      # removed from the codebase; never bundle it
    'tkinter.test',
    'unittest',
    'pydoc',
    'pydoc_data',
    'test',
]
if sys.platform == 'win32':
    excludes.append('Xlib')

a = Analysis(
    ['d2rc.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=[],
    hookspath=[],
    runtime_hooks=[],
    excludes=excludes,
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
