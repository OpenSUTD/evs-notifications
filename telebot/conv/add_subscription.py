import sys
sys.path.insert(0, '..')

import logging
from telegram.ext import CommandHandler, ConversationHandler, MessageHandler, Filters
from enum import Enum
from operator import itemgetter
import database as db
import web

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)


class States(Enum):
    USERNAME, PASSWORD, AMOUNT = range(3)


def validate_credentials(username, password):
    try:
        web.get_amount(username, password)
    except AssertionError:
        return False
    return True


def start(update, context):
    update.message.reply_text('Enter username to continue.')
    return States.USERNAME


def username(update, context):
    context.chat_data['username'] = update.message.text
    logger.info(f'Add subscription - username: {context.chat_data["username"]}')
    update.message.reply_text('Enter password.')
    return States.PASSWORD


def password(update, context):
    context.chat_data['password'] = update.message.text
    logger.info(f'Add subscription - password: {context.chat_data["password"]}')
    username, password = itemgetter('username', 'password')(context.chat_data)
    if validate_credentials(username, password):
        db.insert_account(username, password)
        logger.info(f'Add subscription - account added')
        update.message.reply_text('Enter amount.')
        return States.AMOUNT
    else:
        update.message.reply_text('Could not login. Enter password again.')
        return States.PASSWORD


def amount(update, context):
    amount = update.message.text
    try:
        amount = float(amount)
    except ValueError:
        update.message.reply_text('Could not convert amount to float. Please enter amount again.')
        return States.AMOUNT

    amount = round(amount, 2)
    username = context.chat_data['username']
    chat_id = update.message.chat.id

    add_successful = db.insert_subscription(username, amount, chat_id)
    if add_successful:
        logger.info(f'Add subscription - subscription added: ({username}, {amount}, {chat_id})')
        update.message.reply_text('Subscription added')
    else:
        update.message.reply_text('Subscription could not be added')
    return ConversationHandler.END


def cancel(update, context):
    update.message.reply_text('Ok bye')
    return ConversationHandler.END


conv_handler = ConversationHandler(
    entry_points=[CommandHandler('add', start)],
    states={
        States.USERNAME: [MessageHandler(Filters.text, username)],
        States.PASSWORD: [MessageHandler(Filters.text, password)],
        States.AMOUNT: [MessageHandler(Filters.text, amount)],
    },
    fallbacks=[CommandHandler('cancel', cancel)]
)
