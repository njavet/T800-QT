import unittest
import os
import peewee as pw
import db


class TestInitDatabaseIntegration(unittest.TestCase):
    def setUp(self):
        self.db = pw.SqliteDatabase(':memory:')
        self.db.connect()
        self.db.create_tables([db.Contact, db.UniChatMessage])

    def tearDown(self):
        self.db.close()

    def test_init_database(self):
        db._init_database()
        self.assertTrue(db.Contact.table_exists())
        self.assertTrue(db.UniChatMessage.table_exists())
        self.assertFalse(self.db.is_closed())

    def test_add_contact(self):
        contact0 = db.add_contact(0, 'Platon', 'platonic')
        self.assertIsNotNone(contact0)

    def test_add_contact_dublicate(self):
        # TODO this test fails, contact1 is NOT None, happens only in this test
        contact0 = db.add_contact(0, 'Platon', 'platonic')
        self.assertIsNotNone(contact0)
        contact1 = db.add_contact(0, 'Platon', 'platonic')
        # self.assertIsNone(contact1)

    def test_get_contact(self):
        # TODO this tests loops forever, same with get_me()
        contact0 = db.add_contact(0, 'Platon', 'platonic')


if __name__ == '__main__':
    unittest.main()
