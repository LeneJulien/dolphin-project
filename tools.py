from config import URL, AUTH
import requests
import json
from scipy.optimize import minimize

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


def objectives(x):
	x1 = x[0] * 2.0
	x2 = x[1] * 1.4
	x3 = x[2] * 1.9
	x4 = x[3] * 1.8
	x5 = x[4] * 1.4
	x6 = x[5] * 1.4
	x7 = x[6] * 1.0
	x8 = x[7] * 1.47
	x9 = x[8] * 1.45
	x10 = x[9] * 1.9
	x11 = x[10]
	x12 = x[11]
	x13 = x[12]
	x14 = x[13]
	x15 = x[14]
	x16 = x[15]
	x17 = x[16]
	x18 = x[17]
	x19 = x[18]
	x20 = x[19]
	return (x1 + x2 + x3 + x4 + x5 + x6 + x7 + x8 + x9 + x10 + x11 + x12 + x13 + x14 + x15 + x16 + x17 + x18 + x19 + x20)* 1

def constraint(x):
	return x[0] + x[1] + x[2] + x[3] + x[4] + x[5] + x[6] + x[7] + x[8] + x[9] + x[10] + x[11] + x[12] + x[13] + x[14] + x[15] + x[16] + x[17] + x[18] + x[19] - 100

def optimize():
	x0 = [1, 1, 1, 1, 1, 1, 2, 2, 2, 3, 3, 3, 4, 4, 4, 5, 5, 5, 6, 6]
	print(len(x0))
	b = (1.0, 10.0)
	bnds = (b, b, b, b, b, b, b, b, b, b, b, b, b, b, b, b, b, b, b, b)
	cons = [{'type': 'ineq', 'fun': constraint}]
	solution = minimize(objectives, x0, method='SLSQP', bounds=bnds, constraints=cons)
	print(solution)
