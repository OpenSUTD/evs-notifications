import json
import requests
import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CommandHandler, ConversationHandler, CallbackQueryHandler
from enum import Enum
from collections import namedtuple

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)


class States(Enum):
    CALLBACK = range(1)


def get_reply_markup(chat_id):
    def button(subscription):
        text = f'{subscription.username} - ${subscription.amount:.2f}'
        callback_data = subscription.id
        return InlineKeyboardButton(text, callback_data=callback_data)
    cancel_button = InlineKeyboardButton('Cancel', callback_data='cancel')

    subscriptions = get_subscriptions_by_chat_id(chat_id)
    keyboard = [[button(subscription)] for subscription in subscriptions]
    keyboard.append([cancel_button])
    return InlineKeyboardMarkup(keyboard)


def start(update, context):
    chat_id = update.message.chat.id
    reply_markup = get_reply_markup(chat_id)
    text = ('Here are a list of your subscriptions. ' 
            'To remove subscriptions, click on their corresponding button.\n\n' 
            'Alternatively, press cancel to exit.')
    update.message.reply_text(text, reply_markup=reply_markup)
    return States.CALLBACK


def callback(update, context):
    query = update.callback_query
    chat_id = query.message.chat.id
    data = query.data
    if data == 'cancel':
        logger.info(f'({chat_id}) View subscription - cancel')
        query.edit_message_text('Ok bye')
        return ConversationHandler.END

    delete_subscription_by_id(data)
    logger.info(f'({chat_id}) Delete subscription - ID: {data}')
    reply_markup = get_reply_markup(chat_id)
    text = ('Your subscription has been successfully removed.\n\n'
            "Press 'Cancel' to exit, or continue removing available subscriptions.")
    query.edit_message_text(text, reply_markup=reply_markup)
    return States.CALLBACK


def cancel(update, context):
    update.message.reply_text('Ok bye')
    return ConversationHandler.END


def get_subscriptions_by_chat_id(chat_id):
    url = f'http://{DB_API_HOST}:{DB_API_PORT}/subscription/{chat_id}'
    req = requests.get(url)
    rows = json.loads(req.text)
    Subscription = namedtuple('Subscription', 'id, username, amount, chat_id')
    return [Subscription(*row) for row in rows]


def delete_subscription_by_id(subscription_id):
    url = f'http://{DB_API_HOST}:{DB_API_PORT}/subscription/{subscription_id}'
    requests.delete(url)


conv_handler = ConversationHandler(
    entry_points=[CommandHandler('view', start)],
    states={
        States.CALLBACK: [CallbackQueryHandler(callback)]
    },
    fallbacks=[CommandHandler('cancel', cancel)]
)
