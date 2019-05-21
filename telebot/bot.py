from telegram.ext import Updater
from telegram.error import BadRequest
from conv import (add_subscription as add,
                  view_subscription as view)


class Bot(object):
    def __init__(self):
        with open('token.txt', 'r') as f:
            token = f.read().strip()
        self.updater = Updater(token=token, use_context=True)
        self.dispatcher = self.updater.dispatcher

    def add_handlers(self):
        self.dispatcher.add_handler(add.conv_handler)
        self.dispatcher.add_handler(view.conv_handler)

    def start(self):
        self.updater.start_polling()
        self.updater.idle()

    def send_message(self, user_id:int, message:int):
        bot = self.updater.dispatcher.bot
        try:
            bot.send_message(chat_id=user_id, text=message)
        except BadRequest as e:
            print('telegram.error.BadRequest:', e.message, user_id)
