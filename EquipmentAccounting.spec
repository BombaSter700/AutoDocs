# -*- mode: python ; coding: utf-8 -*-

import sys
from pathlib import Path

BASE = Path(".")

block_cipher = None

excludes = [
    "tensorflow", "tensorboard", "torch", "torchvision", "torchaudio",
    "sklearn", "scipy", "matplotlib", "grpc", "dask", "bokeh",
    "cffi", "Cython", "zmq", "notebook", "jupyter", "ipython",
    "nbformat", "nbconvert", "jedi", "parso", "debugpy",
    "setuptools._distutils", "pytest", "nose", "unittest",
    "cv2", "opencv", "pandas", "tornado", "prometheus_client",
    "werkzeug", "flask", "django", "sphinx", "docutils",
    "numba", "llvmlite", "h5py", "tables", "bottleneck",
    "google.cloud", "azure", "boto3", "botocore",
]

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[
        (str(BASE / 'docs'), 'docs'),
    ],
    hiddenimports=[
        'sqlalchemy', 'pydantic', 'docxtpl', 'qfluentwidgets',
        'PyQt6', 'PIL',
    ],
    hookspath=[],
    hooksconfig={},
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
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='EquipmentAccounting',
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
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='EquipmentAccounting',
)
