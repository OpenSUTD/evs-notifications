import json
from unittest import TestCase
from app import app


class BaseTest(TestCase):
    def setUp(self):
        app.testing = True
        self.client = app.test_client()

        filename = 'tests/credentials.json'
        self.username, self.password = self.read_credentials(filename)

    def read_credentials(self, filename):
        with open(filename) as f:
            text = f.read()
        obj = json.loads(text)
        return obj['username'], obj['password']
