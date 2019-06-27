import unittest
from web.utils import get_request_params


class TestRequestParams(unittest.TestCase):
    def test_output_type(self):
        username, password = 'user', 'pass'
        data, headers = get_request_params(username, password)
        self.assertTrue(type(data) == type(headers) == dict)

    def test_output_headers(self):
        username, password = 'user', 'pass'
        _, headers = get_request_params(username, password)
        self.assertEqual(headers, {'Content-Type': 'application/x-www-form-urlencoded'})

    def test_output_data(self):
        username, password = 'user', 'pass'
        data, _ = get_request_params(username, password)
        self.assertEqual(data, {
            'txtLoginId': username,
            'txtPassword': password,
            'btnLogin': 'Login',
        })
