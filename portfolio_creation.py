import requests
from tools import get_data
from tools import post_data
import json
from scipy.optimize import minimize
from scipy.stats import rankdata


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

#date de debut 14/06/2013
#date de fin 18/04/2019
def asset_id_sort(assets):
    for data in assets:
        print(data['ASSET_DATABASE_ID']['value'])
        r = get_data("asset/" + data['ASSET_DATABASE_ID']['value'] + "?columns=CURRENCY")

def get_value_asset(assets):
    res = []
    for data in assets:
        tmp = "{'ratio'=[10, 12, 13],'asset'=[" + data['ASSET_DATABASE_ID']['value'] + "],'start_date'='2013-06-14','end_date'='2019-04-18','frequency':null}"
        r = post_data('ratio/invoke', tmp)
        value_dic = json.loads(r)
        res.append(value_dic)
    return res

def select_assets(x):
    tab = []
    for assets in x:
        for key in assets.keys():
            if(key != "2201" and key != "1829" and assets[key]['12']['type'] != "error"):
                if(float(assets[key]['12']['value'].replace(',', '.')) > 0,5):
                    if(float(assets[key]['10']['value'].replace(',', '.')) < 0.5):
                        print(assets[key]['10']['value'].replace(',', '.'))
                        tab.append([key, float(assets[key]['12']['value'].replace(',', '.')), float(assets[key]['13']['value'].replace(',', '.')), \
                                float(assets[key]['10']['value'].replace(',', '.'))])
    ref = [0, 0]
    k = 0
    bestSharp = []
    for i in range(100):
        for elt in tab:
            if(elt[1] > ref[1]):
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
            if(elt[2] > ref[1]):
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
        if(rank[i] >= 18):
            res.append(selection[i])
    return res

def objectives_efficiency(x):
    x1 = x[0] * global_selected[0][2]
    x2 = x[1] * global_selected[1][2]
    x3 = x[2] * global_selected[2][2]
    x4 = x[3] * global_selected[3][2]
    x5 = x[4] * global_selected[4][2]
    x6 = x[5] * global_selected[5][2]
    x7 = x[6] * global_selected[6][2]
    x8 = x[7] * global_selected[7][2]
    x9 = x[8] * global_selected[8][2]
    x10 = x[9] * global_selected[9][2]
    x11 = x[10] * global_selected[10][2]
    x12 = x[11] * global_selected[11][2]
    x13 = x[12] * global_selected[12][2]
    x14 = x[13] * global_selected[13][2]
    x15 = x[14] * global_selected[14][2]
    x16 = x[15] * global_selected[15][2]
    x17 = x[16] * global_selected[16][2]
    x18 = x[17] * global_selected[17][2]
    x19 = x[18] * global_selected[18][2]
    x20 = x[19] * global_selected[19][2]
    x21 = x[20] * global_selected[20][2]
    x22 = x[21] * global_selected[21][2]
    x23 = x[22] * global_selected[22][2]
    x24 = x[23] * global_selected[23][2]
    x25 = x[24] * global_selected[24][2]
    x26 = x[25] * global_selected[25][2]
    x27 = x[26] * global_selected[26][2]
    x28 = x[27] * global_selected[27][2]
    x29 = x[28] * global_selected[28][2]
    x30 = x[29] * global_selected[29][2]
    x31 = x[30] * global_selected[30][2]
    x32 = x[31] * global_selected[31][2]
    x33 = x[32] * global_selected[32][2]
    x34 = x[33] * global_selected[33][2]
    x35 = x[34] * global_selected[34][2]
    x36 = x[35] * global_selected[35][2]
    x37 = x[36] * global_selected[36][2]
    x38 = x[37] * global_selected[37][2]
    x39 = x[38] * global_selected[38][2]
    x40 = x[39] * global_selected[39][2]
    return (x1 + x2 + x3 + x4 + x5 + x6 + x7 + x8 + x9 + x10 + x11 + x12 + x13 + x14 + x15 + x16 + x17 + x18 + x19 + x20 \
        + x21 + x22 + x23 + x24 + x25 + x26 + x27 + x28 + x29 + x30 + x31 + x32 + x33 + x34 + x35 + x36 + x37 + x38 + x39 + x40)* -1

