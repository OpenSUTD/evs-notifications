import sys
sys.path.insert(0, '..')

import psycopg2
from collections import namedtuple
import web


def get_connection():
    dbname = 'evs'
    user = 'ubuntu'
    conn = psycopg2.connect(f"dbname='{dbname}' user='{user}'")
    return conn


def execute_and_commit(query):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(query)
    conn.commit()

    cursor.close()
    conn.close()


def execute_and_fetchall(query) -> list:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(query)
    rows = cursor.fetchall()

    cursor.close()
    conn.close()
    return rows


def get_accounts():
    query = """SELECT * FROM account;"""
    rows = execute_and_fetchall(query)
    Account = namedtuple('Account', 'username password')
    return [Account(*row) for row in rows]


def username_valid(username):
    """
    Ensures that input username is valid (i.e. exists in database).

    :param username: username of length 8 (by SUTD EVS standard)
    :return: True if valid
    """
    all_usernames = [acc.username for acc in get_accounts()]
    return username in all_usernames


def get_balances_by_username(username):
    if not username_valid(username):
        return []

    def parse_date(date):
        return '{:04d}/{:02d}/{:02d}'.format(date.year, date.month, date.day)

    query = f"""SELECT retrieve_date, amount
                FROM balance
                WHERE username = '{username}'
                ORDER BY id;"""
    rows = execute_and_fetchall(query)
    return [(parse_date(date), amount) for date, amount in rows]


def insert_balance(username, retrieve_date, amount):
    query = f"""INSERT INTO balance (username, retrieve_date, amount) 
                VALUES ('{username}', '{retrieve_date}', {amount});"""
    execute_and_commit(query)


def add_account(username: str, password: str) -> bool:
    try:
        web.get_amount(username, password)
    except AssertionError:
        return False

    query = f"""INSERT INTO account (username, password)
                VALUES ('{username}', '{password}')
                ON CONFLICT DO NOTHING;"""
    execute_and_commit(query)
    return True


def add_subscription(username: str, amount: str, chat_id: int) -> bool:
    if not username_valid(username):
        return False

    query = f"""INSERT INTO subscription (username, amount, chat_id)
                VALUES ('{username}', '{amount}', '{chat_id}')
                ON CONFLICT DO NOTHING;"""
    execute_and_commit(query)
    return True


def get_notifications():
    query = """SELECT balance.username, balance.amount, chat_id
               FROM subscription
               INNER JOIN (
                   SELECT *
                   FROM balance
                   WHERE balance.id IN (
                       SELECT MAX (id) FROM balance GROUP BY username
                   )
               ) AS balance
               ON balance.username = subscription.username
               AND balance.amount <= subscription.amount;"""
    rows = execute_and_fetchall(query)
    Notification = namedtuple('Notification', 'username amount chat_id')
    return [Notification(*row) for row in rows]
