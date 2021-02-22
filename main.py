import traceback
from stock import Stock
from repository import Repository
from updator import Updator
from strategy_factory import StrategyFactory

def get_stk_features(stk):
    return ", ".join(stk.features)

def sort_by_features(stks):
    return sorted(stks, key=get_stk_features)

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
        updator.save_results(trade_date, s, stks)

if __name__ == '__main__':

    trade_date = '20210222'
    show_recommended(trade_date)

    # repo = Repository()
    # dates = repo.get_all_trade_dates_between('000001.SZ', '20210101', '20210301')
    # for date in dates:
    #     show_recommended(date)
