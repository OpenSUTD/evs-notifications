from bot import Bot


def main():
    with open('token.txt', 'r') as f:
        token = f.read().strip()
    bot = Bot(token)

    chat_id = int(input('Enter chat ID: '))
    text = input('Enter message: ')
    bot.send_message(chat_id, text)


if __name__ == '__main__':
    main()
