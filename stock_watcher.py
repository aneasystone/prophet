amplitude_date = "20210917"
all_stocks = """
代码		    名称		
SZ002498	汉缆股份	
SH603979	金诚信		
SZ002002	鸿达兴业	
SH600782	新钢股份	
SH601699	潞安环能	
SZ000898	鞍钢股份	
SZ000761	本钢板材	
SH600395	盘江股份	
SZ000960	锡业股份	
SH600348	华阳股份	
SH603688	石英股份	
SZ000683	远兴能源	
SH600010	包钢股份	
SZ000762	西藏矿业	
SZ000708	中信特钢	
SH603995	甬金股份	
SH600426	华鲁恒升	
SH600176	中国巨石	
SH600409	三友化工	
SZ002079	苏州固锝	
SH600111	北方稀土	
SH600733	北汽蓝谷	
SH600586	金晶科技	
SZ002171	楚江新材	
SZ002135	东南网架	
SZ002155	湖南黄金	
SH600338	西藏珠峰	
SZ002585	双星新材	
SH601238	广汽集团	
SH601117	中国化学	
SH600958	东方证券	
SH601717	郑煤机		
SH600587	新华医疗	
SH601058	赛轮轮胎	
SH600765	中航重机	
"""

import os
import re
import requests
import json
import time
from stock import Stock

def get_all_stocks():
    mas = re.findall('\d{6}', all_stocks)
    results = []
    for ma in mas:
        if ma.startswith('6'):
            results.append('0' + ma[0:6])
        else:  
            results.append('1' + ma[0:6])
    return results

def get_real_price(mas):
    url = "https://api.money.126.net/data/feed/%s?callback=a" % (",".join(mas))
    response = requests.get(url)
    content = response.content.decode('utf-8')
    stocks = json.loads(content[2:-2])
    results = []
    for s in stocks:
        results.append(stocks[s])
    return results

ma30_dict = {}
def init_ma30_dict(stocks):
    for stock in stocks:
        stk = Stock(stock['name'], stock['symbol'] + '.' + stock['type'], amplitude_date)
        if stk.init():
            ma30_dict[stock['name']] = stk.ma30[-1]

def get_ma30_diff(stock):
    ma30_price = ma30_dict[stock['name']]
    current_price = stock['price']
    return (current_price-ma30_price)/ma30_price*100

def show_current_price(stocks):
    print("{0:<10}\t{1:<10}\t{2:<10}\t{3:<10}\t{4:<10}\t{5:<10}".format("股票代码", "股票名称", "30日均线", "当日最低价", "当前价", "买点距离"))
    stocks = sorted(stocks, key=get_ma30_diff, reverse=False)
    for stock in stocks:
        ma30_price = ma30_dict[stock['name']]
        low_price = stock['low']
        current_price = stock['price']
        diff = (current_price-ma30_price)/ma30_price*100
        info = "{0:<10}\t{1:<10}\t{2:<10}\t{3:<10}\t{4:<10}\t{5:<10}".format(
            stock['symbol'] + '.' + stock['type'], 
            stock['name'].replace(' ', ''),
            "%.2f" % (ma30_price),
            "%.2f" % (low_price),
            "%.2f" % (current_price),
            "%.2f%%" % (diff))
        if low_price <= ma30_price:
            # already low than ma30
            if current_price <= ma30_price:
                print_green(info)
            else:
                print_blue(info)
        else:
            if diff < 1:
                # very close to ma30
                print_yellow(info)
            else:
                print_normal(info)

def print_normal(s):
    print(s)

def print_green(s):
    print(f"\033[0;32;40m%s %s\033[0m" % (s, "买点已到，关注分时图，均线突破时买入"))

def print_yellow(s):
    print(f"\033[0;33;40m%s %s\033[0m" % (s, "即将到达买点"))

def print_blue(s):
    print(f"\033[0;34;40m%s %s\033[0m" % (s, "刚刚错过买点，关注分时图，均线突破时买入，若已突破一段距离，不操作"))

if __name__ == '__main__':

    # get all stocks and real price
    mas = get_all_stocks()
    stocks = get_real_price(mas)
    
    # init ma30 dict
    init_ma30_dict(stocks)

    while True:
        os.system('cls')
        show_current_price(stocks)
        time.sleep(10)
        stocks = get_real_price(mas)