def objectives_volatility(x):
    x1 = x[0] * global_selected[0][3]
    x2 = x[1] * global_selected[1][3]
    x3 = x[2] * global_selected[2][3]
    x4 = x[3] * global_selected[3][3]
    x5 = x[4] * global_selected[4][3]
    x6 = x[5] * global_selected[5][3]
    x7 = x[6] * global_selected[6][3]
    x8 = x[7] * global_selected[7][3]
    x9 = x[8] * global_selected[8][3]
    x10 = x[9] * global_selected[9][3]
    x11 = x[10] * global_selected[10][3]
    x12 = x[11] * global_selected[11][3]
    x13 = x[12] * global_selected[12][3]
    x14 = x[13] * global_selected[13][3]
    x15 = x[14] * global_selected[14][3]
    x16 = x[15] * global_selected[15][3]
    x17 = x[16] * global_selected[16][3]
    x18 = x[17] * global_selected[17][3]
    x19 = x[18] * global_selected[18][3]
    x20 = x[19] * global_selected[19][3]
    x21 = x[20] * global_selected[20][3]
    x22 = x[21] * global_selected[21][3]
    x23 = x[22] * global_selected[22][3]
    x24 = x[23] * global_selected[23][3]
    x25 = x[24] * global_selected[24][3]
    x26 = x[25] * global_selected[25][3]
    x27 = x[26] * global_selected[26][3]
    x28 = x[27] * global_selected[27][3]
    x29 = x[28] * global_selected[28][3]
    x30 = x[29] * global_selected[29][3]
    x31 = x[30] * global_selected[30][3]
    x32 = x[31] * global_selected[31][3]
    x33 = x[32] * global_selected[32][3]
    x34 = x[33] * global_selected[33][3]
    x35 = x[34] * global_selected[34][3]
    x36 = x[35] * global_selected[35][3]
    x37 = x[36] * global_selected[36][3]
    x38 = x[37] * global_selected[37][3]
    x39 = x[38] * global_selected[38][3]
    x40 = x[39] * global_selected[39][3]
    return x1 + x2 + x3 + x4 + x5 + x6 + x7 + x8 + x9 + x10 + x11 + x12 + x13 + x14 + x15 + x16 + x17 + x18 + x19 + x20 \
        + x21 + x22 + x23 + x24 + x25 + x26 + x27 + x28 + x29 + x30 + x31 + x32 + x33 + x34 + x35 + x36 + x37 + x38 + x39 + x40

def objectives_portfolio(x):
    x1 = x[0] * portfolio[0][2]
    x2 = x[1] * portfolio[1][2]
    x3 = x[2] * portfolio[2][2]
    x4 = x[3] * portfolio[3][2]
    x5 = x[4] * portfolio[4][2]
    x6 = x[5] * portfolio[5][2]
    x7 = x[6] * portfolio[6][2]
    x8 = x[7] * portfolio[7][2]
    x9 = x[8] * portfolio[8][2]
    x10 = x[9] * portfolio[9][2]
    x11 = x[10] * portfolio[10][2]
    x12 = x[11] * portfolio[11][2]
    x13 = x[12] * portfolio[12][2]
    x14 = x[13] * portfolio[13][2]
    x15 = x[14] * portfolio[14][2]
    x16 = x[15] * portfolio[15][2]
    x17 = x[16] * portfolio[16][2]
    x18 = x[17] * portfolio[17][2]
    x19 = x[18] * portfolio[18][2]
    x20 = x[19] * portfolio[19][2]
    x21 = x[20] * portfolio[20][2]
    x22 = x[21] * portfolio[21][2]

    return (x1 + x2 + x3 + x4 + x5 + x6 + x7 + x8 + x9 + x10 + x11 + x12 + x13 + x14 + x15 + x16 + x17 + x18 + x19 + x20 + x21 + x22)* -1

def constraint_efficiency(x):
    return (x[0] + x[1] + x[2] + x[3] + x[4] + x[5] + x[6] + x[7] + x[8] + x[9] + x[10] + x[11] + x[12] + x[13] + x[14] + x[15] + x[16] + x[17] + x[18] + x[19] \
        + x[20] + x[21] + x[22] + x[23] + x[24] + x[25] + x[26] + x[27] + x[28] + x[29] + x[30] + x[31] + x[32] + x[33] + x[34] + x[35] + x[36] + x[37] + x[38] + x[39])* -1 + 200

def constraint_volatility(x):
    return x[0] + x[1] + x[2] + x[3] + x[4] + x[5] + x[6] + x[7] + x[8] + x[9] + x[10] + x[11] + x[12] + x[13] + x[14] + x[15] + x[16] + x[17] + x[18] + x[19] \
        + x[20] + x[21] + x[22] + x[23] + x[24] + x[25] + x[26] + x[27] + x[28] + x[29] + x[30] + x[31] + x[32] + x[33] + x[34] + x[35] + x[36] + x[37] + x[38] + x[39] - 200

def constraint_portfolio(x):
    return (x[0] + x[1] + x[2] + x[3] + x[4] + x[5] + x[6] + x[7] + x[8] + x[9] + x[10] + x[11] + x[12] + x[13] + x[14] + x[15] + x[16] + x[17] + x[18] + x[19] \
        + x[20] + x[21])* -1 + 100


