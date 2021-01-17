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
    trade_date = '20210115'
    updator = Updator()
    updator.update_all_daily_by_trade_date(trade_date)

    sf = StrategyFactory()
    results = sf.do_strategy(trade_date)
    
    print("------------------------")
    print("------- RESULTS --------")
    print("------------------------")
    for s in results:
        print(s + ":-------------------------------------------------------")
        for stk in results[s]:
            average_amplitude = stk.average_amplitude
            b1 = stk.get_gear_price(-1)
            b2 = stk.get_gear_price(-2)
            b3 = stk.get_gear_price(-3)
            b4 = stk.get_gear_price(-4)
            u1 = stk.get_gear_price(1)
            u2 = stk.get_gear_price(2)
            u3 = stk.get_gear_price(3)
            u4 = stk.get_gear_price(4)
            delta = "%.2f" % (stk.close * average_amplitude * 0.25)

            print("{0:{6}<10}\t{1:<10}\t{2:<10}\t{3:<10}\t{4:{6}<10}\t{5}".format(
                stk.name, stk.code, str(stk.close), delta, stk.industry, ", ".join(stk.features), chr(12288)))
            print("%.2f\t%.2f\t%.2f\t%.2f\t%.2f\t%.2f\t%.2f\t%.2f\t%.2f" % (
                b4, b3, b2, b1, stk.close, u1, u2, u3, u4
            ))
            # show_strategy_check_result(stk, s)
