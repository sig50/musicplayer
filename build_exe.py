"""One-command build: python build_exe.py  ->  dist/musicplayer.exe"""
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def main():
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", str(ROOT / "requirements.txt"), "pyinstaller"])
    subprocess.check_call(
        [sys.executable, "-m", "PyInstaller", "--noconfirm", "--clean", str(ROOT / "build.spec")],
        cwd=ROOT,
    )
    print("\nBuild complete: %s" % (ROOT / "dist" / "musicplayer.exe"))


if __name__ == "__main__":
    main()
