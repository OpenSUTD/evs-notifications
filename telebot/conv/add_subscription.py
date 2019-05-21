import sys
sys.path.insert(0, '..')

from telegram.ext import CommandHandler, ConversationHandler, MessageHandler, Filters
from enum import Enum
import database as db
import web


class States(Enum):
    USERNAME, PASSWORD, AMOUNT = range(3)


def validate_credentials(username, password):
    try:
        web.get_amount(username, password)
    except AssertionError:
        return False
    return True


def start(bot, update):
    update.message.reply_text('Enter username to continue.')
    return States.USERNAME


def username(bot, update, chat_data):
    chat_data['username'] = update.message.text
    update.message.reply_text('Enter password.')
    return States.PASSWORD


def password(bot, update, chat_data):
    chat_data['password'] = update.message.text
    username, password = chat_data['username'], chat_data['password']
    if validate_credentials(username, password):
        db.add_account(username, password)
        update.message.reply_text('Enter amount.')
        return States.AMOUNT
    else:
        update.message.reply_text('Could not login. Enter password again.')
        return States.PASSWORD


def amount(bot, update, chat_data):
    amount = update.message.text
    try:
        amount = float(amount)
    except ValueError:
        update.message.reply_text('Could not convert amount to float. Please enter amount again.')
        return States.AMOUNT

    amount = round(amount, 2)
    username = chat_data['username']
    chat_id = update.message.chat.id

    add_successful = db.add_subscription(username, amount, chat_id)
    if add_successful:
        update.message.reply_text('Subscription added')
    else:
        update.message.reply_text('Subscription could not be added')
    return ConversationHandler.END


def cancel(bot, update):
    update.message.reply_text('Ok bye')
    return ConversationHandler.END


conv_handler = ConversationHandler(
    entry_points=[CommandHandler('add', start)],
    states={
        States.USERNAME: [MessageHandler(Filters.text, username, pass_chat_data=True)],
        States.PASSWORD: [MessageHandler(Filters.text, password, pass_chat_data=True)],
        States.AMOUNT: [MessageHandler(Filters.text, amount, pass_chat_data=True)],
    },
    fallbacks=[CommandHandler('cancel', cancel)]
)
