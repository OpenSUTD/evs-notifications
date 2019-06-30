import json
from flask.wrappers import Response
from tests.base_test import BaseTest


class TestValidate(BaseTest):
    def test_validate_with_valid_credentials(self):
        response = self.validate(self.username, self.password)
        self.assertEqual(response.status_code, 200)

        valid = json.loads(response.data)['valid']
        self.assertTrue(valid)

    def test_validate_with_invalid_credentials(self):
        username, password = 'foo', 'bar'
        response = self.validate(username, password)
        self.assertEqual(response.status_code, 200)

        valid = json.loads(response.data)['valid']
        self.assertFalse(valid)

    def validate(self, username: str, password: str) -> Response:
        headers = {'Content-Type': 'application/json'}
        data = json.dumps({'username': username, 'password': password})
        return self.client.post('/validate', data=data, headers=headers)
