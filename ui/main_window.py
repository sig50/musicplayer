"""Main application window."""
import os

from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtWidgets import (QFileDialog, QHBoxLayout, QLabel, QMainWindow, QPushButton,
                             QSlider, QSplitter, QVBoxLayout, QWidget)

import library
from player import Player
from settings import Settings
from ui.album_art import AlbumArt
from ui.library_tree import LibraryTree


class MainWindow(QMainWindow):
    def __init__(self, settings=None, player=None):
        super().__init__()
        self.setWindowTitle("Music Player")
        self.resize(900, 520)
        self.settings = settings or Settings()
        self.player = player or Player()
        self.player.shuffle = self.settings.shuffle
        self.tracks = []

        self.folder_btn = QPushButton("Select Folder…")
        self.folder_label = QLabel("No folder selected")
        self.tree = LibraryTree()
        self.art = AlbumArt()
        self.title_label = QLabel("—")
        self.title_label.setStyleSheet("font-size: 16px; font-weight: bold;")
        self.title_label.setWordWrap(True)
        self.sub_label = QLabel("")
        self.play_btn = QPushButton("Play")
        self.pause_btn = QPushButton("Pause")
        self.stop_btn = QPushButton("Stop")
        self.prev_btn = QPushButton("Prev")
        self.next_btn = QPushButton("Next")
        self.shuffle_btn = QPushButton("Shuffle")
        self.shuffle_btn.setCheckable(True)
        self.shuffle_btn.setChecked(self.player.shuffle)
        self.volume = QSlider(Qt.Horizontal)
        self.volume.setRange(0, 100)
        self.volume.setValue(70)

        top = QHBoxLayout()
        top.addWidget(self.folder_btn)
        top.addWidget(self.folder_label, 1)
        controls = QHBoxLayout()
        for b in (self.prev_btn, self.play_btn, self.pause_btn, self.stop_btn,
                  self.next_btn, self.shuffle_btn):
            controls.addWidget(b)
        right = QVBoxLayout()
        right.addWidget(self.art, alignment=Qt.AlignCenter)
        right.addWidget(self.title_label)
        right.addWidget(self.sub_label)
        right.addLayout(controls)
        right.addWidget(self.volume)
        right.addStretch(1)
        right_w = QWidget()
        right_w.setLayout(right)
        split = QSplitter()
        split.addWidget(self.tree)
        split.addWidget(right_w)
        split.setStretchFactor(0, 1)
        central = QWidget()
        lay = QVBoxLayout(central)
        lay.addLayout(top)
        lay.addWidget(split, 1)
        self.setCentralWidget(central)

        self.folder_btn.clicked.connect(self.choose_folder)
        self.play_btn.clicked.connect(self.on_play)
        self.pause_btn.clicked.connect(self.player.pause)
        self.stop_btn.clicked.connect(self.on_stop)
        self.next_btn.clicked.connect(self.on_next)
        self.prev_btn.clicked.connect(self.on_prev)
        self.shuffle_btn.toggled.connect(self.on_shuffle)
        self.volume.valueChanged.connect(lambda v: self.player.set_volume(v / 100))
        self.tree.track_activated.connect(self.play_item)
        self.tree.favorite_toggled.connect(self.on_favorite)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.poll)
        self.timer.start(500)

        if self.settings.last_folder and os.path.isdir(self.settings.last_folder):
            self.load_folder(self.settings.last_folder)

    def choose_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Select music folder",
                                                  self.settings.last_folder or "")
        if folder:
            self.load_folder(folder)

    def load_folder(self, folder):
        self.settings.last_folder = folder
        self.settings.save()
        self.folder_label.setText(folder)
        self.tracks = library.scan_folder(folder)
        self.refresh_tree()

    def refresh_tree(self):
        self.tree.populate(self.tracks, self.settings.favorites)
        self.tree.expandToDepth(0)

    def play_item(self, item):
        tracks = self.tree.tracks_of(item)
        if not tracks:
            return
        # queue = all tracks in tree order, start at the chosen one
        ordered = []
        for i in range(self.tree.topLevelItemCount()):
            ordered.extend(self.tree.tracks_of(self.tree.topLevelItem(i)))
        self.player.set_queue(ordered, ordered.index(tracks[0]))
        self.start()

    def start(self, idx=None):
        if self.player.play(idx):
            self.show_current()
        else:
            self.sub_label.setText("Cannot play this file")

    def show_current(self):
        t = self.player.current
        if not t:
            return
        self.title_label.setText(t.title)
        self.sub_label.setText(f"{t.artist} — {t.album}")
        self.art.set_image(library.extract_cover(t.path))

    def on_play(self):
        if self.player.paused:
            self.player.resume()
        elif self.player.queue:
            self.start(self.player.index if self.player.index >= 0 else 0)
        elif self.tracks:
            self.player.set_queue(self.tracks, 0)
            self.start()

    def on_stop(self):
        self.player.stop()

    def on_next(self):
        if self.player.next():
            self.show_current()

    def on_prev(self):
        if self.player.previous():
            self.show_current()

    def on_shuffle(self, on):
        self.player.shuffle = on
        self.settings.shuffle = on
        self.settings.save()

    def on_favorite(self, key):
        self.settings.toggle_favorite(key)
        self.refresh_tree()

    def poll(self):
        if self.player.is_finished() and self.player.next():
            self.show_current()

    def closeEvent(self, event):
        self.player.stop()
        super().closeEvent(event)
