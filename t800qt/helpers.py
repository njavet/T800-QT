import os
from datetime import datetime, timezone
from typing import Callable

from PySide6.QtCore import QObject, QThread, Signal
from PySide6.QtWidgets import QLabel

# project imports
import config


def get_user_data_path() -> str:
    """
    assert that directory exists after calling this method

    """
    home = os.path.expanduser('~')
    data_dir = os.path.join(home, config.user_data)
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
    return data_dir


def get_database_path():
    """
    returns the path of the database
    TODO such a comment is kind of useless, since the
     function name says it all, empty or useless comment ?

      user_data_dir is created here, probably not good practice
    """
    data_dir_path = get_user_data_path()
    return os.path.join(data_dir_path, config.db_name)


def read_image_file(path: str) -> bytes:
    """
    returns the image from path as bytes
    TODO exception handling

    """
    with open(path, 'rb') as f:
        return f.read()


def get_telethon_session_path(session: str) -> str:
    """
    used for storing the session files in the user data directory

    """
    return os.path.join(get_user_data_path(), session)


def string_to_utc_timestamp(date_string: str) -> str:
    """Convert a date string to a UTC timestamp.

    Args:
        date_string (str): Date string in various formats.

    Returns:
        str: UTC timestamp in ISO 8601 format.
    """

    formats = ['%I:%M %p, %m/%d/%Y', '%H:%M, %d.%m.%Y', '%H:%M, %m/%d/%Y', '%H:%M, %d.%m.%Y']

    for fmt in formats:
        try:
            date_object = datetime.strptime(date_string, fmt)
            date_utc = date_object.replace(tzinfo=timezone.utc)
            return date_utc.isoformat()
        except ValueError:
            pass

    return f"Invalid date format: {date_string}"


def execute_qt_worker(worker: QObject, thread: QThread, sub_func: Callable = None) -> None:
    """Execute a QObject worker inside a QThread with an additional sub function,
    which is called when the worker is finished.

    :param worker: QObject worker to be executed
    :param thread: QThread thread to be executed
    :param sub_func: Function to be executed at the end of the worker task
    """

    worker.moveToThread(thread)
    thread.started.connect(worker.run)
    worker.finished.connect(thread.quit)
    if sub_func:
        worker.finished.connect(sub_func)
    thread.finished.connect(worker.deleteLater)
    thread.finished.connect(thread.quit)
    thread.start()

    
def format_msg(message: str, line_length: int = 48) -> str:
    """
    The `format_msg` function splits a text message into lines of maximum 48 characters each.
    :return: The `format_msg` method returns a formatted message where the original message text is
    split into lines with a maximum of 48 characters per line. The method processes the input
    message text to ensure that each line does not exceed the character limit and handles cases
    where words are too long or lines are too long. The formatted message is returned as a single
    string with line breaks.
    """
    lines = []
    words = message.split()
    curr = 0
    curr_line = []
    for i, word in enumerate(words):
        curr += len(word)
        # Case 1: the word is too long for a single line
        if len(word) > line_length:
            if len(curr_line) == 0:
                while word:
                    lines.append(word[:line_length])
                    word = word[line_length:]
            else:
                lines.append(' '.join(curr_line))
                while word:
                    curr_line.append(word[:line_length])
                    word = word[line_length:]
                    lines.append(' '.join(curr_line))
                curr = 0
                curr_line = []
        # Case 2: the line is too long and has more than 48 characters
        elif curr > line_length:
            curr_line.append(word)
            lines.append(' '.join(curr_line))
            curr = 0
            curr_line = []
        # Case 3: the line still has space
        else:
            curr_line.append(word)

    lines.append(' '.join(curr_line))
    new_msg = '\n'.join(lines)
    return new_msg


def find_xpath_with_class(class_name: str) -> str:
    """Helper to find xpath elements in Instagram web client.

    :param class_name: Instagram html class name.
    :return: string to xpath elements.
    """

    return './/*[@class="' + class_name + '"]'


class ElementHasAttribute(object):
    """An expectation for checking that an element has a particular attribute.

    locator - used to find the element
    returns the WebElement once it has the particular attribute
    """

    def __init__(self, locator, attribute_name):
        self.locator = locator
        self.attribute_name = attribute_name

    def __call__(self, driver):
        # Finding the referenced element
        element = driver.find_element(*self.locator)
        if element.get_attribute(self.attribute_name) is not None:
            return element
        else:
            return False


class ClickableLabel(QLabel):
    """Creates a QLabel that can be clicked."""

    clicked = Signal()

    def mousePressEvent(self, event):
        self.clicked.emit()
        QLabel.mousePressEvent(self, event)
