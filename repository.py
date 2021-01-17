import pandas as pd
from sqlalchemy import create_engine

engine = create_engine('mysql+pymysql://root:123456@localhost:3306/stock')

# Using SQLAlchemy
# https://www.liaoxuefeng.com/wiki/897692888725344/955081460091040

class Repository:

    prices_cache = {}

    # get all stocks
    def get_all_stocks(self):
        sql = "SELECT * FROM stock_basic"
        df = pd.read_sql(sql=sql, con=engine)
        return df.to_dict("records")

    # get basic of this stock
    def get_stock_basic(self, code):
        sql = "SELECT * FROM stock_basic WHERE ts_code = '" + code + "'"
        df = pd.read_sql(sql=sql, con=engine)
        return df.to_dict("records")[0]

    # get all prices of this stock
    def get_all_prices(self, code):
        if code in self.prices_cache:
            return self.prices_cache[code]
        sql = "SELECT * FROM daily WHERE ts_code = '" + code + "' ORDER BY trade_date"
        df = pd.read_sql(sql=sql, con=engine)
        self.prices_cache[code] = df
        return df

    # get all prices of this stock before someday
    def get_all_prices_before(self, code, date):
        prices = self.get_all_prices(code)
        return prices[prices['trade_date'] <= date]

    # get all prices of this stock after someday
    def get_all_prices_after(self, code, date):
        prices = self.get_all_prices(code)
        return prices[prices['trade_date'] > date]

    # get all trade dates of this stock
    def get_all_trade_dates(self, code):
        sql = "SELECT trade_date FROM daily WHERE ts_code = '" + code + "' ORDER BY trade_date"
        df = pd.read_sql(sql=sql, con=engine)
        return df['trade_date'].values

    # get all trade dates of this stock after someday
    def get_all_trade_dates_after(self, code, date):
        sql = "SELECT trade_date FROM daily WHERE ts_code = '" + code + "' AND trade_date >= '" + date + "' ORDER BY trade_date"
        df = pd.read_sql(sql=sql, con=engine)
        return df['trade_date'].values

    # get all trade dates of this stock between two days
    def get_all_trade_dates_between(self, code, begin, end):
        sql = "SELECT trade_date FROM daily WHERE ts_code = '" + code + "' AND trade_date >= '" + begin + "' AND trade_date < '" + end + "' ORDER BY trade_date"
        df = pd.read_sql(sql=sql, con=engine)
        return df['trade_date'].values
