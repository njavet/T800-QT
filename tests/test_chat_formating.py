import unittest
import helpers
import json


class TestMessageFormating(unittest.TestCase):
    def setUp(self):
        self.line_length = 64
        with open('tests/resources/messages.json') as f:
            self.data = json.load(f)

    def test_empty_msg(self):
        msg = ''
        formatted_msg = helpers.format_msg(msg, self.line_length)
        self.assertEqual(formatted_msg, msg)

    def test_short_msg_formating(self):
        msg = 'Hello'
        formatted_msg = helpers.format_msg(msg, self.line_length)
        self.assertEqual(formatted_msg, msg)

    def test_message_exact_line_length(self):
        msg = 'a' * self.line_length
        formatted_msg = helpers.format_msg(msg, self.line_length)
        self.assertEqual(formatted_msg, msg)

    def test_word_longer_than_line_length(self):
        msg = 'a' * (self.line_length + 2)
        formatted_msg = helpers.format_msg(msg)
        expected_output = '\n'.join(['a' * self.line_length, 'aa'])
        self.assertEqual(formatted_msg, expected_output)

    def test_message_very_long_message(self):
        msg = self.data['msg0']
        expected_output = '\n'.join(self.data['formatted_msg0'])
        formatted_msg = helpers.format_msg(msg)
        self.assertEqual(formatted_msg, expected_output)

    def test_message_with_many_white_spaces(self):
        msg = self.data['msg1']
        expected_output = '\n'.join(self.data['formatted_msg1'])
        formatted_msg = helpers.format_msg(msg)
        self.assertEqual(formatted_msg, expected_output)

    def test_message_with_longer_than_line_length_in_between(self):
        msg = self.data['msg2']
        expected_output = '\n'.join(self.data['formatted_msg2'])
        formatted_msg = helpers.format_msg(msg)
        self.assertEqual(formatted_msg, expected_output)

    def test_message_with_white_space_start(self):
        msg = self.data['msg3']
        expected_output = '\n'.join(self.data['formatted_msg3'])
        formatted_msg = helpers.format_msg(msg)
        self.assertEqual(formatted_msg, expected_output)


if __name__ == "__main__":
    unittest.main()

