from typing import Tuple

base_url = 'https://nus-utown.evs.com.sg/SUTDMain'
login_url = f'{base_url}/loginServlet'
credit_url = f'{base_url}/viewMeterCreditServlet'
transaction_url = f'{base_url}/listTransactionServlet'


def get_request_params(username: str, password: str) -> Tuple[dict, dict]:
    if type(username) != str:
        raise TypeError("Username must be type 'string'")
    if type(password) != str:
        raise TypeError("Password must be type 'string'")
    data = {
        'txtLoginId': username,
        'txtPassword': password,
        'btnLogin': 'Login',
    }
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    return data, headers
