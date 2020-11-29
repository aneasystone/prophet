import traceback
from stock import Stock
from repository import Repository

if __name__ == '__main__':

    all_statistics = []

    repo = Repository()
    stocks = repo.get_all_stocks()
    for s in stocks:
        try:
            # for debug
            # if s['ts_code'] != '000001.SZ':
            #     continue
            dates = repo.get_all_trade_dates(s['ts_code'])
            for date in dates:
                try:
                    ss = Stock(s['name'], s['ts_code'], date)
                    if ss.is_recommended() and ss.features == 'HAMMER':
                        statistics = ss.get_profit_statistics()
                        all_statistics.append(statistics)
                        print("%s %s %s" % (ss.name, ss.code, date))
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
