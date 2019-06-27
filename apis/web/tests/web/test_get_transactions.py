import json
import unittest
from bs4 import BeautifulSoup
from web.transaction import Transaction, get_transactions, row_to_transaction, transaction_to_dict


class TestGetTransactions(unittest.TestCase):
    def setUp(self):
        with open('tests/credentials.json') as f:
            text = f.read()
        obj = json.loads(text)
        self.username = obj['username']
        self.password = obj['password']

    def test_row_to_transaction(self):
        data = ('<tr>'
                '  <td>transaction_id</td>'
                '  <td>date</td>'
                '  <td>amount</td>'
                '  <td>offer_id</td>'
                '  <td>payment_mode</td>'
                '  <td>channel</td>'
                '  <td>status</td>'
                '</tr>')
        soup = BeautifulSoup(data, 'html.parser')
        result = row_to_transaction(soup.tr)

        txn = Transaction(transaction_id='transaction_id',
                          date='date',
                          amount='amount',
                          offer_id='offer_id',
                          payment_mode='payment_mode',
                          channel='channel',
                          status='status')
        self.assertEqual(result, txn)

    def test_transaction_to_dict(self):
        data = Transaction(date='01/01/2019 00:00', amount='10.00',
                           transaction_id=None, offer_id=None, payment_mode=None, channel=None, status=None)
        result = transaction_to_dict(data)
        self.assertEqual(result, {'date': '2019-01-01', 'amount': 10})

    def test_get_transactions(self):
        transactions = get_transactions(self.username, self.password)
        self.assertEqual(type(transactions), list)

    def test_get_transactions_attributes(self):
        transactions = get_transactions(self.username, self.password)
        for txn in transactions:
            self.assertEqual(type(txn), dict)

            date, amount = txn['date'], txn['amount']
            self.assertEqual(type(date), str)
            self.assertEqual(type(amount), float)
