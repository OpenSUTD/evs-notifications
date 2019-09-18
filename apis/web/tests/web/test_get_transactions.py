from datetime import datetime
from bs4 import BeautifulSoup
from tests.base_test import BaseTest
from web.transaction import (Transaction, get_transactions, get_transactions_demo,
                             row_to_transaction, transaction_to_dict)


class TestGetTransactions(BaseTest):
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

    def test_get_transactions_demo(self):
        transactions = get_transactions_demo(self.username, self.password)
        self.assertEqual(type(transactions), list)

    def test_get_transactions_demo_attributes(self):
        transactions = get_transactions_demo(self.username, self.password)
        for txn in transactions:
            self.assertEqual(type(txn), dict)

            date, amount = txn['date'], txn['amount']
            self.assertEqual(type(date), str)
            self.assertEqual(type(amount), float)

    def test_get_transactions_demo_cutoff(self):
        cutoff = datetime(2019, 6, 1)
        transactions = get_transactions_demo(self.username, self.password, cutoff)
        for txn in transactions:
            date = txn['date']
            self.assertLessEqual(datetime.strptime(date, '%Y-%m-%d'),
                                 cutoff)
