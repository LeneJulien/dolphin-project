from portfolio_creation import get_asset
from tools import post_data, get_data, put_data, convert_to_EUR

def nav_constraint(weight, assets):
    nav_total = 0
    val_in_eur = []
    for i in range(len(weight)):
        weight[i] = round(weight[i])*1000
        splited = assets[i][4].split(" ")
        val = convert_to_EUR(splited[1], float(splited[0].replace(',', '.')))
        nav_total += val * weight[i]
        val_in_eur.append(val * weight[i])
    for i in range(len(weight)):
        current = val_in_eur[i] * 100 / nav_total
        if(current < 2 or current > 10):
            new = round(weight[i] * 4.5 / current)
            weight[i] = new
    nav_total = 0
    val_in_eur = []
    for i in range(len(weight)):
        splited = assets[i][4].split(" ")
        val = convert_to_EUR(splited[1], float(splited[0].replace(',', '.')))
        nav_total += val * weight[i]
        val_in_eur.append(val * weight[i])
    for i in range(len(weight)):
        current = val_in_eur[i] * 100 / nav_total
        print(str(i) + " : " + str(current) + "%")
    return weight

# 9 rendement annualise
# 13 rendement
# 12 sharp
# 10 volatility
# 7 beta
if __name__ == '__main__':
    tmp = "{'ratio'=[10, 12, 13],'asset'=[1829],'start_date'='2013-06-14','end_date'='2019-04-18','frequency':null}"
    # print(r)
    assets, weight = get_asset()
    weight = nav_constraint(weight, assets)
    print(weight)
    put = "{'label':'EPITA_PTF_10','currency':{'code':'EUR'},'type':'front','values':{'2013-06-14':["
    for i in range(len(assets)):
        put += "{'asset':{'asset':" + assets[i][0] + ",'quantity':" + str(weight[i]) + "}}"
        if(i != len(assets) -1):
            put += ","
    put += "]}}"
    r = put_data('portfolio/1829/dyn_amount_compo', put)
    print(r)
    r = get_data("portfolio/1829/dyn_amount_compo")
    print(r)
    r = post_data('ratio/invoke', tmp)
    print(r)
