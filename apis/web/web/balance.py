import re
import requests
from .utils import login_url, credit_url, get_request_params


def get_amount(username, password):
    with requests.session() as sess:
        data, headers = get_request_params(username, password)

        # store login cookies in session
        r = sess.post(url=login_url, data=data, headers=headers)
        assert 'Invalid' not in r.url, 'Wrong login credentials'

        r = sess.get(credit_url)
        amount = get_balance_from_text(r.text)
    return amount


def get_balance_from_text(text):
    pattern = r'S\$ ((\d{1,3},)*\d{1,3}\.\d{2})'  # S$ (ddd,)*ddd.dd
    matches = re.findall(pattern, text)
    assert len(matches) > 1, 'Could not find balance on page'

    match = matches[1][0].replace(',', '')
    return float(match)
