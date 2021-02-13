import traceback
from stock import Stock
from repository import Repository
from updator import Updator
from strategy_factory import StrategyFactory

def print_green(s):
    print(f"\033[0;32;40m%s\033[0m" % (s))

def print_red(s):
    print(f"\033[0;31;40m%s\033[0m" % (s))

def show_recommended(trade_date):
    
    updator = Updator()
    updator.update_all_daily_by_trade_date(trade_date)

    repo = Repository()
    sf = StrategyFactory()
    results = sf.do_strategy(trade_date)

    for s in results:
        print("=== " + trade_date + " ===")
        print("=== " + s + " ===")
        red = 0
        green = 0
        for stk in results[s]:
            delta = '--'
            after_prices = repo.get_all_prices_after(stk.code, trade_date)
            if after_prices['open'].values.any():
                _close = after_prices['close'].values[0]
                _open = after_prices['open'].values[0]
                delta = "%.2f" % ((_close-_open)/_open*100)

            info = "{0:{6}<10}\t{1:<10}\t{2:<10}\t{3:{6}<10}\t{4}\t{5:<10}".format(
                stk.name, stk.code, str(stk.close), stk.industry, ", ".join(stk.features), delta, chr(12288))
            if '--' in delta:
                print(info)
            elif '-' in delta:
                print_green(info)
                green += 1
            else:
                print_red(info)
                red += 1
        print("=== %d red, %d green ===" % (red, green))

if __name__ == '__main__':

    trade_date = '20210210'
    show_recommended(trade_date)

    # repo = Repository()
    # dates = repo.get_all_trade_dates_between('000001.SZ', '20210101', '20210130')
    # for date in dates:
    #     show_recommended(date)
