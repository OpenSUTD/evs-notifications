import psycopg2
from collections import namedtuple

Account = namedtuple('Account', 'username,password,name')


def get_connection():
    dbname = 'evs'
    user = 'ubuntu'
    conn = psycopg2.connect(f"dbname='{dbname}' user='{user}'")
    return conn


def get_accounts():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM account;')
    rows = cursor.fetchall()

    cursor.close()
    conn.close()
    return [Account(*row) for row in rows]


def insert_balance(username, retrieve_date, amount):
    query = f"""INSERT INTO balance (username, retrieve_date, amount) 
                VALUES ('{username}', '{retrieve_date}', {amount});"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(query)
    conn.commit()

    cursor.close()
    conn.close()
