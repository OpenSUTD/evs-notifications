from flask import Flask, request
from operator import itemgetter
from bot import send_message

app = Flask(__name__)


@app.route('/message', methods=['POST'])
def message():
    body = request.get_json()
    user_id, text = itemgetter('user_id', 'text')(body)
    success = send_message(user_id, text)
    return 'Success' if success else 'Fail'


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
