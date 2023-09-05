import requests
from .utils import login_url, get_request_params


def login_valid(username: str, password: str) -> bool:
    with requests.session() as sess:
        data, headers = get_request_params(username, password)
        r = sess.post(url=login_url, data=data, headers=headers, verify=False)
        # if invalid, r.url will be
        # https://nus-utown.evs.com.sg/SUTD/index.jsp?
        # strMsg=Invalid%20Login%20ID%20or%20Password.
        is_valid = 'Invalid' not in r.url
    return is_valid
