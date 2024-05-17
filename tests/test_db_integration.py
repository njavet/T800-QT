import unittest
import os
import peewee as pw
import db


test_db = pw.SqliteDatabase(':memory:')
models = [db.Contact, db.UniChatMessage]


class TestInitDatabaseIntegration(unittest.TestCase):
    def setUp(self):
        test_db.bind(models)
        test_db.connect()
        test_db.create_tables(models)

    def tearDown(self):
        test_db.drop_tables(models)
        test_db.close()

    def test_init_database(self):
        db._init_database()
        self.assertTrue(db.Contact.table_exists())
        self.assertTrue(db.UniChatMessage.table_exists())
        self.assertFalse(test_db.is_closed())

    def test_add_contact(self):
        contact0 = db.add_contact(0, 'Platon', 'platonic')
        self.assertIsNotNone(contact0)

    def test_add_contact_dublicate(self):
        contact0 = db.add_contact(1, 'Kant', 'k1')
        self.assertIsNotNone(contact0)
        contact1 = db.add_contact(1, 'Platon', 'platonic')
        self.assertIsNone(contact1)

    def test_get_contact(self):
        # TODO this tests loops forever, same with get_me()
        contact0 = db.add_contact(3, 'Platon', 'platonic')
        contact1 = db.get_contact(3)
        self.assertIsNotNone(contact1)



if __name__ == '__main__':
    unittest.main()
