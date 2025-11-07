# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['zmea_V0.5.6.py'],
    pathex=[],
    binaries=[],
    datas=[('assets', 'assets'), ('settings.json', '.'), ('leaderboard.json', '.'), ('levels.json', '.'), ('level_progress.json', '.')],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='zmea_V0.5.6',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['zmea5.ico'],
)
