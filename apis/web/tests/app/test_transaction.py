import json
from flask.wrappers import Response
from tests.base_test import BaseTest


class TestTransaction(BaseTest):
    def test_transaction_with_valid_credentials(self):
        response = self.transaction(self.username, self.password)
        self.assertEqual(response.status_code, 200)

    def test_transaction_with_invalid_credentials(self):
        username, password = 'foo', 'bar'
        response = self.transaction(username, password)
        self.assertEqual(response.status_code, 404)

        response_text = response.get_data(as_text=True)
        self.assertEqual(response_text, f'Error on account login: {username}')

    def test_transaction_result_data_type(self):
        response = self.transaction(self.username, self.password)
        transactions = json.loads(response.data)
        self.assertEqual(type(transactions), list)

        for d in transactions:
            date, amount = d['date'], d['amount']
            self.assertEqual(type(date), str)
            self.assertEqual(type(amount), float)

    def transaction(self, username: str, password: str) -> Response:
        headers = {'Content-Type': 'application/json'}
        data = json.dumps({'username': username, 'password': password})
        return self.client.post('/transaction', data=data, headers=headers)
