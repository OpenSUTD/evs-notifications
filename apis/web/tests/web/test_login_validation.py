from tests.base_test import BaseTest
from web.login import login_valid


class TestLoginValid(BaseTest):
    def test_login_is_valid(self):
        result = login_valid(self.username, self.password)
        self.assertTrue(result)

    def test_login_is_invalid(self):
        username, password = 'foo', 'bar'
        result = login_valid(username, password)
        self.assertFalse(result)
