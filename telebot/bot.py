from telegram.ext import Updater
from handlers import commands as cmd
from handlers.conv import (add_subscription as add,
                           view_subscription as view)
import config

for obj in [cmd, add, view]:
    for name, value in config.network.items():
        setattr(obj, name, value)


class Bot(object):
    def __init__(self):
        with open('token.txt', 'r') as f:
            token = f.read().strip()
        self.updater = Updater(token=token, use_context=True)
        self.dispatcher = self.updater.dispatcher

    def add_handlers(self):
        for handler in cmd.handlers:
            self.dispatcher.add_handler(handler)
        self.dispatcher.add_handler(add.conv_handler)
        self.dispatcher.add_handler(view.conv_handler)

    def start(self):
        self.updater.start_polling()
        self.updater.idle()
