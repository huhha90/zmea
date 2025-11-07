# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['zmea_V4.py'],
    pathex=[],
    binaries=[],
    datas=[('assets/music/Snake_Rattle_Dendy.mp3', 'assets/music'), ('assets/music/eat.wav', 'assets/music'), ('assets/music/collision.wav', 'assets/music')],
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
    [],
    exclude_binaries=True,
    name='zmea_V4',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['C:\\Users\\dbzcg\\Desktop\\zmea\\zmea22.ico'],
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='zmea_V4',
)
