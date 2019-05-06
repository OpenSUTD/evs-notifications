import psycopg2
from collections import namedtuple

Account = namedtuple('Account', 'username,password,name')


def get_connection():
    dbname = 'evs'
    user = 'ubuntu'
    conn = psycopg2.connect(f"dbname='{dbname}' user='{user}'")
    return conn


def get_accounts():
    query = """SELECT * FROM account;"""

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(query)
    rows = cursor.fetchall()

    cursor.close()
    conn.close()
    return [Account(*row) for row in rows]


def get_balances_by_username(username):
    query = f"""SELECT balance.retrieve_date, balance.amount
                FROM balance
                WHERE balance.username = '{username}';"""

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(query)
    rows = cursor.fetchall()

    cursor.close()
    conn.close()

    parse_date = lambda date: '{:04d}/{:02d}/{:02d}'.format(date.year, date.month, date.day)
    return [(parse_date(date), amount) for date, amount in rows]


def insert_balance(username, retrieve_date, amount):
    query = f"""INSERT INTO balance (username, retrieve_date, amount) 
                VALUES ('{username}', '{retrieve_date}', {amount});"""

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(query)
    conn.commit()

    cursor.close()
    conn.close()
