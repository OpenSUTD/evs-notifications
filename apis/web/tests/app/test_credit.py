import json
from flask.wrappers import Response
from tests.app.base_test import BaseTest


class TestCredit(BaseTest):
    def test_credit_can_be_converted_to_float(self):
        response = self.credit(self.username, self.password)
        self.assertEqual(response.status_code, 200)

        amount = float(response.data)
        self.assertEqual(type(amount), float)

    def test_credit_with_invalid_credentials(self):
        username, password = 'foo', 'bar'
        response = self.credit(username, password)
        self.assertEqual(response.status_code, 404)

        response_text = response.get_data(as_text=True)
        self.assertEqual(response_text, f'Error on account: {username}')

    def credit(self, username: str, password: str) -> Response:
        headers = {'Content-Type': 'application/json'}
        data = json.dumps({'username': username, 'password': password})
        return self.client.post('/credit', data=data, headers=headers)
