import re
import requests

login_url = 'https://nus-utown.evs.com.sg/SUTDMain/loginServlet'
credit_url = 'https://nus-utown.evs.com.sg/SUTDMain/viewMeterCreditServlet'


def get_request_params(username: str, password: str):
    data = {
        'txtLoginId': username,
        'txtPassword': password,
        'btnLogin': 'Login',
    }
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    return data, headers


def login_valid(username: str, password: str) -> bool:
    sess = requests.session()
    data, headers = get_request_params(username, password)
    r = sess.post(url=login_url, data=data, headers=headers)
    # if invalid, r.url will be
    # https://nus-utown.evs.com.sg/SUTD/index.jsp?
    # strMsg=Invalid%20Login%20ID%20or%20Password.
    return 'Invalid' not in r.url


def get_amount(username, password):
    sess = requests.session()
    data, headers = get_request_params(username, password)

    r = sess.post(url=login_url, data=data, headers=headers)
    assert r.status_code == 200, 'Could not login'

    r = sess.get(credit_url)
    assert r.status_code == 200, 'Could not retrieve credit page'

    pattern = r'S\$ (\d{1,2}\.\d{2})'  # S$ (d.dd) OR S$ (dd.dd)
    matches = re.findall(pattern, r.text)
    assert len(matches) > 1, 'Could not find balance on page'

    return float(matches[1])
