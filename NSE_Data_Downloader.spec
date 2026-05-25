# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['nse_downloader.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=['selenium', 'requests', 'schedule'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        'matplotlib', 'numpy', 'scipy', 'pandas', 'PIL', 'cv2',
        'pytest', 'py', 'tkinter.test', 'unittest', 'test',
        'IPython', 'jupyter', 'notebook', 'jedi', 'parso',
        'pygments', 'pkg_resources', 'pip',
        'cryptography'
    ],
    noarchive=False,
    optimize=2,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='NSE_Data_Downloader',
    debug=False,
    bootloader_ignore_signals=False,
    strip=True,
    upx=True,
    upx_exclude=['vcruntime140.dll', 'msvcp140.dll'],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
