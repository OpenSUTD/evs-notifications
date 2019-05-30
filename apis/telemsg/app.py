from flask import Flask, request
from operator import itemgetter
from bot import send_message

app = Flask(__name__)
with open('admin.txt', 'r') as f:
    ADMIN_ID = int(f.read().strip())


@app.route('/message', methods=['POST'])
def message():
    body = request.get_json()
    chat_id, text = itemgetter('chat_id', 'text')(body)
    success = send_message(chat_id, text)
    return 'Success' if success else 'Fail'


@app.route('/message/admin', methods=['POST'])
def message_admin():
    body = request.get_json()
    chat_id, text = itemgetter('chat_id', 'text')(body)

    text = (f'Message from {chat_id}:\n'
            f'{text}')
    success = send_message(ADMIN_ID, text)
    return 'Success' if success else 'Fail'


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
