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
        print(data['ASSET_DATABASE_ID']['value'])
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
                        print(assets[key]['10']['value'].replace(',', '.'))
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
    for i in range(39):
        total += x[i] * global_selected[i][2]

    return total * -1


def objectives_volatility(x):
    total = 0
    for i in range(39):
        total += x[i] * global_selected[i][3]

    return total


def objectives_portfolio(x):
    total = 0
    for i in range(21):
        total += x[i] * portfolio[i][2]

    return total * -1


def constraint_efficiency(x):
    total = 0
    for i in range(39):
        total += x[i]

    return total * -1 + 200


def constraint_volatility(x):
    total = 0
    for i in range(39):
        total += x[i]

    return total - 200


def constraint_portfolio(x):
    total = 0
    for i in range(21):
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
    print(selection)
    # selection = [['2142', 1.927698856275, 0.567463676118, 0.038838438131], ['2143', 1.533162400208, 1.1710239396, 0.089169390882], \
    # ['2132', 1.53069363495, 0.332169943134, 0.029564996327], ['2188', 1.518611441853, 0.154197543397, 0.013051136991], \
    # ['2112', 1.386671126619, 11.964509394572, 0.392783846849], ['1990', 1.372704343636, 10.520532741398, 0.374218565818], \
    # ['2064', 1.361522014963, 5.248729792148, 0.266526886961], ['2144', 1.341569142758, 1.106045804841, 0.097494365528], \
    # ['2187', 1.260083534206, 0.194833371591, 0.020554076784], ['1968', 1.248157717905, 4.405128205128, 0.263895706301], \
    # ['2191', 1.236273302637, 0.213035588673, 0.023108123862], ['2147', 1.195848873908, 1.197861386139, 0.116328848115], \
    # ['1897', 1.177882228021, 4.857664233577, 0.295319931832], ['1877', 1.133621851304, 3.574468085106, 0.257454978493], \
    # ['2189', 1.122544774598, 0.188721586617, 0.022267639904], ['2105', 1.107055124758, 1.910623321293, 0.176497187391], \
    # ['1585', 1.102538915329, 3.321940463065, 0.25334928462], ['1567', 1.092975385369, 1.689649407246, 0.164045423709], \
    # ['2013', 1.085774902123, 2.637284701114, 0.222893236332], ['1956', 1.073301082164, 5.271844660194, 0.338903930177], \
    # ['1956', 1.073301082164, 5.271844660194, 0.338903930177], ['2120', 1.066252500717, 5.044331395349, 0.33306083745], \
    # ['1897', 1.177882228021, 4.857664233577, 0.295319931832], ['2042', 0.728225293648, 4.129411764706, 0.435981424286], \
    # ['1877', 1.133621851304, 3.574468085106, 0.257454978493], ['2000', 0.94810095498, 3.572072072072, 0.307710307617], \
    # ['1960', 1.04890431228, 3.532142857143, 0.276285735303], ['1585', 1.102538915329, 3.321940463065, 0.25334928462], \
    # ['1912', 0.96445460953, 3.242937853107, 0.285428773847], ['1975', 0.808185754067, 3.209302325581, 0.338464559133], \
    # ['2053', 0.675111381869, 3.102122015915, 0.396848477527], ['1874', 0.797852846604, 3.060758082497, 0.333035514244], \
    # ['2035', 0.754393813319, 2.871275327771, 0.338516288407], ['1739', 0.661010928309, 2.729908367132, 0.374251497653], \
    # ['2013', 1.085774902123, 2.637284701114, 0.222893236332], ['1985', 0.641969005309, 2.588235294118, 0.372480261245], \
    # ['1872', 0.985677718011, 2.44512195122, 0.233843047639], ['1958', 1.036445517208, 2.359939186621, 0.217297463247], \
    # ['1977', 0.699185641822, 2.323987538941, 0.318880278123], ['2106', 0.956577056506, 2.177093358999, 0.223196346525]]
    global global_selected
    global_selected = selection
    assets, weight = optimize()
    assets = validate_selection(assets, stocks)
    return assets, weight
