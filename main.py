import traceback
from stock import Stock
from repository import Repository
from updator import Updator
from strategy_factory import StrategyFactory

def get_stk_features(stk):
    return ", ".join(stk.features)

def sort_by_features(stks):
    return sorted(stks, key=get_stk_features)

def int_to_bytes(x: int) -> bytes:
    return x.to_bytes((x.bit_length() + 7) // 8, 'little')

def write_sel(strategy, trade_date, stks):
    with open(strategy + '_' + trade_date + '.sel', 'wb') as f:
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

    sf = StrategyFactory()
    results = sf.do_strategy(trade_date)

    for s in results:
        print("=== " + trade_date + " ===")
        print("=== " + s + " ===")
        stks = sort_by_features(results[s])
        for stk in stks:
            print("{0:{5}<10}\t{1:<10}\t{2:<10}\t{3:{5}<10}\t{4}".format(
                stk.name, stk.code, str(stk.close), stk.industry, ", ".join(stk.features), chr(12288)))
        # updator.save_results(trade_date, s, stks)
        # write_sel(s, trade_date, stks)

if __name__ == '__main__':

    trade_date = '20210226'
    show_recommended(trade_date)
    
    # repo = Repository()
    # dates = repo.get_all_trade_dates_between('000001.SZ', '20210101', '20210301')
    # for date in dates:
    #     show_recommended(date)
