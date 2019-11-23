import requests
from tools import get_data
from tools import post_data
import json

def request_asset_list():
    r = get_data("asset?columns=ASSET_DATABASE_ID&columns=TYPE&columns=LABEL&columns=LAST_CLOSE_VALUE_IN_CURR",
                 start_date='2013-06-14', end_date='2019-04-18')
    dic_asset = json.loads(r)
    return dic_asset

def asset_sort(dic_asset):
    stocks = []
    funds = []
    indexs = []
    for data in dic_asset:
        print(data)
        if data['TYPE']['value'] == 'STOCK':
            stocks.append(data)
        elif data['TYPE']['value'] == 'FUND':
            funds.append(data)
        elif data['TYPE']['value'] == 'INDEX':
            indexs.append(data)
    return stocks, funds, indexs

#date de debut 14/06/2013
#date de fin 18/04/2019
def asset_id_sort(assets):
    for data in assets:
        print(data['ASSET_DATABASE_ID']['value'])
        r = get_data("asset/" + data['ASSET_DATABASE_ID']['value'] + "?columns=CURRENCY")

def get_value_asset(assets):
    res = []
    for data in assets:
        tmp = "{'ratio'=[9, 12, 10, 13],'asset'=[" + data['ASSET_DATABASE_ID']['value'] + "],'start_date'='2013-06-14','end_date'='2019-04-18','frequency':null}"
        r = post_data('ratio/invoke', tmp)
        value_dic = json.loads(r)
        res.append(value_dic)
    print(res)
    return res

def select_assets(x):
    tab = []
    for assets in x:
        for key in assets.keys():
            if(key != "2201" and assets[key]['12']['type'] != "error"):
                if(float(assets[key]['12']['value'].replace(',', '.')) > 0,5):
                    tab.append([key, float(assets[key]['12']['value'].replace(',', '.')), float(assets[key]['13']['value'].replace(',', '.'))])
    print(len(tab))
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

def reduce_selection(bestSharp):
    selected = []
    for i in range(10):
        selected.append(bestSharp[i])
    for i in range(10):    
        bestSharp.pop(0)
    ref = [0, 0]
    k = 0
    for i in range(10):
        for elt in bestSharp:
            if(elt[2] > ref):
                ref = [k, elt[2]]
            k += 1
        selected.append(bestSharp[ref[0]])
        bestSharp.pop(ref[0])
        ref = [0, 0]
        k = 0
    return selected


def get_asset():
    asset_dict = request_asset_list()
    #stocks, funds, indexs = asset_sort(asset_dict)
    x = get_value_asset(asset_dict)
    #y = get_value_asset(funds)
    #z = get_value_asset(indexs)
    bestSharp = select_assets(x)
    #bestSharp = [['2142', 1.927698856275], ['2143', 1.533162400208], ['2132', 1.53069363495], ['2188', 1.518611441853], ['2112', 1.386671126619], ['1990', 1.372704343636], ['2064', 1.361522014963], ['2144', 1.341569142758], ['2187', 1.260083534206], ['1968', 1.248157717905], ['2191', 1.236273302637], ['2147', 1.195848873908], ['1897', 1.177882228021], ['1877', 1.133621851304], ['2189', 1.122544774598], ['2105', 1.107055124758], ['1585', 1.102538915329], ['1567', 1.092975385369], ['2013', 1.085774902123], ['1956', 1.073301082164], ['2120', 1.066252500717], ['1960', 1.04890431228], ['1958', 1.036445517208], ['2173', 1.008370015836], ['1872', 0.985677718011], ['2026', 0.973000259969], ['1912', 0.96445460953], ['1731', 0.960460202743], ['2106', 0.956577056506], ['2000', 0.94810095498], ['1563', 0.933754100231], ['1444', 0.928177669546], ['2196', 0.922200544151], ['1971', 0.921079694745], ['1756', 0.899412979099], ['1431', 0.896227760621], ['2018', 0.880423700667], ['2170', 0.860087364413], ['1934', 0.847081381339], ['1779', 0.844353625972], ['1451', 0.843414111635], ['2074', 0.826477328922], ['1465', 0.820741510124], ['1566', 0.819043849299], ['2067', 0.815990447319], ['2172', 0.809600439348], ['1975', 0.808185754067], ['1995', 0.801955922347], ['1874', 0.797852846604], ['2129', 0.793350723251], ['1876', 0.79065513934], ['2146', 0.786917819919], ['2040', 0.784010205527], ['2085', 0.778267555222], ['2194', 0.777094639979], ['1474', 0.775034692974], ['2091', 0.774055190869], ['1609', 0.76956061056], ['1485', 0.769387585803], ['1603', 0.765699185075], ['1596', 0.75784149977], ['1445', 0.757392432739], ['2195', 0.755674776079], ['2035', 0.754393813319], ['1573', 0.753635894595], ['1430', 0.751769682797], ['1792', 0.730062567166], ['2042', 0.728225293648], ['2004', 0.718150318541], ['2062', 0.71686790274], ['1764', 0.711111027507], ['1910', 0.699732967239], ['1977', 0.699185641822], ['2066', 0.696780675946], ['1931', 0.690874922999], ['2171', 0.688087149531], ['1777', 0.687091513591], ['1514', 0.686930186662], ['1787', 0.683214943925], ['2053', 0.675111381869], ['1928', 0.674766456407], ['2046', 0.664384708356], ['1739', 0.661010928309], ['1439', 0.65808783049], ['1433', 0.656873308482], ['2065', 0.65592174233], ['2063', 0.653116973814], ['1729', 0.642464587922], ['1985', 0.641969005309], ['2075', 0.638550271871], ['1791', 0.630331800813], ['2057', 0.628636802728], ['1911', 0.621589836759], ['2101', 0.621091836032], ['2163', 0.615047256412], ['2183', 0.612380987933], ['1577', 0.606068001433], ['1786', 0.604133279852], ['1595', 0.603269770931], ['2135', 0.592315941797]]
    selection = reduce_selection(bestSharp)
    print(selection)
