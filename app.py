from portfolio_creation import get_asset
from tools import post_data, get_data, put_data

# 9 rendement annualise
# 13 rendement
# 12 sharp
# 10 volatility
# 7 beta
if __name__ == '__main__':
    tmp = "{'ratio'=[10, 12, 13],'asset'=[1829],'start_date'='2013-06-14','end_date'='2019-04-18','frequency':null}"
    # r = tools.convert_to_EUR("USD", 2)
    # print(r)
    assets, weight = get_asset()
    print(assets)
    for i in range(len(weight)):
        weight[i] = round(weight[i]) * 1000
    put = "{'label':'EPITA_PTF_10','currency':{'code':'EUR'},'type':'front','values':{'2013-06-14':["
    for i in range(len(assets)):
        put += "{'asset':{'asset':" + assets[i][0] + ",'quantity':" + str(weight[i]) + "}}"
        if i != len(assets) - 1:
            put += ","
    put += "]}}"
    print(put)
    r = put_data('portfolio/1829/dyn_amount_compo', put)
    print(r)
    r = get_data("portfolio/1829/dyn_amount_compo")
    print(r)
    r = post_data('ratio/invoke', tmp)
    print(r)
