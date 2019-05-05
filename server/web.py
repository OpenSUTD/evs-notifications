import re
import requests

login_url = 'https://nus-utown.evs.com.sg/SUTDMain/loginServlet'
credit_url = 'https://nus-utown.evs.com.sg/SUTDMain/viewMeterCreditServlet'


def get_credit(username, password):
    sess = requests.session()

    login_data = {
        'txtLoginId': username,
        'txtPassword': password,
        'btnLogin': 'Login'
    }
    headers= {'Content-Type': 'application/x-www-form-urlencoded'}
    r = sess.post(url=login_url, data=login_data, headers=headers)
    assert r.status_code == 200, 'Could not login'
    assert 'Invalid' not in r.url, 'Wrong password'

    r = sess.get(credit_url)
    assert r.status_code == 200, 'Could not retrieve credit page'

    pattern = r'S\$ \d{1,2}\.\d{2}'  # S$ d.dd OR S$ dd.dd
    matches = re.findall(pattern, r.text)

    if len(matches) > 1:
        return matches[1]
    return -1

