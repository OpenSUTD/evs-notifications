from collections import namedtuple
from typing import List, NamedTuple
from .exec import execute_and_fetchall, execute_and_commit
from .account import username_valid

Subscription = namedtuple('Subscription', 'id, username, amount, chat_id')


def get_subscriptions_by_chat_id(chat_id: int) -> List[NamedTuple]:
    query = f"""
        SELECT id, username, amount, chat_id
        FROM subscription
        WHERE chat_id = {chat_id}
    """
    rows = execute_and_fetchall(query)
    return [Subscription(*row) for row in rows]


def insert_subscription(username: str, amount: float, chat_id: int) -> None:
    if not username_valid(username):
        return

    query = f"""
        INSERT INTO subscription (username, amount, chat_id)
        VALUES ('{username}', '{amount}', '{chat_id}')
        ON CONFLICT DO NOTHING
    """
    execute_and_commit(query)


def delete_subscription_by_id(id: int) -> None:
    query = f"""
        DELETE FROM subscription
        WHERE id = {id}
    """
    execute_and_commit(query)
