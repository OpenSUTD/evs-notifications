import json
import unittest
from web.login import login_valid


def read_credentials(filename='tests/credentials.json'):
    with open(filename) as f:
        text = f.read()
    obj = json.loads(text)
    return obj['username'], obj['password']


class TestLoginValid(unittest.TestCase):
    def test_login_is_valid(self):
        username, password = read_credentials()
        result = login_valid(username, password)
        self.assertTrue(result)

    def test_login_is_invalid(self):
        username, password = 'foo', 'bar'
        result = login_valid(username, password)
        self.assertFalse(result)
