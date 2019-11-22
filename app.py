import requests
from config import URL, AUTH
import tools
from portfolio_creation import get_asset


if __name__ == '__main__':
    #r = get_data("asset", "2013-04-26", "2014-04-26")
    #r = get_data("asset?columns=ASSET_DATABASE_ID&columns=TYPE&columns=LABEL")
    #print(r)
    #r = tools.convert_to_EUR("USD", 2)
    #print(r)
    get_asset()
