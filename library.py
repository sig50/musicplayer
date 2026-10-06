"""Music library management: folder scanning and artist/album organization."""
import os
from dataclasses import dataclass
from pathlib import Path

import mutagen
from mutagen.flac import FLAC
from mutagen.id3 import ID3
from mutagen.mp4 import MP4

SUPPORTED_EXTENSIONS = {".mp3", ".flac", ".ogg", ".wav"}
UNKNOWN_ARTIST = "Unknown Artist"
UNKNOWN_ALBUM = "Unknown Album"
COVER_NAMES = ("cover", "folder", "front", "album")
IMAGE_EXTENSIONS = (".jpg", ".jpeg", ".png")


@dataclass
class Track:
    path: str
    title: str
    artist: str
    album: str
    track_no: int = 0
    duration: float = 0.0

    @property
    def album_key(self):
        return album_key(self.artist, self.album)

    @property
    def key(self):
        return f"{self.album_key}||{self.path}"


def album_key(artist, album):
    return f"{artist}||{album}"


def _first(tags, name):
    try:
        value = tags.get(name) if tags is not None else None
    except Exception:
        return None
    if not value:
        return None
    if isinstance(value, (list, tuple)):
        value = value[0]
    text = str(value).strip()
    return text or None


def read_track(path):
    """Read metadata for one file; falls back to file/folder names."""
    p = Path(path)
    title, artist, album, track_no, duration = p.stem, None, None, 0, 0.0
    try:
        audio = mutagen.File(str(p), easy=True)
    except Exception:
        audio = None
    if audio is not None:
        duration = float(getattr(getattr(audio, "info", None), "length", 0) or 0)
        title = _first(audio.tags, "title") or title
        artist = _first(audio.tags, "artist") or _first(audio.tags, "albumartist")
        album = _first(audio.tags, "album")
        num = _first(audio.tags, "tracknumber")
        if num:
            try:
                track_no = int(num.split("/")[0])
            except ValueError:
                pass
    return Track(str(p), title, artist or UNKNOWN_ARTIST, album or UNKNOWN_ALBUM,
                 track_no, duration)


def scan_folder(folder):
    """Recursively find supported audio files and return a list of Tracks."""
    tracks = []
    for root, _dirs, files in os.walk(folder):
        for name in sorted(files):
            if Path(name).suffix.lower() in SUPPORTED_EXTENSIONS:
                tracks.append(read_track(os.path.join(root, name)))
    return tracks


def organize(tracks, favorites=frozenset()):
    """Return [(artist, [(album, [tracks])])]; favorites are listed first."""
    tree = {}
    for t in tracks:
        tree.setdefault(t.artist, {}).setdefault(t.album, []).append(t)

    def album_fav(artist, album):
        return album_key(artist, album) in favorites

    result = []
    for artist, albums in tree.items():
        album_list = []
        for album, items in albums.items():
            items.sort(key=lambda t: (not t.key in favorites, t.track_no or 10**6,
                                      t.title.lower()))
            album_list.append((album, items))
        album_list.sort(key=lambda a: (not album_fav(artist, a[0]), a[0].lower()))
        result.append((artist, album_list))
    result.sort(key=lambda a: (
        not any(album_fav(a[0], al) or any(t.key in favorites for t in ts)
                for al, ts in a[1]),
        a[0].lower()))
    return result


def extract_cover(path):
    """Return embedded album art bytes, or art image next to the file, or None."""
    ext = Path(path).suffix.lower()
    try:
        if ext == ".mp3":
            for frame in ID3(path).getall("APIC"):
                return frame.data
        elif ext == ".flac":
            pics = FLAC(path).pictures
            if pics:
                return pics[0].data
        elif ext == ".ogg":
            import base64
            from mutagen.flac import Picture
            audio = mutagen.File(path)
            for b64 in (audio.tags or {}).get("metadata_block_picture", []):
                return Picture(base64.b64decode(b64)).data
        elif ext in (".m4a", ".mp4"):
            covr = MP4(path).tags.get("covr")
            if covr:
                return bytes(covr[0])
    except Exception:
        pass
    folder = Path(path).parent
    try:
        for f in sorted(folder.iterdir()):
            if f.suffix.lower() in IMAGE_EXTENSIONS and f.stem.lower() in COVER_NAMES:
                return f.read_bytes()
    except OSError:
        pass
    return None
