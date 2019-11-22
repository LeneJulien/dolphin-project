import requests
from config import URL, AUTH
from tools import post_data
import tools
from portfolio_creation import get_asset


if __name__ == '__main__':
	tmp = "{'ratio'=[9, 12, 18],'asset'=[2201],'bench'=null,'startDate'='2013-06-14','endDate'='2019-05-31','frequency':null}"
	r = post_data('ratio/invoke', tmp)
	#r = get_data("asset?columns=ASSET_DATABASE_ID&columns=TYPE&columns=LABEL")
	print(r)
	#r = tools.convert_to_EUR("USD", 2)
	#print(r)
	#get_asset()
