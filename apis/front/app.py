import logging
import json
import requests
from flask import Flask, request
from flask_cors import CORS
from operator import itemgetter

DB_API_HOST = 'localhost'
DB_API_PORT = 8001

WEB_API_HOST = 'localhost'
WEB_API_PORT = 5000

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)


@app.route('/info', methods=['POST'])
def get_info():
    body = request.get_json()
    username, password = itemgetter('username', 'password')(body)
    logger.info(f'({username}, {password})')

    account_exists = validate_account(username, password)
    if not account_exists:
        return 'Account not found', 404

    info = get_info_dict(username, password)
    return json.dumps(info)


@app.route('/info/demo')
def get_demo_info():
    logger.info('Demo')

    with open('demo.json') as f:
        s = f.read()
    obj = json.loads(s)
    username, password = itemgetter('username', 'password')(obj)

    info = get_info_dict(username, password, demo=True)
    return json.dumps(info)


def get_info_dict(username: str, password: str, demo=False) -> dict:
    balances = get_balances(username, demo)
    transactions = get_transactions(username, password, demo)
    return {
        'balances': balances,
        'transactions': transactions,
    }


def get_balances(username: str, demo: bool) -> list:
    if demo:
        url = f'http://{DB_API_HOST}:{DB_API_PORT}/balance/username/demo/{username}'
    else:
        url = f'http://{DB_API_HOST}:{DB_API_PORT}/balance/username/{username}'
    r = requests.get(url)
    return json.loads(r.text)


def get_transactions(username: str, password: str, demo: bool) -> list:
    if demo:
        url = f'http://{WEB_API_HOST}:{WEB_API_PORT}/transaction/demo'
    else:
        url = f'http://{WEB_API_HOST}:{WEB_API_PORT}/transaction'
    headers = {'Content-Type': 'application/json'}
    data = json.dumps({'username': username, 'password': password})
    req = requests.post(url, headers=headers, data=data)
    transactions = json.loads(req.text)
    return transactions


def validate_account(username: str, password: str) -> bool:
    url = f'http://{DB_API_HOST}:{DB_API_PORT}/account'
    r = requests.get(url)
    accounts = json.loads(r.text)
    return [username, password] in accounts


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
