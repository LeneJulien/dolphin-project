from config import URL, AUTH
import requests
import json

def convert_to_EUR(identifier, value, date=None, full_response=False):
    payload = {'date': date, 'fullResponse': full_response}
    res = requests.get(URL + 'currency/rate/' + identifier + '/to/EUR', params=payload, auth=AUTH, verify=False)
    r = json.loads(res.content.decode())
    return float(r['rate']['value'].replace(',', '.', 1)) * value
