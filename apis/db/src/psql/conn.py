import os
import psycopg2
from typing import Tuple

DB_HOST = os.environ.get('DB_HOST', '127.0.0.1')
DB_PORT = os.environ.get('DB_PORT', 5432)


def get_connection():
    conn = psycopg2.connect(dbname='evs',
                            user='postgres',
                            password='docker',
                            host=DB_HOST,
                            port=DB_PORT)
    return conn
