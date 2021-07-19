import os
from bot import Bot

TOKEN = os.environ.get('TELEGRAM_TOKEN')


def main():
    bot = Bot(TOKEN)

    chat_id = int(input('Enter chat ID: '))
    text = input('Enter message: ')
    bot.send_message(chat_id, text)


if __name__ == '__main__':
    main()
