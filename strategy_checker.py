import traceback
from stock import Stock
from repository import Repository
from strategy_factory import StrategyFactory

if __name__ == '__main__':

    all_statistics = {}

    sf = StrategyFactory()
    repo = Repository()
    stocks = repo.get_all_stocks()
    for ss in stocks:
        try:
            # for debug
            # if ss['ts_code'] != '002594.SZ':
            #      continue

            dates = repo.get_all_trade_dates(ss['ts_code'])
            for date in dates:
                try:
                    stk = Stock(ss['name'], ss['ts_code'], date)
                    if stk.init():
                        strategies = sf.match_strategies(stk)
                        for s in strategies:
                            # for debug
                            # if s != 'RED':
                            #     continue
                            
                            statistics = strategies[s].get_profit_statistics()
                            if s not in all_statistics:
                                all_statistics[s] = list()
                            print("%s %s %s %s" % (stk.name, stk.code, date, s))
                            if statistics:
                                for stat in statistics:
                                    print("%.2f" % stat, end=" ")
                                print("")
                                all_statistics[s].append(statistics)
                            else:
                                print("BUY MISS")
                except:
                    # traceback.print_exc()
                    pass
        except:
            # traceback.print_exc()
            pass

    print("-----------------------")
    for s in all_statistics:
        print(s + " ", end=" ")
        for d in range(0, 30):
            sum = 0
            for stat in all_statistics[s]:
                sum += stat[d]
            print("%.2f" % (100*sum/len(all_statistics[s])), end=" ")
        print("")
