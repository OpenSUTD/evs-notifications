from collections import namedtuple
from typing import List, NamedTuple
from .exec import execute_and_fetchall, execute_and_commit


Account = namedtuple('Account', 'username, password')


def get_accounts() -> List[NamedTuple]:
    query = """
        SELECT username, password
        FROM account
    """
    rows = execute_and_fetchall(query)
    return [Account(*row) for row in rows]


def insert_account(username: str, password: str) -> None:
    query = f"""
        INSERT INTO account (username, password)
        VALUES ('{username}', '{password}')
        ON CONFLICT DO NOTHING
    """
    execute_and_commit(query)


def username_valid(username: str) -> bool:
    """
    Ensures that input username is valid (i.e. exists in database).

    :param username: username of length 8 (by SUTD EVS standard)
    :return: True if valid
    """
    all_usernames = set(acc.username for acc in get_accounts())
    return username in all_usernames
