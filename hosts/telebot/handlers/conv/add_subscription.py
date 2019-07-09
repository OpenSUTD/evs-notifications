import json
import requests
import logging
from telegram import ChatAction
from telegram.ext import CommandHandler, ConversationHandler, MessageHandler, Filters
from requests.exceptions import ConnectionError
from enum import Enum

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)


class States(Enum):
    USERNAME, PASSWORD, AMOUNT = range(3)


def start(update, context):
    update.message.reply_text('Create a new subscription to receive notifications '
                              'when your credit balance falls below a preset amount.\n\n'
                              'First, I will need your EVS login credentials. '
                              'Begin by entering your username. (20000xxx)')
    return States.USERNAME


def username(update, context):
    context.chat_data['username'] = update.message.text
    logger.info(f'({update.message.chat_id}) Add subscription - username: {context.chat_data["username"]}')
    update.message.reply_text('Now enter your password, and I will validate your credentials.\n\n'
                              'Type /cancel at any time to leave this conversation.')
    return States.PASSWORD


def password(update, context):
    chat_id = update.message.chat_id
    password = update.message.text
    context.chat_data['password'] = password
    logger.info(f'({chat_id}) Add subscription - password: {password}')

    context.bot.send_chat_action(chat_id=chat_id, action=ChatAction.TYPING)
    username = context.chat_data['username']
    try:
        valid = validate_credentials(username, password)
    except ConnectionError:
        update.message.reply_text('Sorry, but we have faced a connection error while validating your credentials. '
                                  'Please try again in a few minutes.')
        return ConversationHandler.END

    if valid:
        insert_account(username, password)
        logger.info(f'({chat_id}) Add subscription - account added')
        update.message.reply_text('Finally, enter the notification amount. '
                                  'You will receive a message when your credit balance falls below this amount.')
        return States.AMOUNT
    else:
        update.message.reply_text(f'Could not login. Enter your password for account {username}.\n\n'
                                  'Type /cancel at any time to leave this conversation.')
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

    add_successful = insert_subscription(username, amount, chat_id)
    if add_successful:
        logger.info(f'({update.message.chat_id}) Add subscription - '
                    f'subscription added: ({username}, {amount}, {chat_id})')
        update.message.reply_text(f'Your subscription has been successfully added: {username} - ${amount:.2f}\n\n'
                                  f'Use /view to view and delete your subscriptions.')
    else:
        logger.info(f'({update.message.chat_id}) Add subscription - '
                    f'subscription failed: ({username}, {amount}, {chat_id})')
        update.message.reply_text('Your subscription could not be added. Please try again later.')
    return ConversationHandler.END


def cancel(update, context):
    update.message.reply_text('Ok bye')
    return ConversationHandler.END


def validate_credentials(username, password):
    url = f'http://{WEB_API_HOST}:{WEB_API_PORT}/validate'
    headers = {'Content-Type': 'application/json'}
    data = json.dumps({'username': username, 'password': password})
    req = requests.post(url, headers=headers, data=data)
    response = json.loads(req.text)
    return response['valid']


def insert_account(username, password):
    url = f'http://{DB_API_HOST}:{DB_API_PORT}/account'
    headers = {'Content-Type': 'application/json'}
    data = json.dumps({'username': username, 'password': password})
    requests.post(url, headers=headers, data=data)


def insert_subscription(username, amount, chat_id):
    url = f'http://{DB_API_HOST}:{DB_API_PORT}/subscription'
    headers = {'Content-Type': 'application/json'}
    data = json.dumps({'username': username, 'amount': amount, 'chat_id': chat_id})
    req = requests.post(url, headers=headers, data=data)
    return req.text == 'Success'


conv_handler = ConversationHandler(
    entry_points=[CommandHandler('add', start)],
    states={
        States.USERNAME: [MessageHandler(Filters.text, username)],
        States.PASSWORD: [MessageHandler(Filters.text, password)],
        States.AMOUNT: [MessageHandler(Filters.text, amount)],
    },
    fallbacks=[CommandHandler('cancel', cancel)]
)
