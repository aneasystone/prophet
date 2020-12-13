import traceback
from stock import Stock
from repository import Repository
from updator import Updator
from strategy_factory import StrategyFactory

def show_strategy_check_result(stk, stragegy):
    
    all_statistics = []
    miss_statistics = []
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
                    if statistics:
                        all_statistics.append(statistics)
                        miss_statistics.append(0)
                    else:
                        miss_statistics.append(1)
            except:
                # traceback.print_exc()
                pass
    except:
        # traceback.print_exc()
        pass

    print("-------- RISE RATE ---------------")
    if len(all_statistics) > 0:
        for d in range(0, 30):
            cnt = 0
            for stat in all_statistics:
                if stat[d] > 0:
                    cnt += 1
            print("%.2f" % (100*cnt/len(all_statistics)), end=" ")
        print("")
    else:
        print("NO DATA")
    print("-------- PROFIT RATE ---------------")
    if len(all_statistics) > 0:
        for d in range(0, 30):
            sum = 0
            for stat in all_statistics:
                sum += stat[d]
            print("%.2f" % (100*sum/len(all_statistics)), end=" ")
        print("")
    else:
        print("NO DATA")
    print("-------- MISS RATE ---------------")
    if len(miss_statistics) > 0:
        cnt = 0
        for stat in miss_statistics:
            if stat:
                cnt += 1
        print("%.2f" % (100*cnt/len(miss_statistics)))
    else:
        print("NO DATA")
    print("------------------------------------")

if __name__ == '__main__':
    trade_date = '20201211'
    updator = Updator()
    updator.update_all_daily_by_trade_date(trade_date)

    sf = StrategyFactory()
    results = {}
    repo = Repository()
    stocks = repo.get_all_stocks()
    for ss in stocks:
        try:
            # for debug
            # if ss['ts_code'] != '603277.SH':
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
        if s == 'AMPLITUDE':
            continue
        print(s + ":")
        for stk in results[s]:
            print(stk.name + " " + stk.code + " " + str(stk.close))
            show_strategy_check_result(stk, s)

    print("------------------------------")
    print("------- WATCH RESULTS --------")
    print("------------------------------")
    for s in results:
        if s != 'AMPLITUDE':
            continue
        print(s + ":")
        for stk in results[s]:
            print(stk.name + " " + stk.code + " " + str(stk.close))
            show_strategy_check_result(stk, s)
