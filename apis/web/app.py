import json
from flask import Flask, request
from operator import itemgetter
from web import login_valid, get_amount

app = Flask(__name__)


@app.route('/validate', methods=['POST'])
def validate():
    body = request.get_json()
    username, password = itemgetter('username', 'password')(body)
    return json.dumps({
        'valid': login_valid(username, password)
    })


@app.route('/credit', methods=['POST'])
def credit():
    body = request.get_json()
    username, password = itemgetter('username', 'password')(body)
    return json.dumps({
        'amount': get_amount(username, password)
    })


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
