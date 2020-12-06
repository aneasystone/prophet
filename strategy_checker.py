import traceback
from stock import Stock
from repository import Repository
from strategy_factory import StrategyFactory

if __name__ == '__main__':

    all_statistics = []

    sf = StrategyFactory()
    repo = Repository()
    stocks = repo.get_all_stocks()
    for ss in stocks:
        try:
            # for debug
            strategy = 'MACDGOLDCROSS'
            if ss['ts_code'] != '603613.SH':
                continue

            dates = repo.get_all_trade_dates(ss['ts_code'])
            for date in dates:
                try:
                    stk = Stock(ss['name'], ss['ts_code'], date)
                    if stk.init():
                        strategies = sf.match_strategies(stk)
                        for s in strategies:
                            if s == strategy:
                                statistics = strategies[s].get_profit_statistics()
                                all_statistics.append(statistics)
                                print("%s %s %s" % (stk.name, stk.code, date))
                                for stat in statistics:
                                    print("%.2f" % stat, end=" ")
                                print("")
                except:
                    # traceback.print_exc()
                    pass
        except:
            # traceback.print_exc()
            pass

    print("-----------------------")
    for d in range(0, 30):
        sum = 0
        count = 0
        for stat in all_statistics:
            sum += stat[d]
            if stat[d] > 0:
                count += 1
        print("%d: %.2f %.2f" % (d+1, count/len(all_statistics), sum/len(all_statistics)))
