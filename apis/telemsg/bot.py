from telegram.ext import Updater
from telegram.error import BadRequest, Unauthorized

with open('token.txt', 'r') as f:
    token = f.read().strip()


def send_message(chat_id: int, text: str):
    updater = Updater(token=token)
    bot = updater.dispatcher.bot
    try:
        bot.send_message(chat_id=chat_id, text=text)
        return True
    except BadRequest:
        return False
    except Unauthorized:
        print(f'Unauthorized: {chat_id}')
        return False
