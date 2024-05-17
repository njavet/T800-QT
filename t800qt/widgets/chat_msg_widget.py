from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QPixmap
from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QGridLayout,
    QFrame
)
# project imports
import helpers
import db


class ChatMessageWidget(QWidget):
    """
    A ChatMessageWidget is the typical bubble with a message.

    """
    def __init__(self, unichat_message: db.UniChatMessage):
        super().__init__()
        self.unichat_message = unichat_message
        self.init_ui()

    def init_ui(self):
        """
        The `init_ui` function sets up the user interface for
        displaying chat messages with timestamps
        and alignment based on the sender.
        """
        layout = QGridLayout()
        from_me = self.unichat_message.from_contact.is_me

        message_frame = QFrame(self)
        message_frame.setObjectName('MessageBubble')
        message_frame.setFrameStyle(QFrame.Box | QFrame.Plain)
        message_frame.setLineWidth(0)
        message_frame_layout = QGridLayout()

        if self.unichat_message.text:
            message_label = QLabel(helpers.format_msg(self.unichat_message.text))
        elif self.unichat_message.photo_path:
            message_label = QLabel()
            pixmap = QPixmap(self.unichat_message.photo_path)
            message_label.setPixmap(pixmap)
        else:
            message_label = QLabel('unknown message format')

        message_label.setObjectName('MessageLabel')
        if from_me:
            message_frame.setProperty('status', 'me')
            message_label.setProperty('status', 'me')
            alignment = Qt.AlignRight
        else:
            message_frame.setProperty('status', 'contact')
            message_label.setProperty('status', 'contact')
            alignment = Qt.AlignLeft

        try:
            timestamp = self.unichat_message.timestamp.strftime('%H:%M')
        except AttributeError:
            timestamp = self.unichat_message.timestamp[11:16]
        timestamp_label = QLabel(timestamp)
        timestamp_label.setObjectName('TimestampLabel')
        timestamp_label.setAlignment(Qt.AlignRight)
        font = QFont()
        font.setPointSizeF(7)
        timestamp_label.setFont(font)

        message_label.setAlignment(alignment)
        message_frame_layout.addWidget(message_label)
        message_frame_layout.addWidget(timestamp_label)
        message_frame.setLayout(message_frame_layout)
        layout.addWidget(message_frame, 0, 0, alignment=alignment)
        layout.setContentsMargins(1, 1, 1, 1)
        self.setLayout(layout)

