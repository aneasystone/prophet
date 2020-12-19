amplitude_date = "20201218"
amplitude_stocks = """
MACDGOLDCROSSMINUS:
南玻A 000012.SZ 7.21
浩物股份 000757.SZ 4.73
省广集团 002400.SZ 5.54
雅化集团 002497.SZ 18.14
昊华能源 601101.SH 4.37
平煤股份 601666.SH 5.9
新集能源 601918.SH 3.09
石大胜华 603026.SH 48.16
金石资源 603505.SH 28.55
神力股份 603819.SH 11.6
MACDGOLDCROSS:
江铃汽车 000550.SZ 20.75
多氟多 002407.SZ 17.23
赣锋锂业 002460.SZ 89.4
中矿资源 002738.SZ 24.41
科力远 600478.SH 4.63
厦门钨业 600549.SH 16.5
开滦股份 600997.SH 6.27
广汽集团 601238.SH 14.27
骆驼股份 601311.SH 9.28
长城汽车 601633.SH 28.97
联明股份 603006.SH 10.44
禾望电气 603063.SH 17.93
HAMMER:
大参林 603233.SH 78.69
"""

import os
import re
import requests
import json
import time
from stock import Stock

def get_all_stocks():
    mas = re.findall('\d{6}\.S[H|Z]', amplitude_stocks)
    results = []
    for ma in mas:
        if 'SH' in ma:
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

def get_average_amplitude_dict(stocks):
    average_amplitude_dict = {}
    for stock in stocks:
        stk = Stock(stock['name'], stock['symbol'] + '.' + stock['type'], amplitude_date)
        if stk.init():
            average_amplitude_dict[stock['name']] = stk.get_average_amplitude(7)
    return average_amplitude_dict

def align(ss, length=15):
    if length == 0:
        return ss
    slen = len(ss)
    re = ss
    if isinstance(ss, str):
        placeholder = ' '
    else:
        placeholder = u'　'
    while slen < length:
        re += placeholder
        slen += 1
    return re

def show_current_price(stocks):
    print(align("CODE") + align("NAME") + align("PRE_CLOSE") + align("OPEN") + align("HIGH") + align("LOW") +
        align("AVG_AMP") + align("AMP") + align("PRICE") + 
        align("B1") + align("B2") + align("B3") + align("B4"))
    for stock in stocks:    
        # if '603002.SH' != stock['symbol'] + '.' + stock['type']:
        #     continue
        average_amplitude = 100 * average_amplitude_dict[stock['name']]    
        current_amplitude = 100 * (stock['high'] - stock['low']) / stock['yestclose']

        b1 = stock['yestclose'] * (1 - average_amplitude / 100 * 0.25)
        b2 = stock['yestclose'] * (1 - average_amplitude / 100 * 0.5)
        b3 = stock['yestclose'] * (1 - average_amplitude / 100 * 0.75)
        b4 = stock['yestclose'] * (1 - average_amplitude / 100 * 1)
        delta = (b1 - b2) / 2
        current_price = stock['price']
        
        info = align(stock['symbol'] + '.' + stock['type']) + \
                align(stock['name']) + \
                align("%.2f" % (stock['yestclose'])) + \
                align("%.2f" % (stock['open'])) + \
                align("%.2f" % (stock['high'])) + \
                align("%.2f" % (stock['low'])) + \
                align("%.2f" % (average_amplitude)) + \
                align("%.2f" % (current_amplitude)) + \
                align("%.2f" % (current_price)) + \
                align("%.2f" % (b1)) + \
                align("%.2f" % (b2)) + \
                align("%.2f" % (b3)) + \
                align("%.2f" % (b4))

        if b1 + delta > current_price > b1 - delta:
            print_red(info)
        elif b2 + delta > current_price > b2 - delta:
            print_green(info)
        elif b3 + delta > current_price > b3 - delta:
            print_yellow(info)
        elif b4 + delta > current_price > b4 - delta:
            print_blue(info)
        else:
            print_normal(info)
    # print(time.perf_counter())

def print_normal(s):
    print(s)

def print_red(s):
    print(f"\033[0;31;40m%s\033[0m" % (s))

def print_green(s):
    print(f"\033[0;32;40m%s\033[0m" % (s))

def print_yellow(s):
    print(f"\033[0;33;40m%s\033[0m" % (s))

def print_blue(s):
    print(f"\033[0;34;40m%s\033[0m" % (s))

if __name__ == '__main__':

    # get all stocks and real price
    mas = get_all_stocks()
    stocks = get_real_price(mas)
    
    # get average amplitude dict
    average_amplitude_dict = get_average_amplitude_dict(stocks)
    # print(average_amplitude_dict)

    while True:
        os.system("clear")
        show_current_price(stocks)
        time.sleep(5)
        stocks = get_real_price(mas)
