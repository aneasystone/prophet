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

    # get all prices of this stock
    def get_all_prices(self, code):
        if code in self.prices_cache:
            return self.prices_cache[code]
        sql = "SELECT * FROM daily WHERE ts_code = '" + code + "'"
        df = pd.read_sql(sql=sql, con=engine)
        prices = df.sort_values(by = "trade_date", ascending = True)
        self.prices_cache[code] = prices
        return prices

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
        sql = "SELECT trade_date FROM daily WHERE ts_code = '" + code + "'"
        df = pd.read_sql(sql=sql, con=engine)
        df.sort_values(by = "trade_date", ascending = False)
        return df['trade_date'].values
