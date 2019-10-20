import json
from unittest import TestCase
from app import app

# TODO - mock DB connection
DOCKER_CONTAINER_NOT_FOUND_ERROR = AssertionError


class TestApp(TestCase):
    def test_get_account(self):
        with self.assertRaises(DOCKER_CONTAINER_NOT_FOUND_ERROR):
            self.client.get('/account')

    def test_post_account(self):
        with self.assertRaises(DOCKER_CONTAINER_NOT_FOUND_ERROR):
            headers = {'Content-Type': 'application/json'}
            data = json.dumps({
                'username': 'username',
                'password': 'password',
            })
            self.client.post('/account', data=data, headers=headers)

    def test_get_balance_by_user(self):
        with self.assertRaises(DOCKER_CONTAINER_NOT_FOUND_ERROR):
            self.client.get('/balance/username/username')

    def test_get_demo_balances_by_username(self):
        with self.assertRaises(DOCKER_CONTAINER_NOT_FOUND_ERROR):
            self.client.get('/balance/username/demo/username')

    def test_get_latest_balance_by_chat_id(self):
        with self.assertRaises(DOCKER_CONTAINER_NOT_FOUND_ERROR):
            self.client.get('/balance/chatid/chat_id')

    def test_insert_balance(self):
        with self.assertRaises(DOCKER_CONTAINER_NOT_FOUND_ERROR):
            headers = {'Content-Type': 'application/json'}
            data = json.dumps({
                'username': 'username',
                'retrieve_date': 'YYYY-MM-DD',
                'amount': 0.0,

            })
            self.client.post('/balance', data=data, headers=headers)

    def test_get_subscriptions_by_chat_id(self):
        with self.assertRaises(DOCKER_CONTAINER_NOT_FOUND_ERROR):
            self.client.get('/subscription/chat_id')

    def test_insert_subscription(self):
        with self.assertRaises(DOCKER_CONTAINER_NOT_FOUND_ERROR):
            headers = {'Content-Type': 'application/json'}
            data = json.dumps({
                'username': 'username',
                'amount': 0.0,
                'chat_id': 'chat_id',
            })
            self.client.post('/subscription', data=data, headers=headers)

    def test_delete_subscription_by_id(self):
        with self.assertRaises(DOCKER_CONTAINER_NOT_FOUND_ERROR):
            self.client.delete('/subscription/subscription_id')

    def test_get_notifications(self):
        with self.assertRaises(DOCKER_CONTAINER_NOT_FOUND_ERROR):
            self.client.get('/notification')

    def test_insert_notification(self):
        with self.assertRaises(DOCKER_CONTAINER_NOT_FOUND_ERROR):
            headers = {'Content-Type': 'application/json'}
            data = json.dumps({
                'username': 'username',
                'chat_id': 'chat_id',
                'message_date': 'YYYY-MM-DD',
            })
            self.client.post('/notification', data=data, headers=headers)

    @classmethod
    def setUpClass(cls):
        app.testing = True
        cls.client = app.test_client()
