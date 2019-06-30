from tests.base_test import BaseTest
from web.balance import get_amount


class TestGetAmount(BaseTest):
    def test_successful_login(self):
        amount = get_amount(self.username, self.password)
        self.assertEqual(type(amount), float)

    def test_unsuccessful_login(self):
        username, password = 'foo', 'bar'
        with self.assertRaises(AssertionError):
            get_amount(username, password)
