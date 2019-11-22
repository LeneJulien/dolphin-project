import requests
from tools import get_data
from tools import post_data
import json

def request_asset_list():
    r = get_data("asset?columns=ASSET_DATABASE_ID&columns=TYPE&columns=LABEL&columns=LAST_CLOSE_VALUE_IN_CURR",
                 start_date='2013-06-14', end_date='2019-04-18')
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

#date de debut 14/06/2013
#date de fin 31/05/2019
def asset_id_sort(assets):
    for data in assets:
        print(data['ASSET_DATABASE_ID']['value'])
        r = get_data("asset/" + data['ASSET_DATABASE_ID']['value'] + "?columns=CURRENCY")

def get_value_asset(assets):
    res = []
    for data in assets:
        tmp = "{'ratio'=[9, 12, 10, 13],'asset'=[" + data['ASSET_DATABASE_ID']['value'] + "],'start_date'='2013-06-14','end_date'='2019-04-18','frequency':null}"
        r = post_data('ratio/invoke', tmp)
        value_dic = json.loads(r)
        res.append(value_dic)
    print(res)
    return res

def get_asset():
    asset_dict = request_asset_list()
    stocks, funds, indexs = asset_sort(asset_dict)
    get_value_asset(stocks)
    get_value_asset(funds)
    get_value_asset(indexs)