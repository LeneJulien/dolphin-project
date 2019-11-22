import requests
from tools import get_data
import json

def request_asset_list():
    r = get_data("asset?columns=ASSET_DATABASE_ID&columns=TYPE&columns=LABEL&coulmns=")
    print(r)
    dic_asset = json.loads(r)
    return dic_asset

def choose_(dic_asset):
    for data in dic_asset:
        