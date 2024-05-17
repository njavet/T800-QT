import os
import unittest
import peewee
from unittest.mock import patch, MagicMock

import db
import config


class TestCreateDataDirs(unittest.TestCase):
    @patch('os.path.exists')
    @patch('os.makedirs')
    @patch('os.path.join')
    @patch('os.path.expanduser')
    def test_create_user_data_dir_new(self,
                                      mock_expanduser,
                                      mock_join,
                                      mock_makedirs,
                                      mock_exists):
        # prepare mocks
        mock_expanduser.return_value = '/home/user'
        data_path = os.path.join('/home/user', config.data_dir)
        mock_join.return_value = data_path
        mock_exists.return_value = False

        # call the function
        db._create_user_data_dir()

        # verify calls
        mock_expanduser.assert_called_once_with('~')
        mock_exists.assert_called_once_with(data_path)
        mock_makedirs.assert_called_once_with(data_path)
        assert mock_join.call_count == 2

    @patch('os.path.exists')
    @patch('os.makedirs')
    @patch('os.path.join')
    @patch('os.path.expanduser')
    def test_create_user_data_dir_exists(self,
                                         mock_expanduser,
                                         mock_join,
                                         mock_makedirs,
                                         mock_exists):
        # prepare mocks
        mock_expanduser.return_value = '/home/user'
        data_path = os.path.join('/home/user', config.data_dir)
        mock_join.return_value = data_path
        mock_exists.return_value = True

        # call the function
        db._create_user_data_dir()

        # verify calls
        mock_expanduser.assert_called_once_with('~')
        mock_exists.assert_called_once_with(data_path)
        assert mock_makedirs.call_count == 0
        assert mock_join.call_count == 2


class TestInitDatabase(unittest.TestCase):
    @patch('os.path.join')
    @patch('os.path.expanduser')
    @patch('peewee.SqliteDatabase')
    def test_init_database(self, mock_sqlite_db, mock_expanduser, mock_join):
        # Mock os.path.expanduser() and os.path.join() to return dummy paths
        mock_expanduser.return_value = '/home/user/data'
        mock_join.side_effect = lambda *args: '/home/user/data'

        # Create mock database and meta objects
        mock_database = MagicMock()
        mock_meta = MagicMock()
        mock_database.attach_mock(mock_meta, '_meta')
        mock_sqlite_db.return_value = mock_database

        # Call _init_database()
        db._init_database()

        # Assert that methods were called with the expected parameters
        mock_join.assert_called_with('/home/user/data', config.db_name)
        mock_sqlite_db.assert_called_with('/home/user/data')
        mock_database.connect.assert_called()
        mock_database.create_tables.assert_called_with([db.Contact,
                                                        db.UniChatMessage], safe=True)
        mock_database.close.assert_called()


if __name__ == '__main__':
    unittest.main()

