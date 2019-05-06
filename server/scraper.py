from datetime import datetime
import web
import psql


def get_date():
    now = datetime.now()
    return '{:04d}/{:02d}/{:02d}'.format(now.year, now.month, now.day)


if __name__ == '__main__':
    accounts = psql.get_accounts()
    for account in accounts:
        date = get_date()
        amount = web.get_amount(account.username, account.password)
        psql.insert_balance(account.username, date, amount)
