"""Persistent user preferences (last folder, favorites, shuffle)."""
import json
from pathlib import Path

DEFAULT_PATH = Path.home() / ".musicplayer" / "settings.json"


class Settings:
    def __init__(self, path=None):
        self.path = Path(path) if path else DEFAULT_PATH
        self.last_folder = ""
        self.shuffle = False
        self.favorites = set()  # keys: "artist||album" or "artist||album||track path"
        self.load()

    def load(self):
        try:
            data = json.loads(self.path.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            return
        if not isinstance(data, dict):
            return
        self.last_folder = str(data.get("last_folder", ""))
        self.shuffle = bool(data.get("shuffle", False))
        self.favorites = {str(f) for f in data.get("favorites", [])}

    def save(self):
        try:
            self.path.parent.mkdir(parents=True, exist_ok=True)
            self.path.write_text(json.dumps({
                "last_folder": self.last_folder,
                "shuffle": self.shuffle,
                "favorites": sorted(self.favorites),
            }, ensure_ascii=False, indent=2), encoding="utf-8")
        except OSError:
            pass

    def toggle_favorite(self, key):
        if key in self.favorites:
            self.favorites.discard(key)
        else:
            self.favorites.add(key)
        self.save()
        return key in self.favorites
