import os
import logging
import peewee as pw

# project imports
import config
logger = logging.getLogger(__name__)


class BaseModel(pw.Model):
    class Meta:
        database = None


class Contact(BaseModel):
    user_id = pw.IntegerField(primary_key=True)
    profile_pic = pw.CharField(default=config.default_profile_pic_path)
    name = pw.CharField()
    username = pw.CharField(null=True)
    # field for determining if it is the owner
    # TODO check that this can be true only once -> one owner
    is_me = pw.BooleanField(default=False)


class UniChatMessage(BaseModel):
    from_contact = pw.ForeignKeyField(Contact)
    to_contact = pw.ForeignKeyField(Contact)
    timestamp = pw.DateTimeField()
    text = pw.TextField(null=True)
    photo_path = pw.CharField(null=True)
    video_path = pw.CharField(null=True)


# private init functions
def _create_user_data_dir():
    data_dir_path = os.path.join(os.path.expanduser('~'), config.data_dir)
    if not os.path.exists(data_dir_path):
        os.makedirs(data_dir_path)


def _init_database():
    data_dir_path = os.path.join(os.path.expanduser('~'), config.data_dir)
    db_path = os.path.join(data_dir_path, config.db_name)
    database = pw.SqliteDatabase(db_path)
    # TODO find a better solution
    Contact._meta.database = database
    UniChatMessage._meta.database = database
    database.connect()
    database.create_tables([Contact, UniChatMessage], safe=True)
    database.close()


def init_storage():
    _create_user_data_dir()
    _init_database()


def get_me() -> Contact | None:
    try:
        return Contact.get(is_me=True)
    except pw.DoesNotExist:
        return None


def add_contact(user_id, name, username, is_me=False) -> Contact | None:
    try:
        contact = Contact.create(user_id=user_id,
                                 name=name,
                                 username=username,
                                 is_me=is_me)
    except pw.IntegrityError as e:
        logger.error(f'Integrity error: {e}')
        contact = None

    return contact


def get_contact(user_id) -> Contact | None:
    try:
        return Contact.get(user_id=user_id)
    except pw.DoesNotExist:
        return None

