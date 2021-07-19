import os
from bot import Bot

TOKEN = os.environ.get('TELEGRAM_TOKEN')



def main():
    bot = Bot(TOKEN)
    bot.add_handlers()
    bot.start()


if __name__ == '__main__':
    main()
