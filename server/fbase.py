import json
from firebase import firebase

with open('config/fbase.json', 'r') as f:
    fbase_config = json.loads(f.read())
url = fbase_config['url']
secret = fbase_config['secret']
email = fbase_config['email']
auth = firebase.FirebaseAuthentication(secret, email, admin=True)
firebase = firebase.FirebaseApplication(url, auth)


def fetch_all_balances(user):
    balances_by_year = firebase.get('/daily_aircon', user)
    all_balances = []
    for year, yearly_balances in balances_by_year.items():
        for month, monthly_balances in yearly_balances.items():
            print(monthly_balances)
            for day, balance_amt in monthly_balances.items():
                balance_date = f'{year}/{month}/{day}'
                all_balances.append((balance_date, balance_amt))
    return all_balances

