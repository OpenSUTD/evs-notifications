import json
import requests
import logging
from telegram.ext import ConversationHandler, CommandHandler, MessageHandler, Filters
from enum import Enum

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)


class States(Enum):
    FEEDBACK = range(1)


def start(update, context):
    update.message.reply_text('Hi! Feel free to leave a message here. '
                              'Feedback or bug reports are always welcome. '
                              'Anything you type next will be forwarded to the admin.\n\n'
                              'Type /cancel to cancel.')
    return States.FEEDBACK


def feedback(update, context):
    chat_id = update.message.chat_id
    text = update.message.text

    logger.info(f'({chat_id}) Feedback: {text}')
    message_successful = message_admin(chat_id, text)
    if message_successful:
        update.message.reply_text('Your message has been successfully received. Thank you!')
    else:
        update.message.reply_text('I am sorry, but your message could not be received.'
                                  'Please try again later.')
    return ConversationHandler.END


def cancel(update, context):
    update.message.reply_text('Ok bye')
    return ConversationHandler.END


def message_admin(chat_id, text):
    url = f'http://{TELE_API_HOST}:{TELE_API_PORT}/message/admin'
    headers = {'Content-Type': 'application/json'}
    data = json.dumps({'chat_id': chat_id, 'text': text})
    req = requests.post(url, headers=headers, data=data)
    return req.text == 'Success'


conv_handler = ConversationHandler(
    entry_points=[CommandHandler('feedback', start)],
    states={
        States.FEEDBACK: [MessageHandler(Filters.text, feedback)],
    },
    fallbacks=[CommandHandler('cancel', cancel)]
)
