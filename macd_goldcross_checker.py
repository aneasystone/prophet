import traceback
from stock import Stock
from repository import Repository

if __name__ == '__main__':

    repo = Repository()
    stocks = repo.get_all_stocks()
    for s in stocks:
        try:
            profit = 0
            nonprofit = 0
            dates = repo.get_all_trade_dates(s['ts_code'])
            for date in dates:
                try:
                    ss = Stock(s['name'], s['ts_code'], date)
                    if ss.is_recommended() and ss.features == 'GOLDCROSS':
                        if ss.can_profit():
                            print(ss.name + " " + ss.code + " " + date + " PROFIT")
                            profit += 1
                        else:
                            print(ss.name + " " + ss.code + " " + date + " NONPROFIT")
                            nonprofit += 1
                except:
                    # traceback.print_exc()
                    pass
            
            alls = profit + nonprofit
            if alls > 0:
                print("-----------------------------------")
                print("--- %s %s" % (s['name'], s['ts_code']))
                print("--- PROFIT RATE: %0.2f (%s/%s)" % (profit/alls, profit, alls))
                print("-----------------------------------")
        except:
            # traceback.print_exc()
            pass
