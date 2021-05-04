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

def get_highest_price_after_trade_date(trade_date, stk):
    after_prices = repo.get_all_prices_after(stk.code, trade_date)
    highest = -9999
    for high in after_prices['high'].values:
        if high > highest:
            highest = high
    return highest

def show_stock_result(trade_date, stk):
    highest = get_highest_price_after_trade_date(trade_date, stk)
    if highest == -9999:
        info = "{0:{5}<10}\t{1:<10}\t{2:<10}\t{3:{5}<10}\t{4}".format(
            stk.name, stk.code, str(stk.close), stk.industry, ", ".join(stk.features), chr(12288))
    else:
        info = "{0:{5}<10}\t{1:<10}\t{2:<10}\t{3:{5}<10}\t{4}\t{6}({7})".format(
            stk.name, stk.code, str(stk.close), stk.industry, ", ".join(stk.features), chr(12288), highest, "%.2f%%" % ((highest/stk.close-1)*100))
    if highest == -9999:
        print(info)
    elif highest > stk.close:
        print_red(info)
    else:
        print_green(info)

def get_stk_features(stk):
    return ", ".join(stk.features)

def sort_by_features(stks):
    return sorted(stks, key=get_stk_features)

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
        stks = sort_by_features(results[s])
        for stk in stks:
            show_stock_result(trade_date, stk)
        # updator.save_results(trade_date, s, stks)
        write_sel(s, trade_date, stks)

if __name__ == '__main__':

    trade_date = '20210430'
    show_recommended(trade_date)
    
    # dates = repo.get_all_trade_dates_between('000001.SZ', '20210101', '20210501')
    # for date in dates:
    #     show_recommended(date)
