import json
import unittest
from web.balance import get_amount


class TestGetAmount(unittest.TestCase):
    def setUp(self):
        with open('tests/credentials.json') as f:
            text = f.read()
        obj = json.loads(text)
        self.username = obj['username']
        self.password = obj['password']

    def test_successful_login(self):
        amount = get_amount(self.username, self.password)
        self.assertEqual(type(amount), float)

    def test_unsuccessful_login(self):
        username, password = 'foo', 'bar'
        with self.assertRaises(AssertionError):
            get_amount(username, password)
