import json
import requests
import psycopg2
import docker
from docker.models.containers import Container
from collections import namedtuple
from datetime import datetime

WEB_API_HOST = 'localhost'
WEB_API_PORT = 5000


def get_accounts() -> list:
    query = """SELECT username, password
               FROM account;"""
    rows = execute_and_fetchall(query)
    Account = namedtuple('Account', 'username, password')
    return [Account(*row) for row in rows]


def insert_account(username: str, password: str):
    query = f"""INSERT INTO account (username, password)
                VALUES ('{username}', '{password}')
                ON CONFLICT DO NOTHING;"""
    execute_and_commit(query)


def get_balances_by_username(username) -> list:
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


def get_demo_balances_by_username(username, cutoff=datetime(2019, 8, 24)) -> list:
    if not username_valid(username):
        return []

    def parse_date(date):
        return '{:04d}/{:02d}/{:02d}'.format(date.year, date.month, date.day)

    query = f"""SELECT retrieve_date, amount
                FROM balance
                WHERE username = '{username}'
                    AND retrieve_date <= '{parse_date(cutoff)}'
                ORDER BY id;"""
    rows = execute_and_fetchall(query)
    return [(parse_date(date), amount) for date, amount in rows]


def get_latest_balances_by_chat_id(chat_id: int) -> list:
    UserBalance = namedtuple('UserBalance', 'username, amount')

    query = f"""SELECT DISTINCT balance.username, balance.amount
                FROM subscription
                INNER JOIN (
                    SELECT id, username, amount
                    FROM balance
                    WHERE balance.id IN (
                        SELECT MAX(id) FROM balance GROUP BY username
                    )
                ) AS balance
                ON subscription.username = balance.username
                    AND subscription.chat_id = {chat_id};"""
    rows = execute_and_fetchall(query)
    db_balances = [UserBalance(*row) for row in rows]

    query = f"""SELECT DISTINCT account.username, account.password
                FROM subscription
                INNER JOIN account
                    ON account.username = subscription.username
                WHERE subscription.chat_id = {chat_id};"""
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


def insert_balance(username, retrieve_date, amount):
    query = f"""INSERT INTO balance (username, retrieve_date, amount) 
                VALUES ('{username}', '{retrieve_date}', {amount});"""
    execute_and_commit(query)


def get_subscriptions_by_chat_id(chat_id: int) -> list:
    query = f"""SELECT id, username, amount, chat_id
                FROM subscription
                WHERE chat_id = {chat_id};"""
    rows = execute_and_fetchall(query)
    Subscription = namedtuple('Subscription', 'id, username, amount, chat_id')
    return [Subscription(*row) for row in rows]


def insert_subscription(username: str, amount: float, chat_id: int):
    if not username_valid(username):
        return False

    query = f"""INSERT INTO subscription (username, amount, chat_id)
                VALUES ('{username}', '{amount}', '{chat_id}')
                ON CONFLICT DO NOTHING;"""
    execute_and_commit(query)


def delete_subscription_by_id(id: int):
    query = f"""DELETE FROM subscription
                WHERE id = {id};"""
    execute_and_commit(query)


def get_notifications() -> list:
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
                AND message_date < DATE '2019-10-09'
        );
    
        SELECT username, amount, chat_id
        FROM all_notes
        LEFT JOIN latest_notes
        USING (username, chat_id)
        WHERE latest_notes.message_date <= CURRENT_DATE - interval '3 days';
            OR (latest_notes.username IS NULL AND latest_notes.chat_id IS NULL);
    """
    rows = execute_and_fetchall(query)
    Notification = namedtuple('Notification', 'username, amount, chat_id')
    return [Notification(*row) for row in rows]


def insert_notification(username: str, chat_id: int, message_date):
    query = f"""INSERT INTO notification (username, chat_id, message_date)
                VALUES ('{username}', {chat_id}, '{message_date}');"""
    execute_and_commit(query)


def username_valid(username: str) -> bool:
    """
    Ensures that input username is valid (i.e. exists in database).

    :param username: username of length 8 (by SUTD EVS standard)
    :return: True if valid
    """
    all_usernames = set(acc.username for acc in get_accounts())
    return username in all_usernames


def get_amount(username, password):
    url = f'http://{WEB_API_HOST}:{WEB_API_PORT}/credit'
    headers = {'Content-Type': 'application/json'}
    data = json.dumps({'username': username, 'password': password})
    req = requests.post(url, headers=headers, data=data)
    if req.ok:
        return float(req.text)
    else:
        return -1


def execute_and_commit(query):
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(query)
            conn.commit()


def execute_and_fetchall(query) -> list:
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(query)
            rows = cursor.fetchall()
    return rows


def get_connection():
    container = get_docker_container_by_name('pg-docker')
    ip_address, port = get_network_settings_from_container(container)
    conn = psycopg2.connect(dbname='evs',
                            user='postgres',
                            password='docker',
                            host=ip_address,
                            port=port)
    return conn


def get_docker_container_by_name(name: str) -> Container:
    client = docker.from_env()
    container_list = client.containers.list(filters={'name': name})
    assert len(container_list) == 1, f'Could not find Docker container with name: {name}'
    return container_list[0]


def get_network_settings_from_container(container: Container):
    settings = container.attrs['NetworkSettings']
    ip_address = settings['IPAddress']

    ports = list(settings['Ports'].keys())
    assert len(ports) == 1, f'Found multiple ports in Docker container: {container.name}'
    port = int(ports[0].split('/')[0])  # '5432/tcp' -> 5432

    return ip_address, port
