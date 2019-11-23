import requests
from config import URL, AUTH
from tools import post_data, get_data
import tools
from portfolio_creation import get_asset

# 9 rendement annualisé
# 13 rendement
# 12 sharp
# 10 volatility
if __name__ == '__main__':
    tmp = "{'ratio'=[9, 12, 10, 13],'asset'=[2201],'start_date'='2013-06-14','end_date'='2019-04-18','frequency':null}"
    r = post_data('ratio/invoke', tmp)
    # r = get_data("asset?columns=ASSET_DATABASE_ID&columns=TYPE&columns=LABEL")
    print(r)
    # r = tools.convert_to_EUR("USD", 2)
    # print(r)
    get_asset()
