import json
from flask import Flask, request
from requests.exceptions import ConnectionError
from operator import itemgetter
from web import login_valid, get_amount, get_transactions

app = Flask(__name__)


@app.route('/validate', methods=['POST'])
def validate():
    try:
        body = request.get_json()
        username, password = itemgetter('username', 'password')(body)
        return json.dumps({
            'valid': login_valid(username, password)
        })
    except ConnectionError:
        return f'Could not access EVS web', 503


@app.route('/credit', methods=['POST'])
def credit():
    body = request.get_json()
    username, password = itemgetter('username', 'password')(body)

    try:
        amount = get_amount(username, password)
    except AssertionError:  # TODO - raise proper exception
        return f'Error on account: {username}', 404
    except ConnectionError:
        return f'Could not access EVS web', 503

    return str(amount)


@app.route('/transaction', methods=['POST'])
def transaction():
    body = request.get_json()
    username, password = itemgetter('username', 'password')(body)

    try:
        transactions = get_transactions(username, password)
    except AssertionError:  # TODO - raise proper exception
        return f'Error on account: {username}', 404
    except ConnectionError:
        return f'Could not access EVS web', 503

    return json.dumps(transactions)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
