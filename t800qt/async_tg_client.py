from PySide6.QtCore import QObject, Signal
from telethon import TelegramClient, events
from telethon.events import NewMessage
from dotenv import load_dotenv
import asyncio
import os


class AsyncTelegramClientWorker(QObject):
    msg_receive_signal = Signal(events.newmessage.NewMessage)
    session = 'telethon_async'

    def __init__(self):
        super().__init__()
        # load telegram api keys
        load_dotenv()
        self.api_id = int(os.getenv('API_ID'))
        self.api_hash = os.getenv('API_HASH')
        self.telethon_client = self.init_telethon_client()

    def init_telethon_client(self):
        """
        asyncio event loop
        """
        user_session = '/home/tosh/t800qt_user_data/telethon_async'
        telethon_client = TelegramClient(user_session,
                                         self.api_id,
                                         self.api_hash)

        telethon_client.add_event_handler(self.msg_handler,
                                          NewMessage(outgoing=False))
        return telethon_client

    async def msg_handler(self, event):
        self.msg_receive_signal.emit(event.message)

    def run(self):
        """
        called from the qt app
        """
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        self.telethon_client.start()
        with self.telethon_client:
            self.telethon_client.run_until_disconnected()
