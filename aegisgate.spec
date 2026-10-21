# -*- mode: python ; coding: utf-8 -*-
"""PyInstaller specification file for AegisGate standalone Windows executable.

Guarantees:
1. Bundles only application source code and web template (app/templates/index.html).
2. NEVER bundles data/, database files, .secret_key, passwords, or personal credentials.
3. Includes all necessary uvicorn, anyio, and cryptography hidden imports.
4. Generates a standalone executable in dist/release_candidate/aegisgate.exe.
"""

import sys
from pathlib import Path
from PyInstaller.utils.hooks import collect_submodules, collect_data_files

block_cipher = None

# Hidden imports needed for uvicorn async workers, starlette, and cryptography
hidden_imports = [
    "uvicorn",
    "uvicorn.logging",
    "uvicorn.loops",
    "uvicorn.loops.auto",
    "uvicorn.loops.asyncio",
    "uvicorn.protocols",
    "uvicorn.protocols.http",
    "uvicorn.protocols.http.auto",
    "uvicorn.protocols.http.h11_impl",
    "uvicorn.protocols.websockets",
    "uvicorn.protocols.websockets.auto",
    "uvicorn.lifespans",
    "uvicorn.lifespans.on",
    "uvicorn.lifespans.off",
    "anyio",
    "anyio._backends._asyncio",
    "argon2",
    "cryptography",
    "cryptography.hazmat.primitives.asymmetric.ed25519",
    "sqlite3",
    "pydantic",
    "pydantic_core",
    "starlette",
    "starlette.responses",
    "starlette.routing",
    "fastapi",
]

# Assets to bundle: ONLY the dashboard template
# Strictly NO data/, NO databases, NO secret keys
datas = [
    ("app/templates", "app/templates"),
]

a = Analysis(
    ["entrypoint.py"],
    pathex=["."],
    binaries=[],
    datas=datas,
    hiddenimports=hidden_imports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        "tkinter",
        "unittest",
        "pdb",
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
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name="aegisgate",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,  # Disable UPX to avoid antivirus heuristics false positives
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,  # Console window enabled so logs and CLI commands are visible
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
