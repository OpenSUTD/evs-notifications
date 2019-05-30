import json
import requests
from operator import attrgetter
from collections import namedtuple

DB_API_HOST = 'localhost'
DB_API_PORT = 8001

TELE_API_HOST = 'localhost'
TELE_API_PORT = 5001


def make_text(notification):
    username, amount = attrgetter('username', 'amount')(notification)
    return (f'Aircon notification for account {username}: '
            f'your remaining balance is ${amount:.2f}.')


def notify(notification):
    user_id = notification.chat_id
    text = make_text(notification)

    url = f'http://{TELE_API_HOST}:{TELE_API_PORT}/message'
    headers = {'Content-Type': 'application/json'}
    data = json.dumps({'user_id': user_id, 'text': text})
    requests.post(url, headers=headers, data=data)


def get_notifications():
    Notification = namedtuple('Notification', 'username, amount, chat_id')

    url = f'http://{DB_API_HOST}:{DB_API_PORT}/notification'
    req = requests.get(url)
    rows = json.loads(req.text)
    notifications = [Notification(*row) for row in rows]
    return notifications


def main():
    notifications = get_notifications()
    for n in notifications:
        notify(n)


if __name__ == '__main__':
    main()
