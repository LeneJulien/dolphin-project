import json

import requests

from config import URL, AUTH


def get_data(endpointApi, start_date=None, end_date=None, full_response=False, columns=list()):
    payload = {'start_date': start_date, 'end_date': end_date, 'fullResponse': full_response}
    res = requests.get(URL + endpointApi, params=payload, auth=AUTH, verify=False)
    return res.content.decode('utf-8')


def post_data(endpointApi, data=None, start_date=None, end_date=None, full_response=False, columns=list()):
    payload = {'start_date': start_date, 'end_date': end_date, 'fullResponse': full_response}
    res = requests.post(URL + endpointApi, data, params=payload, auth=AUTH, verify=False)
    return res.content.decode('utf-8')


def put_data(endpointApi, data=None, start_date=None, end_date=None, full_response=False, columns=list()):
    payload = {'start_date': start_date, 'end_date': end_date, 'fullResponse': full_response}
    res = requests.put(URL + endpointApi, data, params=payload, auth=AUTH, verify=False)
    return res.content.decode('utf-8')


def convert_to_EUR(identifier, value, date=None, full_response=False):
    payload = {'date': date, 'fullResponse': full_response}
    res = requests.get(URL + 'currency/rate/' + identifier + '/to/EUR', params=payload, auth=AUTH, verify=False)
    r = json.loads(res.content.decode())
    return float(r['rate']['value'].replace(',', '.', 1)) * value
