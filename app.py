import requests
from config import URL, AUTH
from tools import post_data, get_data, put_data
import tools
from portfolio_creation import get_asset

# 9 rendement annualise
# 13 rendement
# 12 sharp
# 10 volatility
if __name__ == '__main__':
    tmp = "{'ratio'=[9, 12, 10, 13],'asset'=[1829],'start_date'='2013-06-14','end_date'='2019-04-18','frequency':null}"
    put = "{'label':'EPITA_PTF_10','currency':{'code':'EUR'},'type':'front','values':{'2013-06-14':[{'asset':{'asset':2142,'quantity':1000.0}},{'asset':{'asset':2143,'quantity':2000.0}},{'asset':{'asset':2132,'quantity':5000.0}},{'asset':{'asset':2188,'quantity':90000.0}},{'asset':{'asset':2112,'quantity':7000.0}},{'asset':{'asset':1980,'quantity':7000.0}},{'asset':{'asset':2064,'quantity':7000.0}},{'asset':{'asset':2144,'quantity':7000.0}},{'asset':{'asset':2187,'quantity':7000.0}},{'asset':{'asset':1968,'quantity':7000.0}},{'asset':{'asset':2191,'quantity':7000.0}},{'asset':{'asset':2147,'quantity':7000.0}},{'asset':{'asset':1897,'quantity':7000.0}},{'asset':{'asset':1877,'quantity':7000.0}},{'asset':{'asset':2189,'quantity':7000.0}}]}}"
    #r = post_data('ratio/invoke', tmp)
    #r = put_data('portfolio/1829/dyn_amount_compo', put)
    #r = get_data("portfolio/1829/dyn_amount_compo")
    #print(r)
    # r = tools.convert_to_EUR("USD", 2)
    # print(r)
    #get_asset()
    tools.optimize()
    
