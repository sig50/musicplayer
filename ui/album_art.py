"""Album art widget with placeholder for missing art."""
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor, QFont, QImage, QPainter, QPixmap
from PyQt5.QtWidgets import QLabel

SIZE = 300


def placeholder(size=SIZE):
    pix = QPixmap(size, size)
    pix.fill(QColor("#3a3a3a"))
    painter = QPainter(pix)
    painter.setPen(QColor("#888888"))
    font = QFont()
    font.setPixelSize(size // 2)
    painter.setFont(font)
    painter.drawText(pix.rect(), Qt.AlignCenter, "\u266a")
    painter.end()
    return pix


class AlbumArt(QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(SIZE, SIZE)
        self.setAlignment(Qt.AlignCenter)
        self.set_image(None)

    def set_image(self, data):
        pix = QPixmap()
        if not data or not pix.loadFromData(data):
            pix = placeholder()
        self.setPixmap(pix.scaled(SIZE, SIZE, Qt.KeepAspectRatio, Qt.SmoothTransformation))
