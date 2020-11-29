import traceback
from stock import Stock
from repository import Repository
from updator import Updator

if __name__ == '__main__':

    trade_date = '20201127'
    updator = Updator()
    updator.update_all_daily_by_trade_date(trade_date)

    results = {}
    repo = Repository()
    stocks = repo.get_all_stocks()
    for s in stocks:
        try:
            # for debug
            # if s['ts_code'] != '002795.SZ':
            #     continue
            
            ss = Stock(s['name'], s['ts_code'], trade_date)
            print(ss.name + " " + ss.code)
            if ss.is_recommended() and ss.features:
                print(ss.name + " " + ss.code + " " + str(ss.close) + " " + ss.features)
                if ss.features not in results:
                    results[ss.features] = list()
                results[ss.features].append(ss)
        except:
            # traceback.print_exc()
            pass

    print("------------------------")
    print("------- RESULTS --------")
    print("------------------------")
    for features in results:
        print(features + ":")
        for ss in results[features]:
            print(ss.name + " " + ss.code + " " + str(ss.close) + " " + ss.features)
