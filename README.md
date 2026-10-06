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
