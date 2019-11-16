import requests
from config import URL, AUTH
import tools

def get_data(endpointApi, date=None, full_response=False):
    payload = {'date': date, 'fullResponse': full_response}
    res = requests.get(URL + endpointApi, params=payload, auth=AUTH, verify=False)
    return res.content.decode('utf-8')

if __name__ == '__main__':
    r = tools.convert_to_EUR("USD", 2)
    print(r)