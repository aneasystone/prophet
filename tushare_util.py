import imp


import datetime
import tushare as ts

pro = ts.pro_api("a5a9fbdbf64462122f1c3281c54b3bd3fa0982e54c20c44977b2d72f")

class TuShareUtil:
    ''' TuShare 工具类，封装 TuShare 常用接口
    
    参考文档：
    https://waditu.com/document/2?doc_id=27
    '''

    def get_all_trade_dates_after(start_date):
        '''交易日历'''
        end_date = datetime.date.today().strftime('%Y%m%d')
        df = pro.trade_cal(exchange='', start_date=start_date, end_date=end_date)
        return df

    def get_all_trade_dates_between(start_date, end_date):
        '''交易日历'''
        df = pro.trade_cal(exchange='', start_date=start_date, end_date=end_date)
        return df

    def get_all_stock_basic():
        '''股票列表，包括：名称、代码、地区、行业'''
        df = pro.stock_basic(exchange='', list_status='L', fields='ts_code,symbol,name,area,industry,list_date')
        return df
    
    def get_daily(trade_date):
        '''日线行情，包括：开盘价、收盘价、最高价、最低价'''
        df = pro.daily(trade_date=trade_date)
        return df

    def get_daily_basic(trade_date):
        '''每日基本面指标，包括：换手、量比、市盈率、股本、股息、市值'''
        df = pro.daily_basic(trade_date=trade_date)
        return df

    def get_money_flow(trade_date):
        '''每日资金流向'''
        df = pro.moneyflow(trade_date=trade_date)
        return df

if __name__ == '__main__':
    
    trade_dates = TuShareUtil.get_all_trade_dates_between('20220101', '20220110')
    print(len(trade_dates))

    stocks = TuShareUtil.get_all_stock_basic()
    print(len(stocks))

    daily = TuShareUtil.get_daily('20220325')
    print(len(daily))

    daily_basic = TuShareUtil.get_daily_basic('20220325')
    print(len(daily_basic))

    money_flow = TuShareUtil.get_money_flow('20220325')
    print(len(money_flow))