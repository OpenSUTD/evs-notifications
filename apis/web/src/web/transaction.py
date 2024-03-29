import requests
import bs4
from bs4 import BeautifulSoup
from collections import namedtuple
from datetime import datetime
from .utils import login_url, transaction_url, get_request_params
from .exceptions import LoginError


Transaction = namedtuple('Transaction', 'transaction_id,'
                                        'date,'
                                        'amount,'
                                        'offer_id,'
                                        'payment_mode,'
                                        'channel,'
                                        'status')


def get_transactions(username: str, password: str) -> list:
    # see transaction_to_dict for format of each transaction returned
    with requests.session() as sess:
        data, headers = get_request_params(username, password)

        # store login cookies in session
        r = sess.post(url=login_url, data=data, headers=headers, verify=False)
        if 'Invalid' in r.url:
            raise LoginError('Wrong login credentials')

        r = sess.get(transaction_url)
        html_text = r.text
    return get_transactions_from_html_page(html_text)


def get_transactions_demo(username: str, password: str, cutoff=datetime(2019, 8, 24)) -> list:
    transactions = get_transactions(username, password)
    transactions_demo = [txn for txn in transactions
                         if datetime.strptime(txn['date'], '%Y-%m-%d') <= cutoff]
    return transactions_demo


def get_transactions_from_html_page(html_text: str) -> list:
    soup = BeautifulSoup(html_text, 'html.parser')
    rows = soup.find_all('tr', attrs='tblRow')
    transactions = (row_to_transaction(row) for row in rows)
    return [transaction_to_dict(txn) for txn in transactions]


def row_to_transaction(row: bs4.element.Tag) -> Transaction:
    """
    Convert HTML string of one <tr> with multiple <td> entries into named tuple.

    :param row: HTML string of the entire <tr> tag, including <td> tags
    :return: Transaction named tuple with corresponding entries
    """
    args = (elem.text.strip() for elem in row.find_all('td'))
    return Transaction(*args)


def transaction_to_dict(txn: Transaction) -> dict:
    """
    Convert Transaction tuple into dictionary to be returned as JSON object.

    :param txn: Transaction named tuple with corresponding entries
    :return: Dictionary containing date and amount, with relevant formatting
    """
    date_obj = datetime.strptime(txn.date, '%d/%m/%Y %H:%M')
    date_str = date_obj.strftime('%Y-%m-%d')
    amount = float(txn.amount)
    return {'date': date_str, 'amount': amount}
