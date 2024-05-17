import sys
from telethon.types import Message
from PySide6.QtCore import QThread, Qt
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QStackedWidget,
    QHBoxLayout, QMessageBox,
)

# project imports
import config
import db
from async_tg_client import AsyncTelegramClientWorker
from sync_tg_client import SyncTelegramClient
from widgets.telegram_login_widget import TelegramClientLogin
from widgets.chat_client_widget import ChatClientWidget
from widgets.contact_list_widget import ContactListWidget


class T800(QMainWindow):
    def __init__(self):
        super().__init__()
        db.init_storage()
        self.contacts: dict = {}
        self.chats: dict = {}

        # telegram code
        self.sync_telegram_client = SyncTelegramClient()
        self.async_telegram_client = None
        self.telethon_thread = None
        self.init_telegram_event_loop()

        # gui code
        self.central_widget = QWidget()
        self.central_widget.setObjectName('central_widget')
        self.contact_list = ContactListWidget()
        self.contact_list.list_widget.itemClicked.connect(
            self.handle_contact_list_signal
        )
        self.chat_containers = QStackedWidget()
        self.init_ui()

    def init_ui(self):
        # title and placement
        self.setWindowTitle('T800-QT')
        self.setGeometry(100, 100, config.WINDOW_WIDTH, config.WINDOW_HEIGHT)

        # main window central widget
        self.setCentralWidget(self.central_widget)
        layout = QHBoxLayout(self.central_widget)
        # TODO find more elegant solutions for layout settings
        layout.addWidget(self.contact_list)
        self.contact_list.setMinimumWidth(300)
        self.contact_list.setMaximumWidth(300)
        layout.addWidget(self.chat_containers)

        if not self.sync_telegram_client.is_logged_in():
            dialog = TelegramClientLogin(self.sync_telegram_client,
                                         config.logo)
            dialog.resize(self.size())
            if not dialog.exec():
                error_box = QMessageBox()
                error_box.setIcon(QMessageBox.Critical)
                error_box.setText('Login failed!')
                error_box.setStandardButtons(QMessageBox.Ok)
                error_box.exec()
        self.setLayout(layout)

    def setup_chat_client_widget(self, contact):
        self.contacts[contact.user_id] = len(self.contacts)
        self.chats[contact.user_id] = ChatClientWidget(contact,
                                                       self.sync_telegram_client)
        self.chat_containers.addWidget(self.chats[contact.user_id])

    def handle_contact_list_signal(self, contact_item):
        contact = contact_item.data(101).contact
        try:
            ind = self.contacts[contact.user_id]
        except KeyError:
            self.setup_chat_client_widget(contact)
            ind = self.contacts[contact.user_id]
        self.chat_containers.setCurrentIndex(ind)

    def init_telegram_event_loop(self):
        """
        setup Qthread with the async telegram client
        """
        self.async_telegram_client = AsyncTelegramClientWorker()
        self.telethon_thread = QThread()
        self.async_telegram_client.moveToThread(self.telethon_thread)
        self.async_telegram_client.msg_receive_signal.connect(self.handle_recv_msg,
                                                              Qt.QueuedConnection)
        # connect slot to the signal
        self.telethon_thread.started.connect(self.async_telegram_client.run)
        self.telethon_thread.started.connect(self.async_telegram_client.run)
        # clean up
        self.telethon_thread.finished.connect(self.telethon_thread.quit)
        self.telethon_thread.finished.connect(self.async_telegram_client.deleteLater)
        self.telethon_thread.start()

    def handle_recv_msg(self, message: Message):
        from_id = self.sync_telegram_client.get_user_id_from_tg_message(message)
        contact = db.get_contact(from_id)
        if contact is not None:
            ucm = self.sync_telegram_client.save_unichat_message(message)
            try:
                self.chats[contact.user_id].add_message_to_chat_history(ucm)
            except KeyError:
                self.setup_chat_client_widget(contact)
                self.chats[contact.user_id].add_message_to_chat_history(ucm)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    with open(config.main_style, 'r') as f:
        app.setStyleSheet(f.read())
    main_window = T800()
    main_window.show()
    sys.exit(app.exec())
