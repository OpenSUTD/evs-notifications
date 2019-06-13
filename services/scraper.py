import json
import requests
from datetime import datetime
from collections import namedtuple

WEB_API_HOST = 'localhost'
WEB_API_PORT = 5000

DB_API_HOST = 'localhost'
DB_API_PORT = 8001


class RetrieveError(Exception):
    pass


def get_date():
    now = datetime.now()
    return '{:04d}/{:02d}/{:02d}'.format(now.year, now.month, now.day)


def get_accounts():
    url = f'http://{DB_API_HOST}:{DB_API_PORT}/account'
    req = requests.get(url)
    rows = json.loads(req.text)
    Account = namedtuple('Account', 'username, password')
    return [Account(*row) for row in rows]


def get_amount(account):
    url = f'http://{WEB_API_HOST}:{WEB_API_PORT}/credit'
    headers = {'Content-Type': 'application/json'}
    data = json.dumps({'username': account.username, 'password': account.password})
    req = requests.get(url, headers=headers, data=data)

    if not req.ok:
        raise RetrieveError(username)

    amount = json.loads(req.text)['amount']
    return amount


def post_balance(username, date, amount):
    url = f'http://{DB_API_HOST}:{DB_API_PORT}/balance'
    headers = {'Content-Type': 'application/json'}
    data = json.dumps({'username': username, 'retrieve_date': date, 'amount': amount})
    requests.post(url, headers=headers, data=data)


def add_account_balance(account):
    date = get_date()
    try:
        amount = get_amount(account)
    except RetrieveError as e:
        print('Error retrieving account:', e)
        return
    post_balance(account.username, date, amount)


def main():
    accounts = get_accounts()
    for account in accounts:
        print(account)
        add_account_balance(account)


if __name__ == '__main__':
    main()
