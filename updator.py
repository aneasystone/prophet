import traceback
import tushare as ts
import pandas as pd
from sqlalchemy import create_engine
from repository import Repository

# TuShare API Document
# https://waditu.com/document/2?doc_id=27

pro = ts.pro_api("a5a9fbdbf64462122f1c3281c54b3bd3fa0982e54c20c44977b2d72f")
engine = create_engine('mysql+pymysql://root:123456@localhost:3306/stock')

class Updator:

    # update all stocks
    def update_all_stock_basic(self):
        df = pro.query('stock_basic', exchange='', list_status='L', fields='ts_code,symbol,name,area,industry,list_date')
        df.to_sql('stock_basic', engine, index=False, if_exists='replace', chunksize=5000)

    # update all prices of this stock
    def update_all_daily_by_code(self, code):
        df = pro.daily(ts_code = code)
        df.to_sql('daily', engine, index=False, if_exists='append', chunksize=5000)

    # update the price of all stock of someday
    def update_all_daily_by_trade_date(self, trade_date):
        sql = "SELECT * FROM daily WHERE trade_date = '" + trade_date + "'"
        df = pd.read_sql(sql=sql, con=engine)
        if df.empty:
            # print('Data is empty, update by tushare api')
            df = pro.daily(trade_date = trade_date)
            df.to_sql('daily', engine, index=False, if_exists='append', chunksize=5000)
        else:
            # print('Data is not empty, ignore updating ...')
            pass

    def save_results(self, trade_date, strategy, stks):
        rs = []
        for stk in stks:
            rs.append([trade_date, stk.code, strategy, ", ".join(stk.features)])
        df = pd.DataFrame(rs, columns=['trade_date', 'ts_code', 'strategy', 'features'])
        df.to_sql('results', engine, index=False, if_exists='append', chunksize=5000)

if __name__ == '__main__':
    
    updator = Updator()
    repo = Repository()

    first_run = False

    if first_run:
        # Run this in the first time
        updator.update_all_stock_basic()
        stocks = repo.get_all_stocks()
        for s in stocks:
            try:
                # for debug
                # if s['ts_code'] != '603110.SH':
                #     continue
                print(s['name'] + " " + s['ts_code'])
                updator.update_all_daily_by_code(s['ts_code'])
            except:
                traceback.print_exc()
    else:
        # Run this everyday
        updator.update_all_daily_by_trade_date('20201127')
