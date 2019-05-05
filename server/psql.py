import psycopg2
from collections import namedtuple

Account = namedtuple('Account', 'username,password,name')


def fetch_accounts():
    try:
        dbname = 'evs'
        user = 'ubuntu'
        conn = psycopg2.connect(f"dbname='{dbname}' user='{user}'")
    except:
        print('DB connection error')

    cur = conn.cursor()
    cur.execute('SELECT * FROM account')
    rows = cur.fetchall()
    return [Account(*row) for row in rows]

