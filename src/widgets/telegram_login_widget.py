from PySide6.QtWidgets import (
    QLabel,
    QVBoxLayout,
    QLineEdit,
    QPushButton, QDialog)
from PySide6.QtGui import QPixmap, QRegularExpressionValidator, Qt


class TelegramClientLogin(QDialog):
    def __init__(self, sync_tg_client, logo_path):
        super().__init__()
        self.sync_tg_client = sync_tg_client
        self.phone_number = None
        self.logo_path = logo_path

        self.logo_label = QLabel()

        self.phone_number_label = QLabel('Phone number:')
        self.phone_number_edit = QLineEdit()

        self.access_code_button = QPushButton('Request Access code')
        self.access_code_button.clicked.connect(self.request_code)

        self.access_code_label = QLabel('Access Code:')
        self.access_code_edit = QLineEdit()
        self.login_button = QPushButton('Login')
        self.login_button.clicked.connect(self.qt_login)

        self.layout = QVBoxLayout()
        self.set_width()
        self.set_color()
        self.init_ui()

    def set_width(self, width=512):
        self.phone_number_label.setMaximumWidth(width)
        self.phone_number_label.setMinimumWidth(width)

        self.phone_number_edit.setMaximumWidth(width)
        self.phone_number_edit.setMinimumWidth(width)

        self.access_code_button.setMaximumWidth(width)
        self.access_code_button.setMinimumWidth(width)

        self.access_code_label.setMaximumWidth(width)
        self.access_code_label.setMinimumWidth(width)

        self.access_code_edit.setMaximumWidth(width)
        self.access_code_edit.setMinimumWidth(width)

        self.login_button.setMaximumWidth(width)
        self.login_button.setMinimumWidth(width)

    def set_color(self):
        self.phone_number_label.setStyleSheet("color: #bc957c")
        self.phone_number_edit.setStyleSheet("background-color: #888f93")

        self.access_code_label.setStyleSheet("color: #bc957c")
        self.access_code_edit.setStyleSheet("background-color: #888f93")

        self.access_code_button.setStyleSheet("background-color: #888f93")
        self.login_button.setStyleSheet("background-color: #888f93")

    def init_ui(self):
        self.setup_logo()
        self.set_phone_number_elements()

        self.layout.addWidget(self.access_code_button, alignment=Qt.AlignCenter)
        self.layout.addWidget(self.access_code_label, alignment=Qt.AlignCenter)
        self.layout.addWidget(self.access_code_edit, alignment=Qt.AlignCenter)
        self.layout.addWidget(self.login_button, alignment=Qt.AlignCenter)

        self.setLayout(self.layout)

    def setup_logo(self):
        self.logo_label.setPixmap(QPixmap(self.logo_path))
        self.layout.addWidget(self.logo_label, alignment=Qt.AlignCenter)

    def set_phone_number_elements(self):
        # phone number validator
        phone_number_pattern = "^[+]?[0-9]{1,3}[-]?[0-9]{5,14}$"
        phone_number_validator = QRegularExpressionValidator(phone_number_pattern)
        self.phone_number_edit.setValidator(phone_number_validator)

        self.layout.addWidget(self.phone_number_label, alignment=Qt.AlignCenter)
        self.layout.addWidget(self.phone_number_edit, alignment=Qt.AlignCenter)

    def qt_login(self):
        # TODO exception handling
        self.sync_tg_client.login(phone_number=self.phone_number,
                                  auth_code=self.access_code_edit.text())
        self.accept()

    def request_code(self):
        self.phone_number = self.phone_number_edit.text()
        self.sync_tg_client.send_code_request(self.phone_number)

