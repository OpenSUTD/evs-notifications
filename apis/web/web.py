import re
import requests

base_url = 'https://nus-utown.evs.com.sg/SUTDMain'
login_url = f'{base_url}/loginServlet'
credit_url = f'{base_url}/viewMeterCreditServlet'


def get_request_params(username: str, password: str):
    if type(username) != str:
        raise TypeError('Username must be type "string"')
    if type(password) != str:
        raise TypeError('Password must be type "string"')
    data = {
        'txtLoginId': username,
        'txtPassword': password,
        'btnLogin': 'Login',
    }
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    return data, headers


def login_valid(username: str, password: str) -> bool:
    with requests.session() as sess:
        data, headers = get_request_params(username, password)
        r = sess.post(url=login_url, data=data, headers=headers)
        # if invalid, r.url will be
        # https://nus-utown.evs.com.sg/SUTD/index.jsp?
        # strMsg=Invalid%20Login%20ID%20or%20Password.
        is_valid = 'Invalid' not in r.url
    return is_valid


def get_balance_from_text(text):
    pattern = r'S\$ ((\d{1,3},)*\d{1,3}\.\d{2})'  # S$ (ddd,)*ddd.dd
    matches = re.findall(pattern, text)
    assert len(matches) > 1, 'Could not find balance on page'

    match = matches[1][0].replace(',', '')
    return float(match)


def get_amount(username, password):
    with requests.session() as sess:
        data, headers = get_request_params(username, password)

        r = sess.post(url=login_url, data=data, headers=headers)
        assert r.status_code == 200, 'Could not login'

        r = sess.get(credit_url)
        assert r.status_code == 200, 'Could not retrieve credit page'

        amount = get_balance_from_text(r.text)
    return amount

