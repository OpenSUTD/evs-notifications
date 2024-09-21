import json
import requests
from collections import namedtuple
from telegram.ext import CommandHandler

from ..config import DB_API_HOST, DB_API_PORT
from .logging import logger, log_command_in_db

handlers = []


def register_command_handler(command: str):
    def inner(callback):
        handlers.append(CommandHandler(command, callback))
        return callback
    return inner


@register_command_handler('start')
def start(update, context):
    log_command('start', update.message.chat_id)

    text = ('Hi! Receive notifications when your EVS credit balance '
            'falls below a specified threshold.\n\n'
            'To begin, use the /add command to create a subscription.\n\n'
            'Once you have subscriptions set up, you can use /balance to '
            'quickly check your balance here as well.')
    context.bot.send_message(chat_id=update.message.chat_id, text=text)


@register_command_handler('about')
def start(update, context):
    log_command('about', update.message.chat_id)
    text = (
        'This bot works by simply logging into your account on your behalf '
        'and checking the balance from there. If there are issues with your '
        'account or balance, please check with the EVS vendor instead.\n\n'
        'For more information, feel free to check out the project source '
        'code here: https://github.com/OpenSUTD/evs-notifications.'
    )
    context.bot.send_message(chat_id=update.message.chat_id, text=text)


@register_command_handler('balance')
def balance(update, context):
    chat_id = update.message.chat_id
    log_command('balance', update.message.chat_id)

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


@register_command_handler('dashboard')
def dashboard(update, context):
    log_command('dashboard', update.message.chat_id)
    text = ('View some dashboard analytics for your aircon usage: '
            'https://opensutd.org/evs-notifications')
    context.bot.send_message(chat_id=update.message.chat_id, text=text)


@register_command_handler('security')
def security(update, context):
    log_command('security', update.message.chat_id)
    text = ('Your credentials are being stored in plaintext. '
            'Please do not use this bot if it makes you uncomfortable.')
    context.bot.send_message(chat_id=update.message.chat_id, text=text)


def get_latest_balances_by_chat_id(chat_id):
    UserBalance = namedtuple('UserBalance', 'username, amount')

    url = f'http://{DB_API_HOST}:{DB_API_PORT}/balance/chatid/{chat_id}'
    req = requests.get(url)
    rows = json.loads(req.text)
    return [UserBalance(*row) for row in rows]


def log_command(name: str, chat_id: int):
    logger.info(f'({chat_id}) Command - {name}')
    log_command_in_db(name, chat_id, is_completed=True, is_cancelled=False)
