import json
import unittest
from web.login import login_valid


class TestLoginValid(unittest.TestCase):
    def setUp(self):
        with open('tests/credentials.json') as f:
            text = f.read()
        obj = json.loads(text)
        self.username = obj['username']
        self.password = obj['password']

    def test_login_is_valid(self):
        result = login_valid(self.username, self.password)
        self.assertTrue(result)

    def test_login_is_invalid(self):
        username, password = 'foo', 'bar'
        result = login_valid(username, password)
        self.assertFalse(result)
