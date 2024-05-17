from datetime import datetime
import pytz
import config
import telethon
from telethon.sync import TelegramClient
from telethon.tl.types import Message
from dotenv import load_dotenv
import os

# project imports
import db


class SyncTelegramClient(TelegramClient):
    session = 'telethon_sync'

    def __init__(self):
        load_dotenv()
        self.user_data = os.path.join(os.path.expanduser('~'), config.data_dir)
        session = os.path.join(
            os.path.join(os.path.expanduser('~'), config.data_dir), self.session
        )
        super().__init__(
            session=session,
            api_id=os.getenv('API_ID'),
            api_hash=os.getenv('API_HASH')
        )
        self.connect()
        self.me = db.get_me()

    def login(self, phone_number, auth_code) -> bool:
        self.sign_in(phone=phone_number,
                     code=auth_code)
        return self.create_me()

    def is_logged_in(self) -> bool:
        return self.is_user_authorized()

    def create_me(self) -> bool:
        tg_me = self.get_me()
        self.me = db.add_contact(user_id=tg_me.id,
                                 name=tg_me.first_name,
                                 username=tg_me.username,
                                 is_me=True)
        self.update_remote_profile_pic(self.me)
        return self.me is not None

    def send_unichat_message(self, to_contact, text) -> db.UniChatMessage:
        unichat_message = db.UniChatMessage.create(from_contact=self.me,
                                                   to_contact=to_contact,
                                                   text=text,
                                                   timestamp=datetime.now())
        try:
            self.send_message(to_contact.user_id, text)
        except telethon.errors.rpcerrorlist.UserIsBotError:
            self.send_message(to_contact.username, text)
        except ValueError:
            self.send_message(to_contact.username, text)
        return unichat_message

    @staticmethod
    def get_user_id_from_tg_message(message: Message):
        try:
            from_id = message.from_id.user_id
        except AttributeError:
            from_id = message.peer_id.user_id
        return from_id

    def download_photo_from_tg_message(self, message: Message):
        file_path = os.path.join(os.path.expanduser('~'), config.data_dir)
        new_path = self.download_media(message, file=file_path)
        return new_path

    def save_unichat_message(self, message: Message) -> db.UniChatMessage:
        from_id = self.get_user_id_from_tg_message(message)
        if from_id == self.me.user_id:
            from_contact = self.me
            to_contact = db.get_contact(message.peer_id.user_id)
        else:
            from_contact = db.get_contact(message.peer_id.user_id)
            to_contact = self.me
        self.download_photo_from_tg_message(message)

        photo_path = self.download_photo_from_tg_message(message)

        timestamp = message.date.astimezone(pytz.timezone('CET'))
        unichat_message = db.UniChatMessage.create(from_contact=from_contact,
                                                   to_contact=to_contact,
                                                   text=message.message,
                                                   photo_path=photo_path,
                                                   timestamp=timestamp)
        return unichat_message

    def update_remote_profile_pic(self, contact: db.Contact) -> bool:
        pic_path = str(contact.user_id) + '.jpg'
        file_path = os.path.join(self.user_data, pic_path)
        new_path = self.download_profile_photo(contact.user_id, file=file_path)
        if new_path:
            contact.profile_pic = new_path
            return contact.save()
