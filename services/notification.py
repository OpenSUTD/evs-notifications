import json
import requests
from operator import attrgetter
from collections import namedtuple
from datetime import datetime

DB_API_HOST = 'localhost'
DB_API_PORT = 8001

TELE_API_HOST = 'localhost'
TELE_API_PORT = 5001


def main():
    notifications = get_notifications()
    for n in notifications:
        notify(n)


def get_notifications():
    Notification = namedtuple('Notification', 'username, amount, chat_id')

    url = f'http://{DB_API_HOST}:{DB_API_PORT}/notification'
    req = requests.get(url)
    rows = json.loads(req.text)
    notifications = [Notification(*row) for row in rows]
    return notifications


def notify(notification):
    chat_id = notification.chat_id
    username = notification.username
    text = make_text(notification)

    send_telegram_message(chat_id, text)
    insert_notification(username, chat_id)


def send_telegram_message(chat_id, text):
    url = f'http://{TELE_API_HOST}:{TELE_API_PORT}/message'
    headers = {'Content-Type': 'application/json'}
    data = json.dumps({'chat_id': chat_id, 'text': text})
    requests.post(url, headers=headers, data=data)


def insert_notification(username, chat_id):
    date = get_date()

    url = f'http://{DB_API_HOST}:{DB_API_PORT}/notification'
    headers = {'Content-Type': 'application/json'}
    data = json.dumps({'username': username, 'chat_id': chat_id, 'message_date': date})
    requests.post(url, headers=headers, data=data)


def get_date():
    now = datetime.now()
    return '{:04d}/{:02d}/{:02d}'.format(now.year, now.month, now.day)


def make_text(notification):
    username, amount = attrgetter('username', 'amount')(notification)
    return (f'Aircon notification for account {username}: '
            f'your remaining balance is ${amount:.2f}.')


if __name__ == '__main__':
    main()
