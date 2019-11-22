import requests
from tools import get_data
import json

def request_asset_list():
    r = get_data("asset?columns=ASSET_DATABASE_ID&columns=TYPE&columns=LABEL&coulmns=")
    dic_asset = json.loads(r)
    return dic_asset

def asset_sort(dic_asset):
    stocks = []
    funds = []
    indexs = []
    for data in dic_asset:
        if data['TYPE']['value'] == 'STOCK':
            stocks.append(data)
        elif data['TYPE']['value'] == 'FUND':
            funds.append(data)
        elif data['TYPE']['value'] == 'INDEX':
            indexs.append(data)
    return stocks, funds, indexs

#date de debut 14/06/2013
#date de fin 31/05/2019
def asset_id_sort(assets):
    for data in assets:
        print(data['ASSET_DATABASE_ID']['value'])
        r = get_data("asset/" + data['ASSET_DATABASE_ID']['value'] + "?columns=CURRENCY", start_date='2013-06-14', end_date='2019-04-18')


def get_asset():
    asset_dict = request_asset_list()
    stocks, funds, indexs = asset_sort(asset_dict)
    asset_id_sort(stocks)
