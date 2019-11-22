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
        print(data)
        if data['TYPE']['value'] == 'STOCK':
            stocks.append(data)
        elif data['TYPE']['value'] == 'FUND':
            funds.append(data)
        elif data['TYPE']['value'] == 'INDEX':
            indexs.append(data)
    return stocks, funds, indexs

def asset_id_sort(assets):
    for data in assets:
        r = get_data()

def get_asset():
    asset_dict = request_asset_list()
    asset_sort(asset_dict)