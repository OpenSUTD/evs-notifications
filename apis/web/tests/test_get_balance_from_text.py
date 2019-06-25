import unittest
from web.balance import get_balance_from_text


class TestGetBalance(unittest.TestCase):
    def test_return_type(self):
        text = 'S$ 0.00' * 2
        result = get_balance_from_text(text)
        self.assertEqual(type(result), float)

    # test regex group \d{1,3}\.\d{2}
    def test_zero(self):
        text = 'S$ 0.00' * 2
        self.assertEqual(get_balance_from_text(text), 0)

    def test_less_than_ten(self):
        text = 'S$ 9.99' * 2
        self.assertEqual(get_balance_from_text(text), 9.99)

    def test_less_than_hundred(self):
        text = 'S$ 99.99' * 2
        self.assertEqual(get_balance_from_text(text), 99.99)

    def test_less_than_thousand(self):
        text = 'S$ 999.999' * 2
        self.assertEqual(get_balance_from_text(text), 999.99)

    # test regex group (\d{1,3},)*
    def test_less_than_million(self):
        text = 'S$ 999,999.99' * 2
        self.assertEqual(get_balance_from_text(text), 999_999.99)

    def test_less_than_billion(self):
        text = 'S$ 999,999,999.99' * 2
        self.assertEqual(get_balance_from_text(text), 999_999_999.99)

    # test assertion error
    def test_empty_string(self):
        text = ''
        with self.assertRaises(AssertionError):
            get_balance_from_text(text)

    def test_one_match(self):
        text = 'S$ 0.00'
        with self.assertRaises(AssertionError):
            get_balance_from_text(text)

    def test_no_decimal(self):
        text = 'S$ 10' * 2
        with self.assertRaises(AssertionError):
            get_balance_from_text(text)
