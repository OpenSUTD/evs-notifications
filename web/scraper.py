from datetime import datetime
import web
import psql


def get_date():
    now = datetime.now()
    return '{:04d}/{:02d}/{:02d}'.format(now.year, now.month, now.day)


def add_account_balance(account):
    date = get_date()
    amount = web.get_amount(account.username, account.password)
    psql.insert_balance(account.username, date, amount)


def add_all_balances():
    accounts = psql.get_accounts()
    for account in accounts:
        add_account_balance(account)


if __name__ == '__main__':
    add_all_balances()
