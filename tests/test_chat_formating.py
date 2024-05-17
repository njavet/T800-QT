import unittest
import helpers
import json


class TestMessageFormating(unittest.TestCase):
    def test_short_msg_formating(self):
        short_msg = 'Hello'
        formatted_short_msg = helpers.format_msg(short_msg)
        self.assertEqual(formatted_short_msg, short_msg)

    def test_message_48a(self):
        exact_48_msg = 'a' * 48
        formatted_exact_48_msg = helpers.format_msg(exact_48_msg)
        self.assertEqual(formatted_exact_48_msg, exact_48_msg)

    def test_long_message_50a(self):
        long_msg = 'a' * 50
        formatted_long_msg = helpers.format_msg(long_msg)
        # Split after 48 characters
        expected_output = '\n'.join(['a' * 48, 'aa\n'])
        self.assertEqual(formatted_long_msg, expected_output)

    def test_long_smith_message(self):
        with open('tests/resources/long_smith_message.json') as f:
            data = json.load(f)
        input_msg = data['input']
        expected_output = '\n'.join(data['lines'])
        formatted_msg = helpers.format_msg(input_msg)
        self.assertEqual(formatted_msg, expected_output)


if __name__ == "__main__":
    unittest.main()

