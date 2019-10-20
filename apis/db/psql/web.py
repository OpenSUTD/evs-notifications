import json
import requests

WEB_API_HOST = 'localhost'
WEB_API_PORT = 5000


def get_amount(username: str, password: str) -> float:
    url = f'http://{WEB_API_HOST}:{WEB_API_PORT}/credit'
    headers = {'Content-Type': 'application/json'}
    data = json.dumps({'username': username, 'password': password})
    req = requests.post(url, headers=headers, data=data)
    if req.ok:
        return float(req.text)
    else:
        return -1
