import json
from flask import Flask, request
from requests.exceptions import ConnectionError
from functools import wraps
from operator import itemgetter
from web import login_valid, get_amount, get_transactions, get_transactions_demo
from web.exceptions import LoginError

app = Flask(__name__)


def catch_errors(route_func):
    @wraps(route_func)
    def inner(*args, **kwargs):
        try:
            result = route_func(*args, **kwargs)
            return result
        except ConnectionError:
            return f'Could not access EVS web', 503
        except LoginError:
            username = request.get_json()['username']
            return f'Error on account login: {username}', 404
    return inner


@app.route('/validate', methods=['POST'])
@catch_errors
def validate():
    body = request.get_json()
    username, password = itemgetter('username', 'password')(body)
    return json.dumps({
        'valid': login_valid(username, password)
    })


@app.route('/credit', methods=['POST'])
@catch_errors
def credit():
    body = request.get_json()
    username, password = itemgetter('username', 'password')(body)
    amount = get_amount(username, password)
    return str(amount)


@app.route('/transaction', methods=['POST'])
@catch_errors
def transaction():
    body = request.get_json()
    username, password = itemgetter('username', 'password')(body)
    transactions = get_transactions(username, password)
    return json.dumps(transactions)


@app.route('/transaction/demo', methods=['POST'])
@catch_errors
def transaction_demo():
    body = request.get_json()
    username, password = itemgetter('username', 'password')(body)
    transactions = get_transactions_demo(username, password)
    return json.dumps(transactions)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
