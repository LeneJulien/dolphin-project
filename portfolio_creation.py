import json

from scipy.optimize import minimize
from scipy.stats import rankdata

from tools import get_data
from tools import post_data


def request_asset_list():
    r = get_data("asset?columns=ASSET_DATABASE_ID&columns=TYPE&columns=LABEL&columns=LAST_CLOSE_VALUE_IN_CURR",
                 start_date='2013-06-14', end_date='2019-04-18')
    dic_asset = json.loads(r)
    return dic_asset


def asset_sort(dic_asset):
    stocks = []
    for data in dic_asset:
        if data['TYPE']['value'] == 'STOCK':
            stocks.append(data)
    return stocks


# date de debut 14/06/2013
# date de fin 18/04/2019
def asset_id_sort(assets):
    for data in assets:
        r = get_data("asset/" + data['ASSET_DATABASE_ID']['value'] + "?columns=CURRENCY")


def get_value_asset(assets):
    res = []
    for data in assets:
        tmp = "{'ratio'=[10, 12, 13],'asset'=[" + data['ASSET_DATABASE_ID'][
            'value'] + "],'start_date'='2013-06-14','end_date'='2019-04-18','frequency':null}"
        r = post_data('ratio/invoke', tmp)
        value_dic = json.loads(r)
        res.append(value_dic)
    return res


def select_assets(x):
    tab = []
    for assets in x:
        for key in assets.keys():
            if key != '2201' and key != "1829" and assets[key]['12']['type'] != "error":
                if float(assets[key]['12']['value'].replace(',', '.')) > 0.5:
                    if float(assets[key]['10']['value'].replace(',', '.')) < 0.5:
                        tab.append([key, float(assets[key]['12']['value'].replace(',', '.')),
                                    float(assets[key]['13']['value'].replace(',', '.')),
                                    float(assets[key]['10']['value'].replace(',', '.'))])
    ref = [0, 0]
    k = 0
    bestSharp = []
    for i in range(100):
        for elt in tab:
            if elt[1] > ref[1]:
                ref = [k, elt[1]]
            k += 1
        bestSharp.append(tab[ref[0]])
        tab.pop(ref[0])
        ref = [0, 0]
        k = 0
    return bestSharp


def validate_selection(tab, stocks):
    ratio = 0
    for elt in tab:
        for stock in stocks:
            if elt[0] == stock['ASSET_DATABASE_ID']['value']:
                ratio += 1
                break
    ratio /= len(tab)
    print("Ratio of STOCK : " + str(ratio))
    return tab


def reduce_selection(bestSharp, stocks):
    selected = []
    for i in range(20):
        selected.append(bestSharp[i])
    for i in range(20):
        bestSharp.pop(0)
    ref = [0, 0]
    k = 0
    for i in range(20):
        for elt in bestSharp:
            if elt[2] > ref[1]:
                ref = [k, elt[2]]
            k += 1
        selected.append(bestSharp[ref[0]])
        bestSharp.pop(ref[0])
        ref = [0, 0]
        k = 0
    return validate_selection(selected, stocks)


global_selected = []
portfolio = []


def selected_weight(max_efficiency, min_volatility, selection):
    ratio = []
    for i in range(40):
        ratio.append((max_efficiency[i] + min_volatility[i]) / 2)
    rank = (rankdata(ratio) - 1).astype(int)
    res = []
    for i in range(40):
        if rank[i] >= 18:
            res.append(selection[i])
    return res


def objectives_efficiency(x):
    total = 0
    for i in range(40):
        total += x[i] * global_selected[i][2]

    return total * -1


def objectives_volatility(x):
    total = 0
    for i in range(40):
        total += x[i] * global_selected[i][3]

    return total


def objectives_portfolio(x):
    total = 0
    for i in range(22):
        total += x[i] * portfolio[i][2]

    return total * -1


def constraint_efficiency(x):
    total = 0
    for i in range(40):
        total += x[i]

    return total * -1 + 200


def constraint_volatility(x):
    total = 0
    for i in range(40):
        total += x[i]

    return total - 200


def constraint_portfolio(x):
    total = 0
    for i in range(22):
        total += x[i]

    return total * -1 + 100


def optimize():
    x0 = [1] * 40
    b = (1.0, 10.0)
    bnds = tuple(b for _ in range(40))
    cons = [{'type': 'ineq', 'fun': constraint_efficiency}]
    max_efficiency = minimize(objectives_efficiency, x0, method='SLSQP', bounds=bnds, constraints=cons).x
    cons = [{'type': 'ineq', 'fun': constraint_volatility}]
    min_volatility = minimize(objectives_volatility, x0, method='SLSQP', bounds=bnds, constraints=cons).x
    global portfolio
    portfolio = selected_weight(max_efficiency, min_volatility, global_selected)
    x0 = [1] * 22
    cons = [{'type': 'ineq', 'fun': constraint_portfolio}]
    bnds = tuple(b for _ in range(22))
    return portfolio, minimize(objectives_portfolio, x0, method='SLSQP', bounds=bnds, constraints=cons).x


def get_asset():
    asset_dict = request_asset_list()
    stocks = asset_sort(asset_dict)
    x = get_value_asset(asset_dict)
    bestSharp = select_assets(x)
    selection = reduce_selection(bestSharp, stocks)
    global global_selected
    global_selected = selection
    assets, weight = optimize()
    assets = validate_selection(assets, stocks)
    for elt in assets:
        for data in asset_dict:
            if data['ASSET_DATABASE_ID']['value'] == elt[0]:
                elt.append(data['LAST_CLOSE_VALUE_IN_CURR']['value'])
                break
    return assets, weight