import json
from flask import Flask
from flask_cors import CORS
import psql

app = Flask(__name__)
CORS(app)


@app.route('/balance/<username>')
def get_balances(username):
    balances = psql.get_balances_by_username(username)
    return json.dumps(balances)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)

