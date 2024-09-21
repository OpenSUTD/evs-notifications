import json
import requests
from telegram.ext import ConversationHandler, CommandHandler, MessageHandler, Filters
from enum import Enum

from ...config import TELEMSG_API_HOST, TELEMSG_API_PORT
from ..logging import logger, log_command_in_db

COMMAND_NAME = 'feedback'


class States(Enum):
    FEEDBACK, CANCEL = range(2)


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
    if text == '/cancel':
        return cancel(update, context)

    message_successful = message_admin(chat_id, text)
    if message_successful:
        log_command_in_db(COMMAND_NAME, update.message.chat_id, is_completed=True, is_cancelled=False)
        update.message.reply_text('Your message has been successfully received. Thank you!')
    else:
        log_command_in_db(COMMAND_NAME, update.message.chat_id, is_completed=False, is_cancelled=False)
        update.message.reply_text('I am sorry, but your message could not be received.'
                                  'Please try again later.')
    return ConversationHandler.END


def cancel(update, context):
    log_command_in_db(COMMAND_NAME, update.message.chat_id, is_completed=False, is_cancelled=True)
    update.message.reply_text('Ok bye')
    return ConversationHandler.END


def message_admin(chat_id, text):
    url = f'http://{TELEMSG_API_HOST}:{TELEMSG_API_PORT}/message/admin'
    headers = {'Content-Type': 'application/json'}
    data = json.dumps({'chat_id': chat_id, 'text': text})
    req = requests.post(url, headers=headers, data=data)
    return req.text == 'Success'


conv_handler = ConversationHandler(
    entry_points=[CommandHandler('feedback', start)],
    states={
        States.FEEDBACK: [MessageHandler(Filters.text, feedback)],
        States.CANCEL: [MessageHandler(Filters.text, cancel)],
    },
    fallbacks=[CommandHandler('cancel', cancel)]
)