def optimize():
    x0 = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    b = (1.0, 10.0)
    bnds = (b, b, b, b, b, b, b, b, b, b, b, b, b, b, b, b, b, b, b, b, b, b, b, b, b, b, b, b, b, b, b, b, b, b, b, b, b, b, b, b)
    cons = [{'type': 'ineq', 'fun': constraint_efficiency}]
    max_efficiency = minimize(objectives_efficiency, x0, method='SLSQP', bounds=bnds, constraints=cons).x
    cons = [{'type': 'ineq', 'fun': constraint_volatility}]
    min_volatility = minimize(objectives_volatility, x0, method='SLSQP', bounds=bnds, constraints=cons).x
    global portfolio
    portfolio = selected_weight(max_efficiency, min_volatility, global_selected)
    x0 = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    cons = [{'type': 'ineq', 'fun': constraint_portfolio}]
    bnds = (b, b, b, b, b, b, b, b, b, b, b, b, b, b, b, b, b, b, b, b, b, b)
    return portfolio, minimize(objectives_portfolio, x0, method='SLSQP', bounds=bnds, constraints=cons).x

def get_asset():
    asset_dict = request_asset_list()
    stocks = asset_sort(asset_dict)
    x = get_value_asset(asset_dict)
    bestSharp = select_assets(x)
    selection = reduce_selection(bestSharp, stocks)
    print(selection)
    #selection = [['2142', 1.927698856275, 0.567463676118, 0.038838438131], ['2143', 1.533162400208, 1.1710239396, 0.089169390882], \
    #['2132', 1.53069363495, 0.332169943134, 0.029564996327], ['2188', 1.518611441853, 0.154197543397, 0.013051136991], \
    #['2112', 1.386671126619, 11.964509394572, 0.392783846849], ['1990', 1.372704343636, 10.520532741398, 0.374218565818], \
    #['2064', 1.361522014963, 5.248729792148, 0.266526886961], ['2144', 1.341569142758, 1.106045804841, 0.097494365528], \
    #['2187', 1.260083534206, 0.194833371591, 0.020554076784], ['1968', 1.248157717905, 4.405128205128, 0.263895706301], \
    #['2191', 1.236273302637, 0.213035588673, 0.023108123862], ['2147', 1.195848873908, 1.197861386139, 0.116328848115], \
    #['1897', 1.177882228021, 4.857664233577, 0.295319931832], ['1877', 1.133621851304, 3.574468085106, 0.257454978493], \
    #['2189', 1.122544774598, 0.188721586617, 0.022267639904], ['2105', 1.107055124758, 1.910623321293, 0.176497187391], \
    #['1585', 1.102538915329, 3.321940463065, 0.25334928462], ['1567', 1.092975385369, 1.689649407246, 0.164045423709], \
    #['2013', 1.085774902123, 2.637284701114, 0.222893236332], ['1956', 1.073301082164, 5.271844660194, 0.338903930177], \
    #['1956', 1.073301082164, 5.271844660194, 0.338903930177], ['2120', 1.066252500717, 5.044331395349, 0.33306083745], \
    #['1897', 1.177882228021, 4.857664233577, 0.295319931832], ['2042', 0.728225293648, 4.129411764706, 0.435981424286], \
    #['1877', 1.133621851304, 3.574468085106, 0.257454978493], ['2000', 0.94810095498, 3.572072072072, 0.307710307617], \
    #['1960', 1.04890431228, 3.532142857143, 0.276285735303], ['1585', 1.102538915329, 3.321940463065, 0.25334928462], \
    #['1912', 0.96445460953, 3.242937853107, 0.285428773847], ['1975', 0.808185754067, 3.209302325581, 0.338464559133], \
    #['2053', 0.675111381869, 3.102122015915, 0.396848477527], ['1874', 0.797852846604, 3.060758082497, 0.333035514244], \
    #['2035', 0.754393813319, 2.871275327771, 0.338516288407], ['1739', 0.661010928309, 2.729908367132, 0.374251497653], \
    #['2013', 1.085774902123, 2.637284701114, 0.222893236332], ['1985', 0.641969005309, 2.588235294118, 0.372480261245], \
    #['1872', 0.985677718011, 2.44512195122, 0.233843047639], ['1958', 1.036445517208, 2.359939186621, 0.217297463247], \
    #['1977', 0.699185641822, 2.323987538941, 0.318880278123], ['2106', 0.956577056506, 2.177093358999, 0.223196346525]]
    global global_selected
    global_selected = selection
    assets, weight = optimize()
    assets = validate_selection(assets, stocks)
    return assets, weight