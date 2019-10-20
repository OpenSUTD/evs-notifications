from collections import namedtuple
from datetime import datetime
from typing import List, NamedTuple
from .exec import execute_and_commit, execute_and_fetchall
from .account import username_valid
from .web import get_amount

DEMO_CUTOFF_DATE = datetime(2019, 8, 24)
UserBalance = namedtuple('UserBalance', 'username, amount')


def get_balances_by_username(username: str) -> List[tuple]:
    if not username_valid(username):
        return []

    def parse_date(date):
        return '{:04d}/{:02d}/{:02d}'.format(date.year, date.month, date.day)

    query = f"""
        SELECT retrieve_date, amount
        FROM balance
        WHERE username = '{username}'
        ORDER BY id
    """
    rows = execute_and_fetchall(query)
    return [(parse_date(date), amount) for date, amount in rows]


def get_demo_balances_by_username(username: str, cutoff=DEMO_CUTOFF_DATE) -> list:
    if not username_valid(username):
        return []

    def parse_date(date):
        return '{:04d}/{:02d}/{:02d}'.format(date.year, date.month, date.day)

    query = f"""
        SELECT retrieve_date, amount
        FROM balance
        WHERE username = '{username}'
            AND retrieve_date <= '{parse_date(cutoff)}'
        ORDER BY id
    """
    rows = execute_and_fetchall(query)
    return [(parse_date(date), amount) for date, amount in rows]


def get_latest_balances_by_chat_id(chat_id: int) -> List[NamedTuple]:
    query = f"""
        SELECT DISTINCT balance.username, balance.amount
        FROM subscription
        INNER JOIN (
            SELECT id, username, amount
            FROM balance
            WHERE balance.id IN (
                SELECT MAX(id) FROM balance GROUP BY username
            )
        ) AS balance
        ON subscription.username = balance.username
            AND subscription.chat_id = {chat_id}
    """
    rows = execute_and_fetchall(query)
    db_balances = [UserBalance(*row) for row in rows]

    query = f"""
        SELECT DISTINCT account.username, account.password
        FROM subscription
        INNER JOIN account
            ON account.username = subscription.username
        WHERE subscription.chat_id = {chat_id}
    """
    accounts = execute_and_fetchall(query)
    web_balances = []
    for username, password in accounts:
        amount = get_amount(username, password)
        web_balances.append(UserBalance(username, amount))

    def get_matching_db_balance(web_balance):
        for db_balance in db_balances:
            if db_balance.username == web_balance.username:
                return db_balance
        return None

    # retrieve from db if web is not available
    balances = []
    for web_balance in web_balances:
        if web_balance.amount != -1:
            balances.append(web_balance)
        else:
            db_balance = get_matching_db_balance(web_balance)
            if db_balance is not None:
                balances.append(db_balance)
            else:
                balances.append(web_balance)
    return sorted(balances)


def insert_balance(username, retrieve_date, amount) -> None:
    query = f"""INSERT INTO balance (username, retrieve_date, amount) 
                VALUES ('{username}', '{retrieve_date}', {amount});"""
    execute_and_commit(query)
