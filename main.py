import traceback
from stock import Stock
from repository import Repository
from updator import Updator
from strategy_factory import StrategyFactory

def show_strategy_check_result(stk, stragegy):
    
    all_statistics = []
    try:
        sf = StrategyFactory()
        repo = Repository()
        dates = repo.get_all_trade_dates(stk.code)
        for date in dates:
            try:
                stk = Stock(stk.name, stk.code, date)
                if stk.init():
                    strategies = sf.match_strategies(stk)
                    statistics = strategies[stragegy].get_profit_statistics()
                    all_statistics.append(statistics)
            except:
                # traceback.print_exc()
                pass
    except:
        # traceback.print_exc()
        pass

    print("-------- PROFIT RATE ---------------")
    for d in range(0, 30):
        sum = 0
        for stat in all_statistics:
            sum += stat[d]
        print("%.2f" % (100*sum/len(all_statistics)), end=" ")
    print("")
    print("------------------------------------")

if __name__ == '__main__':
    trade_date = '20201209'
    updator = Updator()
    updator.update_all_daily_by_trade_date(trade_date)

    sf = StrategyFactory()
    results = {}
    repo = Repository()
    stocks = repo.get_all_stocks()
    for ss in stocks:
        try:
            # for debug
            # if ss['ts_code'] != '603976.SH':
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
            show_strategy_check_result(stk, s)
