import sys
sys.path.insert(0, '..')

from operator import attrgetter
import database as db
from bot import Bot


def make_text(notification):
    username, amount = attrgetter('username', 'amount')(notification)
    return (f'Aircon notification for account {username}: '
            f'your remaining balance is ${amount:.2f}.')


def notify(bot, notification):
    text = make_text(notification)
    bot.send_message(user_id=notification.chat_id, message=text)


if __name__ == '__main__':
    bot = Bot()
    notifications = db.get_notifications()
    for n in notifications:
        notify(bot, n)
