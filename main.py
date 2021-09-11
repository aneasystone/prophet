import traceback
from stock import Stock
from repository import Repository
from updator import Updator
from strategy_factory import StrategyFactory

repo = Repository()

def print_green(s):
    print(f"\033[0;32;40m%s\033[0m" % (s))

def print_red(s):
    print(f"\033[0;31;40m%s\033[0m" % (s))

def get_ma20_diff(stk):
    _close = stk.prices['close'].values[-1]
    _ma20 = stk.ma20[-1]
    # print(_close, _ma20)
    return (_ma20 - _close) / _close * 100

def get_red_days(stk):
    red_days = 0
    days = 60
    if len(stk.prices['close'].values) < days:
        days = len(stk.prices['close'].values)
    for i in range(1,days):
        _close = stk.prices['close'].values[-i]
        _pre_close = stk.prices['pre_close'].values[-i]
        if (_close - _pre_close) / _pre_close > 0.07:
            red_days += 1
    return red_days

def show_stock_stat_result(stks):
    print("===============================")
    map = {}
    stocks = repo.get_all_stocks()
    for stk in stocks:
        if stk['industry'] not in map:
            map[stk['industry']] = { "total": 0, "match": 0 }
        map[stk['industry']]["total"] += 1
    for stk in stks:
        map[stk.industry]["match"] += 1
    for industry in map:
        if industry:
            print("{0:{3}<10}\t{1:<10}\t{2:<10}".format(industry, map[industry]["match"], map[industry]["total"], chr(12288)))

def show_stock_result(trade_date, stk):
    ma20_diff = get_ma20_diff(stk)
    red_days = get_red_days(stk)
    info = "{0:{5}<10}\t{1:<10}\t{2:<10}\t{3:{5}<10}\t{4}\t{6}\t{7}".format(
            stk.name,
            stk.code,
            str(stk.close),
            stk.industry,
            ", ".join(stk.features),
            chr(12288),
            "%.2f%%" % (ma20_diff),
            red_days)
    if ma20_diff > -3.0:
        print_green(info)
    else:
        print(info)

def sort_by_ma20_diff(stks):
    return sorted(stks, key=get_ma20_diff, reverse=True)

def int_to_bytes(x: int) -> bytes:
    return x.to_bytes((x.bit_length() + 7) // 8, 'little')

def write_sel(strategy, trade_date, stks):
    with open('sel/' + strategy + '_' + trade_date + '.sel', 'wb') as f:
        f.write(int_to_bytes(len(stks)))
        f.write(bytes([0]))
        for stk in stks:
            xs = stk.code.split('.')
            if xs[1] == 'SH':
                f.write(bytes([0x07, 0x11]))
                f.write(bytes(xs[0], encoding='utf-8'))
            else:
                f.write(bytes([0x07, 0x21]))
                f.write(bytes(xs[0], encoding='utf-8'))

def show_recommended(trade_date):
    
    updator = Updator()
    updator.update_all_daily_by_trade_date(trade_date)

    sf = StrategyFactory(repo)
    results = sf.do_strategy(trade_date)

    for s in results:
        print("=== " + trade_date + " ===")
        print("=== " + s + " ===")
        stks = sort_by_ma20_diff(results[s])
        for stk in stks:
            show_stock_result(trade_date, stk)
        # updator.save_results(trade_date, s, stks)
        write_sel(s, trade_date, stks)
        # show_stock_stat_result(stks)

if __name__ == '__main__':

    trade_date = '20210910'
    show_recommended(trade_date)
    
    # dates = repo.get_all_trade_dates_between('000001.SZ', '20210101', '20210801')
    # for date in dates:
    #     show_recommended(date)
