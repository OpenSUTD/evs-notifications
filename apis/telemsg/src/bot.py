import os
from telegram.ext import Updater
from telegram.error import BadRequest, Unauthorized

TOKEN = os.environ.get('TELEGRAM_TOKEN')
updater = Updater(token=TOKEN)
bot = updater.dispatcher.bot


def send_message(chat_id: int, text: str):
    try:
        bot.send_message(chat_id=chat_id, text=text)
        return True
    except BadRequest:
        return False
    except Unauthorized:
        print(f'Unauthorized: {chat_id}')
        return False
