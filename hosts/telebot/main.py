from bot import Bot


def main():
    with open('token.txt', 'r') as f:
        token = f.read().strip()
    bot = Bot(token)
    bot.add_handlers()
    bot.start()


if __name__ == '__main__':
    main()
