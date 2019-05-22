import sys
sys.path.insert(0, '..')

import logging
from telegram.ext import CommandHandler
import database as db

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)


def start(update, context):
    logger.info(f'({update.message.chat_id}) Command - start')
    text = ('Hi! Receive notifications when your EVS credit balance '
            'falls below a specified threshold.\n\n'
            'To begin, use the /add command to create a subscription.\n\n'
            'Once you have subscriptions set up, you can use /balance to '
            'quickly check your balance here as well.')
    context.bot.send_message(chat_id=update.message.chat_id, text=text)


def balance(update, context):
    logger.info(f'({update.message.chat_id}) Command - balance')
    chat_id = update.message.chat_id
    user_balances = db.get_latest_balances_by_chat_id(chat_id)
    if len(user_balances) == 0:
        text = ('No entries found. '
                'Either you do not have an existing subscription, '
                'or your credit balances have not been retrieved yet.')
        context.bot.send_message(chat_id=chat_id, text=text)
    else:
        text = '\n'.join(f'• {balance.username} - ${balance.amount:.2f}'
                         for balance in user_balances)
        context.bot.send_message(chat_id=chat_id, text=text)


def security(update, context):
    logger.info(f'({update.message.chat_id}) Command - security')
    text = ('Your credentials are being stored in plaintext. '
            'Please do not use this bot if it makes you uncomfortable.')
    context.bot.send_message(chat_id=update.message.chat_id, text=text)


handlers = [
    CommandHandler('start', start),
    CommandHandler('balance', balance),
    CommandHandler('security', security),
]
