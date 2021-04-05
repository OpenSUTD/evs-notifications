from telegram.ext import Updater
from .handlers import commands as cmd
from .handlers.conv import (add_subscription as add,
                            view_subscription as view,
                            feedback as feedback)


class Bot(object):
    def __init__(self, token: str):
        self.updater = Updater(token=token, use_context=True)
        self.dispatcher = self.updater.dispatcher

    def add_handlers(self):
        for handler in cmd.handlers:
            self.dispatcher.add_handler(handler)
        self.dispatcher.add_handler(add.conv_handler)
        self.dispatcher.add_handler(view.conv_handler)
        self.dispatcher.add_handler(feedback.conv_handler)

    def start(self):
        self.updater.start_polling()
        self.updater.idle()

    def send_message(self, chat_id: int, text: str):
        self.updater.bot.send_message(chat_id=chat_id, text=text)
