# PyInstaller spec: single-file, windowed executable -> dist/musicplayer.exe
a = Analysis(
    ["main.py"],
    pathex=["."],
    datas=[("assets", "assets")],
    hiddenimports=["mutagen", "pygame"],
    noarchive=False,
)
pyz = PYZ(a.pure)
exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name="musicplayer",
    console=False,
    icon="assets/icon.ico",
    upx=True,
)
