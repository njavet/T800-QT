from PySide6.QtWidgets import (
    QWidget,
    QLineEdit,
    QListWidget,
    QListWidgetItem,
    QVBoxLayout, QFileDialog, QPushButton, QHBoxLayout, QSizePolicy,
)

# project imports
import db
from widgets.chat_msg_widget import ChatMessageWidget


class ChatClientWidget(QWidget):
    def __init__(self, contact: db.Contact, sync_tg_client):
        super().__init__()
        self.contact = contact
        self.sync_tg_client = sync_tg_client
        # gui
        self.chat_widget = QWidget()
        self.chat_message_history = QListWidget()
        self.send_file_button = QPushButton()
        self.chat_input = QLineEdit()
        self.init_ui()
        self.init_chat_display()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.addWidget(self.chat_widget)
        layout.addWidget(self.chat_message_history)

        # text input and send file button
        container_widget = QWidget()
        input_layout = QHBoxLayout()
        input_layout.addWidget(self.send_file_button)
        self.chat_input.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.chat_input.setPlaceholderText('Write a message...')
        self.chat_input.returnPressed.connect(self.launch_send_message_process)
        input_layout.addWidget(self.chat_input)
        container_widget.setLayout(input_layout)
        layout.addWidget(container_widget)

    def launch_send_message_process(self):
        text = self.chat_input.text()
        ucm = self.sync_tg_client.send_unichat_message(self.contact, text)
        self.add_message_to_chat_history(ucm)
        self._scroll_to_last_message()
        self.chat_input.clear()

    def add_message_to_chat_history(self, unichat_message: db.UniChatMessage):
        list_item = QListWidgetItem(self.chat_message_history)
        message_widget = ChatMessageWidget(unichat_message)
        list_item.setSizeHint(message_widget.sizeHint())
        self.chat_message_history.addItem(list_item)
        self.chat_message_history.setItemWidget(list_item, message_widget)

    def _scroll_to_last_message(self):
        item_count = self.chat_message_history.count()
        last_item = self.chat_message_history.item(item_count - 1)
        self.chat_message_history.scrollToItem(last_item)

    def init_chat_display(self):
        self.chat_message_history.clear()
        messages = self.load_messages()
        for ucm in messages:
            self.add_message_to_chat_history(ucm)
        vb = self.chat_message_history.verticalScrollBar()
        self.chat_message_history.verticalScrollBar().setValue(vb.maximum())
        self._scroll_to_last_message()
        self.setContentsMargins(2, 2, 3, 4)

    def load_messages(self):
        if self.contact.is_me:
            messages = (db.UniChatMessage
                        .select()
                        .where((db.UniChatMessage.from_contact == self.contact) &
                               (db.UniChatMessage.to_contact == self.contact))
                        .order_by(db.UniChatMessage.timestamp))
        else:
            messages = (db.UniChatMessage
                        .select()
                        .where((db.UniChatMessage.from_contact == self.contact) |
                               (db.UniChatMessage.to_contact == self.contact))
                        .order_by(db.UniChatMessage.timestamp))
        return messages
