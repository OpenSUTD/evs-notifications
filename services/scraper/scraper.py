import sys
sys.path.insert(0, '..')

from datetime import datetime
import web
import database as db


def get_date():
    now = datetime.now()
    return '{:04d}/{:02d}/{:02d}'.format(now.year, now.month, now.day)


def add_account_balance(account):
    date = get_date()
    amount = web.get_amount(account.username, account.password)
    db.insert_balance(account.username, date, amount)


def add_all_balances():
    accounts = db.get_accounts()
    for account in accounts:
        add_account_balance(account)
