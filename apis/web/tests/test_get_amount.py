import json
import unittest
from web import get_amount


def read_credentials(filename='tests/credentials.json'):
    with open(filename) as f:
        text = f.read()
    obj = json.loads(text)
    return obj['username'], obj['password']


class TestGetAmount(unittest.TestCase):
    def test_successful_login(self):
        username, password = read_credentials()
        amount = get_amount(username, password)
        self.assertEqual(type(amount), float)

    def test_unsuccessful_login(self):
        username, password = 'foo', 'bar'
        with self.assertRaises(AssertionError):
            get_amount(username, password)
