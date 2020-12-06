import traceback
from stock import Stock
from repository import Repository
from updator import Updator
from strategy_factory import StrategyFactory

if __name__ == '__main__':
    trade_date = '20201203'
    updator = Updator()
    updator.update_all_daily_by_trade_date(trade_date)

    sf = StrategyFactory()
    results = {}
    repo = Repository()
    stocks = repo.get_all_stocks()
    for ss in stocks:
        try:
            # for debug
            # if s['ts_code'] != '603617.SH':
            #     continue
            
            stk = Stock(ss['name'], ss['ts_code'], trade_date)
            print(stk.name + " " + stk.code)
            if stk.init():
                strategies = sf.match_strategies(stk)
                if len(strategies) > 0:
                    print(stk.name + " " + stk.code + " " + str(stk.close) + " " + ",".join(strategies))
                for s in strategies:
                    if s not in results:
                        results[s] = list()
                    results[s].append(stk)
        except:
            # traceback.print_exc()
            pass

    print("------------------------")
    print("------- RESULTS --------")
    print("------------------------")
    for s in results:
        print(s + ":")
        for stk in results[s]:
            print(stk.name + " " + stk.code + " " + str(stk.close))
