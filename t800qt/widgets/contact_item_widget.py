from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QHBoxLayout,
    QSizePolicy,
)
from PySide6.QtGui import QPixmap, QPainter, QBrush
from PySide6.QtCore import Qt

# project imports
import db


class ContactItemWidget(QWidget):
    def __init__(self, contact: db.Contact):
        super().__init__()
        self.contact = contact
        self.init_ui()

    def init_ui(self):
        layout = QHBoxLayout()
        pixmap = QPixmap(self.contact.profile_pic)
        pixmap = pixmap.scaledToWidth(50)
        rounded_pixmap = self.round_pixmap(pixmap)
        label_image = QLabel()
        label_image.setPixmap(rounded_pixmap)
        label_image.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        layout.addWidget(label_image)
        label_text = QLabel(self.contact.name)
        layout.addWidget(label_text)
        layout.setContentsMargins(1, 1, 0, 0)
        self.setLayout(layout)

    @staticmethod
    def round_pixmap(pixmap):
        rounded_pixmap = QPixmap(pixmap.size())
        rounded_pixmap.fill(Qt.transparent)
        painter = QPainter(rounded_pixmap)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        rounded_rect = pixmap.rect().adjusted(1, 1, -1, -1)
        painter.setBrush(QBrush(pixmap))
        painter.setPen(Qt.NoPen)
        painter.drawRoundedRect(rounded_rect, 50, 50)
        painter.end()
        return rounded_pixmap
