from PySide6.QtWidgets import (
    QWidget,
    QListWidget,
    QListWidgetItem,
    QPushButton,
    QVBoxLayout
)

# project imports
import db
from widgets.contact_item_widget import ContactItemWidget


class ContactListWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.list_widget = QListWidget()
        # TODO layout
        self.list_widget.setMinimumHeight(650)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.addWidget(self.list_widget)
        self.setLayout(layout)
        self.init_contact_list()

    def refresh_contact_list(self):
        self.list_widget.clear()
        self.init_contact_list()

    def init_contact_list(self):
        for contact in db.Contact.select():
            item = QListWidgetItem()
            contact_item = ContactItemWidget(contact)
            item.setSizeHint(contact_item.sizeHint())
            item.setData(101, contact_item)
            self.list_widget.addItem(item)
            self.list_widget.setItemWidget(item, contact_item)

    def add_contact_to_list(self, contact):
        item = QListWidgetItem()
        contact_item = ContactItemWidget(contact)
        item.setSizeHint(contact_item.sizeHint())
        item.setData(101, contact_item)
        self.list_widget.addItem(item)
        self.list_widget.setItemWidget(item, contact_item)
