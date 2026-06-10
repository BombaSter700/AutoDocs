"""
Build script: creates a standalone .exe for the equipment accounting system.
Run: python build.py
"""
import subprocess
import sys
import shutil
from pathlib import Path

BASE = Path(__file__).parent


def build():
    dist = BASE / "dist"
    if dist.exists():
        shutil.rmtree(dist)

    spec = BASE / "EquipmentAccounting.spec"
    if not spec.exists():
        print(f"Spec file not found: {spec}")
        sys.exit(1)

    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--noconfirm",
        str(spec),
    ]

    print("Building with optimized .spec (ML packages excluded)...")
    print(f"Command: {' '.join(cmd)}")
    result = subprocess.run(cmd, cwd=BASE)

    if result.returncode == 0:
        exe = dist / "EquipmentAccounting" / "EquipmentAccounting.exe"
        if exe.exists():
            size_mb = exe.stat().st_size / (1024 * 1024)
            print(f"\n[OK] Build complete: {exe} ({size_mb:.1f} MB)")
        else:
            print(f"\n[!] Build finished but exe not found at {exe}")
    else:
        print(f"\n[FAIL] Build failed with code {result.returncode}")
        sys.exit(result.returncode)


if __name__ == "__main__":
    build()
