import requests
from config import URL, AUTH
import tools

def get_data(endpointApi, start_date=None, end_date=None, full_response=False,):
    payload = {'start_date': start_date, 'end_date': end_date, 'fullResponse': full_response}
    res = requests.get(URL + endpointApi, params=payload, auth=AUTH, verify=False)
    return res.content.decode('utf-8')


if __name__ == '__main__':
    r = get_data("asset/1792/quote")
    print(r)
    r = tools.convert_to_EUR("USD", 2)
    print(r)
