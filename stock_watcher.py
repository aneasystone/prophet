amplitude_date = "20201218"
amplitude_stocks = """
南玻A　　　　　　　     000012.SZ       7.21            玻璃　　　　　　　　    HAMMERPLUS,MACDGOLDCROSSMINUS
江铃汽车　　　　　　    000550.SZ       20.75           汽车整车　　　　　　    MACDGOLDCROSS
粤宏远A　　　　　　     000573.SZ       2.97            区域地产　　　　　　    HAMMERPLUS
浩物股份　　　　　　    000757.SZ       4.73            汽车配件　　　　　　    MACDGOLDCROSSMINUS
鲁西化工　　　　　　    000830.SZ       13.6            农药化肥　　　　　　    HAMMERPLUS
冀中能源　　　　　　    000937.SZ       4.09            煤炭开采　　　　　　    TURNOVER  
德美化工　　　　　　    002054.SZ       8.47            化工原料　　　　　　    HAMMERPLUS
金风科技　　　　　　    002202.SZ       13.1            电气设备　　　　　　    HAMMERPLUS
台海核电　　　　　　    002366.SZ       3.56            专用机械　　　　　　    HAMMER    
省广集团　　　　　　    002400.SZ       5.54            广告包装　　　　　　    MACDGOLDCROSSMINUS
多氟多　　　　　　　    002407.SZ       17.23           化工原料　　　　　　    MACDGOLDCROSS
大金重工　　　　　　    002487.SZ       8.68            钢加工　　　　　　　    HAMMERPLUS
雅化集团　　　　　　    002497.SZ       18.14           化工原料　　　　　　    MACDGOLDCROSSMINUS
华西能源　　　　　　    002630.SZ       2.59            专用机械　　　　　　    TURNOVER  
海洋王　　　　　　　    002724.SZ       7.77            半导体　　　　　　　    HAMMERPLUS
中矿资源　　　　　　    002738.SZ       24.41           小金属　　　　　　　    MACDGOLDCROSS
兰花科创　　　　　　    600123.SH       5.89            煤炭开采　　　　　　    TURNOVER  
科力远　　　　　　　    600478.SH       4.63            元器件　　　　　　　    MACDGOLDCROSS
上海能源　　　　　　    600508.SH       10.07           煤炭开采　　　　　　    TURNOVER  
厦门钨业　　　　　　    600549.SH       16.5            小金属　　　　　　　    MACDGOLDCROSS,TURNOVER
哈投股份　　　　　　    600864.SH       7.6             证券　　　　　　　　    TURNOVER  
开滦股份　　　　　　    600997.SH       6.27            煤炭开采　　　　　　    MACDGOLDCROSS
昊华能源　　　　　　    601101.SH       4.37            煤炭开采　　　　　　    MACDGOLDCROSSMINUS
广汽集团　　　　　　    601238.SH       14.27           汽车整车　　　　　　    MACDGOLDCROSS
骆驼股份　　　　　　    601311.SH       9.28            电气设备　　　　　　    MACDGOLDCROSS
中国中冶　　　　　　    601618.SH       2.86            建筑工程　　　　　　    TURNOVER  
平煤股份　　　　　　    601666.SH       5.9             煤炭开采　　　　　　    MACDGOLDCROSSMINUS
新集能源　　　　　　    601918.SH       3.09            煤炭开采　　　　　　    MACDGOLDCROSSMINUS
联明股份　　　　　　    603006.SH       10.44           汽车配件　　　　　　    MACDGOLDCROSS
禾望电气　　　　　　    603063.SH       17.93           电气设备　　　　　　    HAMMERPLUS,MACDGOLDCROSS
东方电缆　　　　　　    603606.SH       23.12           电气设备　　　　　　    TURNOVER  
江苏新能　　　　　　    603693.SH       12.16           新型电力　　　　　　    TURNOVER  
天域生态　　　　　　    603717.SH       8.25            环境保护　　　　　　    TURNOVER  
乾景园林　　　　　　    603778.SH       4.54            建筑工程　　　　　　    HAMMERPLUS
神力股份　　　　　　    603819.SH       11.6            电气设备　　　　　　    MACDGOLDCROSSMINUS
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

def show_current_price(stocks):
    print("{0:<10}{1:{13}<8}{2:<10}{3:<10}{4:<10}{5:<10}{6:<10}{7:<10}{8:<10}{9:<10}{10:<10}{11:<10}{12:<10}".format(
        "CODE", "NAME", "PRE_CLOSE", "OPEN", "HIGH", "LOW", "AVG_AMP", "AMP", "PRICE", "B1", "B2", "B3", "B4", chr(12288)))
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

        info = "{0:<10}{1:{13}<6}{2:<10}{3:<10}{4:<10}{5:<10}{6:<10}{7:<10}{8:<10}{9:<10}{10:<10}{11:<10}{12:<10}".format(
            stock['symbol'] + '.' + stock['type'], 
            stock['name'].replace(' ', ''),
            "%.2f" % (stock['yestclose']),
            "%.2f" % (stock['open']),
            "%.2f" % (stock['high']),
            "%.2f" % (stock['low']),
            "%.2f" % (average_amplitude),
            "%.2f" % (current_amplitude),
            "%.2f" % (current_price),
            "%.2f" % (b1),
            "%.2f" % (b2),
            "%.2f" % (b3),
            "%.2f" % (b4),
            chr(12288))

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
