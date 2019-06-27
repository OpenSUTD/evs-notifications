import requests
from flask import Flask, request
from flask_cors import CORS

HOST = 'http://13.251.125.232:8000'
app = Flask(__name__)
CORS(app)


@app.route('/info', methods=['POST'])
def get_balances():
    headers = {'Content-Type': 'application/json'}
    data = request.data

    url = f'{HOST}/info'
    r = requests.post(url, headers=headers, data=data)
    return r.text, r.status_code


@app.route('/info/demo')
def get_demo_balances():
    url = f'{HOST}/info/demo'
    r = requests.get(url)
    return r.text


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
