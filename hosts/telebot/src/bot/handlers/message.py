import os
import re

import requests
from telegram.ext import Filters, MessageHandler

from ..config import TELEGRAM_ADMIN_ID, TELEMSG_API_HOST, TELEMSG_API_PORT
from .logging import logger


def admin_message_handler(update, context):
    if update.message.chat_id != TELEGRAM_ADMIN_ID:
        return
    if update.message.reply_to_message is None:
        return

    text = update.message.reply_to_message.text
    m = re.match(r'Message from (\d+):', text)
    if m is None:
        return
    target_user = int(m.group(1))
    text = f'Message from admin:\n{update.message.text}'
    message_user(target_user, text)


def message_user(chat_id: int, text: str) -> None:
    url = f'http://{TELEMSG_API_HOST}:{TELEMSG_API_PORT}/message'
    requests.post(url, json={
        'chat_id': chat_id,
        'text': text,
    })


message_handler = MessageHandler(Filters.text & ~Filters.command, admin_message_handler)
