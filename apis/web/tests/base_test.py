import json
from unittest import TestCase
from app import app


class BaseTest(TestCase):
    @classmethod
    def setUpClass(cls):
        app.testing = True
        cls.client = app.test_client()

        filename = 'tests/credentials.json'
        cls.username, cls.password = cls.read_credentials(filename)

    @staticmethod
    def read_credentials(filename):
        with open(filename) as f:
            text = f.read()
        obj = json.loads(text)
        return obj['username'], obj['password']
