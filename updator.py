import traceback
import pandas as pd
from sqlalchemy import create_engine
from repository import Repository
from tushare_util import TuShareUtil

engine = create_engine('mysql+pymysql://root:123456@localhost:3306/stock')

class Updator:
    '''数据更新'''

    def update_stock_basic(self):
        '''更新 stock_basic 表，股票的基本信息'''
        engine.execute('TRUNCATE TABLE stock_basic')
        df = TuShareUtil.get_all_stock_basic()
        df.to_sql('stock_basic', engine, index=False, if_exists='append', chunksize=5000)
        return df

    def update_daily(self, trade_date):
        '''更新日线行情'''
        df = TuShareUtil.get_daily(trade_date)
        df.to_sql('daily', engine, index=False, if_exists='append', chunksize=5000)
        return df

    def update_daily_basic(self, trade_date):
        '''更新每日基本面指标'''
        df = TuShareUtil.get_daily_basic(trade_date)
        df.to_sql('daily_basic', engine, index=False, if_exists='append', chunksize=5000)
        return df

    def update_money_flow(self, trade_date):
        '''更新资金流向'''
        df = TuShareUtil.get_money_flow(trade_date)
        df.to_sql('money_flow', engine, index=False, if_exists='append', chunksize=5000)
        return df
