import requests

URL = 'https://dolphin.jump-technology.com:8443/api/v1/'
AUTH = ('EPITA_GROUPE10', 'Fy4PsEGnT2B3VnxM')

def get_data(endpointApi, date=None, full_response=False):
    payload = {'date': date, 'fullResponse': full_response}
    res = requests.get(URL + endpointApi, params=payload, auth=AUTH, verify=False)
    return res.content.decode('utf-8')

if __name__ == '__main__':
    r = get_data("asset/1792")
    print(r)