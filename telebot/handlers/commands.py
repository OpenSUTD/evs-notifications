import json
import requests
import logging
from collections import namedtuple
from telegram.ext import CommandHandler

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
    user_balances = get_latest_balances_by_chat_id(chat_id)
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


def get_latest_balances_by_chat_id(chat_id):
    UserBalance = namedtuple('UserBalance', 'username, amount')

    url = f'http://{DB_API_HOST}:{DB_API_PORT}/balance/chatid/{chat_id}'
    req = requests.get(url)
    rows = json.loads(req.text)
    return [UserBalance(*row) for row in rows]


handlers = [
    CommandHandler('start', start),
    CommandHandler('balance', balance),
    CommandHandler('security', security),
]
