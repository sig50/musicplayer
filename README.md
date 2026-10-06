# musicplayer

A desktop music player written in Python (PyQt5 + pygame.mixer + mutagen).

## Features
- Select a music folder (scanned recursively; MP3, FLAC, OGG, WAV)
- Library tree organized by artist → album → track
- Album art shown during playback (embedded art, `cover/folder/front/album.jpg|png`
  next to the file, or a placeholder)
- Play / Pause / Stop / Prev / Next, volume slider
- Shuffle toggle
- Priority display: right-click an artist's album or track and choose
  "Pin to top (favorite)" – favorites are listed first
- Last folder, favorites and shuffle are saved to `~/.musicplayer/settings.json`

## Installation
```
pip install -r requirements.txt
python main.py
```

## Download pre-built EXE
Download the latest `musicplayer.exe` (portable) or `musicplayer-setup.exe`
(installer) from the [Releases page](https://github.com/sig50/musicplayer/releases).
No Python is required: run the portable EXE directly, or run the installer.
Verify a download with `SHA256SUMS.txt` (e.g. `certutil -hashfile musicplayer.exe SHA256`).

### Publishing a release (maintainers)
Pushing a version tag triggers `.github/workflows/build-release.yml`, which builds
the EXE and installer, then creates a GitHub Release with them, checksums and
auto-generated release notes attached:
```
git tag v1.0.0
git push origin v1.0.0
```

## Building a Windows EXE
Users of the EXE do not need Python installed.

1. Install Python 3.8+ on Windows (check "Add Python to PATH").
2. Clone/download this repository and open a Command Prompt in its folder.
3. Run `python build_exe.py` (or double-click `build.bat`). This installs the
   requirements and PyInstaller, then builds using `build.spec`.
4. The single-file portable executable is created at `dist\musicplayer.exe`
   (intermediate files go to `build\`). Run or copy it anywhere.

### Optional: installer (setup wizard)
1. Install [NSIS](https://nsis.sourceforge.io/).
2. After building the EXE, run `makensis installer.nsi`.
3. Distribute `dist\musicplayer-setup.exe`; it installs to Program Files and
   creates Start menu/desktop shortcuts plus an uninstaller.

The icon is `assets/icon.ico`; replace it to use your own.

## Layout
- `main.py` – entry point
- `player.py` – playback logic
- `library.py` – scanning/organizing/metadata/cover extraction
- `settings.py` – persisted preferences
- `ui/` – PyQt widgets and main window

## Tests
```
pip install pytest
python -m pytest tests
```
