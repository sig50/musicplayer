import os
import sys
import wave

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import library
from settings import Settings


def make_wav(path):
    with wave.open(str(path), "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(8000)
        w.writeframes(b"\0\0" * 800)


def test_scan_and_organize(tmp_path):
    (tmp_path / "A" / "x").mkdir(parents=True)
    make_wav(tmp_path / "A" / "x" / "1.wav")
    make_wav(tmp_path / "b.wav")
    (tmp_path / "note.txt").write_text("x")
    tracks = library.scan_folder(str(tmp_path))
    assert len(tracks) == 2
    tree = library.organize(tracks)
    assert tree[0][0] == library.UNKNOWN_ARTIST


def test_favorites_first():
    a = library.Track("/a", "a", "Zed", "Z")
    b = library.Track("/b", "b", "Abe", "A")
    assert library.organize([a, b])[0][0] == "Abe"
    assert library.organize([a, b], {a.album_key})[0][0] == "Zed"


def test_cover_fallback(tmp_path):
    make_wav(tmp_path / "s.wav")
    assert library.extract_cover(str(tmp_path / "s.wav")) is None
    (tmp_path / "cover.jpg").write_bytes(b"img")
    assert library.extract_cover(str(tmp_path / "s.wav")) == b"img"


def test_settings_roundtrip(tmp_path):
    s = Settings(tmp_path / "s.json")
    s.last_folder = "/m"
    s.toggle_favorite("k")
    s2 = Settings(tmp_path / "s.json")
    assert s2.last_folder == "/m" and "k" in s2.favorites
