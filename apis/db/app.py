import json
from flask import Flask, request
from flask_cors import CORS
from operator import itemgetter
import psql as db

app = Flask(__name__)
CORS(app)


@app.route('/account', methods=['GET', 'POST'])
def account():
    if request.method == 'GET':
        accounts = db.get_accounts()
        return json.dumps(accounts)
    elif request.method == 'POST':
        body = request.get_json()
        username, password = itemgetter('username', 'password')(body)
        db.insert_account(username, password)
        return 'Success'


@app.route('/balance/username/<username>')
def get_balances_by_username(username):
    balances = db.get_balances_by_username(username)
    return json.dumps(balances)


@app.route('/balance/username/demo/<username>')
def get_demo_balances_by_username(username):
    balances = db.get_demo_balances_by_username(username)
    return json.dumps(balances)


@app.route('/balance/chatid/<chat_id>')
def get_latest_balances_by_chat_id(chat_id):
    balances = db.get_latest_balances_by_chat_id(chat_id)
    return json.dumps(balances)


@app.route('/balance', methods=['POST'])
def insert_balance():
    body = request.get_json()
    username, retrieve_date, amount = itemgetter('username', 'retrieve_date', 'amount')(body)
    db.insert_balance(username, retrieve_date, amount)
    return 'Success'


@app.route('/subscription/<chat_id>')
def get_subscriptions_by_chat_id(chat_id):
    subscriptions = db.get_subscriptions_by_chat_id(chat_id)
    return json.dumps(subscriptions)


@app.route('/subscription', methods=['POST'])
def insert_subscription():
    body = request.get_json()
    username, amount, chat_id = itemgetter('username', 'amount', 'chat_id')(body)
    db.insert_subscription(username, amount, chat_id)
    return 'Success'


@app.route('/subscription/<subscription_id>', methods=['DELETE'])
def delete_subscription_by_id(subscription_id):
    db.delete_subscription_by_id(subscription_id)
    return 'Success'


@app.route('/notification', methods=['GET'])
def get_notifications():
    notifications = db.get_notifications()
    return json.dumps(notifications)


@app.route('/notification', methods=['POST'])
def insert_notification():
    body = request.get_json()
    username, chat_id, message_date = itemgetter('username', 'chat_id', 'message_date')(body)
    db.insert_notification(username, chat_id, message_date)
    return 'Success'


@app.route('/command', methods=['POST'])
def insert_command():
    body = request.get_json()
    name, chat_id, is_completed = itemgetter('name', 'chat_id', 'is_completed')(body)
    db.insert_command(name, chat_id, is_completed)
    return 'Success'


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8001)
