from collections import namedtuple
from typing import List, NamedTuple
from .exec import execute_and_fetchall, execute_and_commit

Notification = namedtuple('Notification', 'username, amount, chat_id')


def get_notifications() -> List[NamedTuple]:
    query = """
        CREATE TEMP VIEW all_notes AS (
            SELECT DISTINCT balance.username, balance.amount, chat_id
            FROM subscription
            INNER JOIN (
               SELECT id, username, amount
               FROM balance
               WHERE balance.id IN (
                   SELECT MAX(id) FROM balance GROUP BY username
               )
            ) AS balance
            ON balance.username = subscription.username
               AND balance.amount <= subscription.amount
        );

        CREATE TEMP VIEW latest_notes AS (
            SELECT username, chat_id, message_date
            FROM notification
            WHERE notification.id IN (
                SELECT MAX (id) FROM notification GROUP BY username, chat_id
            )
        );

        SELECT username, amount, chat_id
        FROM all_notes
        LEFT JOIN latest_notes
        USING (username, chat_id)
        WHERE latest_notes.message_date <= CURRENT_DATE - interval '3 days'
            OR (latest_notes.username IS NULL AND latest_notes.chat_id IS NULL);
    """
    rows = execute_and_fetchall(query)
    return [Notification(*row) for row in rows]


def insert_notification(username: str, chat_id: int, message_date):
    query = f"""INSERT INTO notification (username, chat_id, message_date)
                VALUES ('{username}', {chat_id}, '{message_date}');"""
    execute_and_commit(query)
