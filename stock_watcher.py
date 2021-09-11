amplitude_date = "20210910"
all_stocks = """
000738 航发控制
002534 杭锅股份
601058 赛轮轮胎
600478 科力远
603212 赛伍技术
002015 协鑫能科
600765 中航重机
000935 四川双马
002097 山河智能
000848 承德露露
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
