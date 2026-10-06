"""Artist/Album/Track tree view with favorite marking."""
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import QMenu, QTreeWidget, QTreeWidgetItem

import library

KEY_ROLE = Qt.UserRole
TRACK_ROLE = Qt.UserRole + 1
STAR = "\u2605 "


class LibraryTree(QTreeWidget):
    track_activated = pyqtSignal(object)
    favorite_toggled = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setHeaderLabels(["Library"])
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self._menu)
        self.itemDoubleClicked.connect(self._double_clicked)
        self.favorites = set()

    def populate(self, tracks, favorites):
        self.favorites = favorites
        self.clear()
        for artist, albums in library.organize(tracks, favorites):
            a_item = QTreeWidgetItem([artist])
            for album, items in albums:
                akey = library.album_key(artist, album)
                al_item = self._item(album, akey)
                for t in items:
                    t_item = self._item(t.title, t.key)
                    t_item.setData(0, TRACK_ROLE, t)
                    al_item.addChild(t_item)
                a_item.addChild(al_item)
            self.addTopLevelItem(a_item)

    def _item(self, text, key):
        item = QTreeWidgetItem([(STAR if key in self.favorites else "") + text])
        item.setData(0, KEY_ROLE, key)
        return item

    def tracks_of(self, item):
        t = item.data(0, TRACK_ROLE)
        if t is not None:
            return [t]
        out = []
        for i in range(item.childCount()):
            out.extend(self.tracks_of(item.child(i)))
        return out

    def _double_clicked(self, item, _col):
        tracks = self.tracks_of(item)
        if tracks:
            self.track_activated.emit(item)

    def _menu(self, pos):
        item = self.itemAt(pos)
        key = item.data(0, KEY_ROLE) if item else None
        if not key:
            return
        menu = QMenu(self)
        act = menu.addAction("Remove from favorites" if key in self.favorites
                             else "Pin to top (favorite)")
        if menu.exec_(self.viewport().mapToGlobal(pos)) == act:
            self.favorite_toggled.emit(key)
