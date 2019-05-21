from bot import Bot


if __name__ == '__main__':
    with open('token.txt', 'r') as f:
        token = f.read().strip()
    bot = Bot(token)
    bot.start()
