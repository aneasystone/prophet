import talib
import numpy as np
from repository import Repository

# How to install talib
# https://blog.csdn.net/weixin_40327641/article/details/81076438

class Stock:

    repo = Repository()
    
    name = ''
    code = ''
    date = ''
    industry = ''

    features = None

    prices = None
    close = 0
    average_amplitude = None
    money_flow = None

    macd = None
    pre_macd = None
    
    ma5 = None
    ma10 = None
    ma20 = None
    ma30 = None
    pre_ma5 = None
    pre_ma10 = None
    pre_ma20 = None

    def __init__(self, name, code, date):
        self.name = name
        self.code = code
        self.date = date
        self.features = []
        
    # get all prices of this stock
    def get_all_prices(self):
        return self.repo.get_all_prices_before(self.code, self.date)

    # get all money flow of this stock
    def get_all_money_flow(self):
        return self.repo.get_all_money_flow_before(self.code, self.date)

    # get macd metric of this stock
    def get_macd(self):
        close = self.prices["close"].values
        return talib.MACD(close, fastperiod = 12, slowperiod = 26, signalperiod = 9)

    # get pre macd metric of this stock, as is, if tomorrow's price rise of 7 days average amplitude
    def get_pre_macd(self):
        close = self.prices["close"].values
        possible_high = close[-1] * (1 + self.average_amplitude / 2)
        close = np.append(close, possible_high)
        return talib.MACD(close, fastperiod = 12, slowperiod = 26, signalperiod = 9)

    # get week macd metric of this stock
    def get_week_macd(self):
        close = self.prices["close"].values
        week_close = close[len(close)%5-1::5]
        return talib.MACD(week_close, fastperiod = 12, slowperiod = 26, signalperiod = 9)

    # get ma metric of this stock
    def get_ma(self, timeperiod):
        close = self.prices["close"].values
        return talib.SMA(close, timeperiod = timeperiod)

    # get pre ma metric of this stock, as is, if tomorrow's price rise of 7 days average amplitude
    def get_pre_ma(self, timeperiod):
        close = self.prices["close"].values
        possible_high = close[-1] * (1 + self.average_amplitude / 2)
        close = np.append(close, possible_high)
        return talib.SMA(close, timeperiod = timeperiod)

    # get week ma metric of this stock
    def get_week_ma(self, timeperiod):
        close = self.prices["close"].values
        week_close = close[len(close)%5-1::5]
        return talib.SMA(week_close, timeperiod = timeperiod)

    # get average amplitude
    def get_average_amplitude(self, days):
        amplitude = 0
        for i in range(1, days + 1):
            _high = self.prices['high'].values[-i]
            _low = self.prices['low'].values[-i]
            _pre_close = self.prices['pre_close'].values[-i]
            amplitude += (_high - _low) / _pre_close
        return amplitude / days

    # get the price at specified gear
    def get_gear_price(self, gear):
        return self.close + self.get_gear_delta() * gear

    # get the gear delta
    def get_gear_delta(self):
        return self.close * self.average_amplitude * 0.25

    # Initialize price information
    def init(self):

        # ignore these stocks
        if self.code.startswith('30'):
            return False
        if self.code.startswith('68'):
            return False
        if self.code.startswith('003'):
            return False
        if 'ST' in self.name:
            return False
        
        basic = self.repo.get_stock_basic(self.code)
        if basic:
            self.industry = basic['industry'] if basic['industry'] else '--'
            self.name = basic['name']

        self.prices = self.get_all_prices()
        self.close = self.prices['close'].values[-1]
        self.average_amplitude = self.get_average_amplitude(7)
        self.money_flow = self.get_all_money_flow()

        if self.date != self.prices['trade_date'].values[-1]:
            # 无今天的价格信息，可能被停牌
            return False

        self.macd = self.get_macd()
        self.pre_macd = self.get_pre_macd()
        self.week_macd = self.get_week_macd()
        
        self.ma5 = self.get_ma(5)
        self.ma10 = self.get_ma(10)
        self.ma20 = self.get_ma(20)
        self.ma30 = self.get_ma(30)
        self.pre_ma5 = self.get_pre_ma(5)
        self.pre_ma10 = self.get_pre_ma(10)
        self.pre_ma20 = self.get_pre_ma(20)
        self.week_ma5 = self.get_week_ma(5)
        self.week_ma10 = self.get_week_ma(10)
        self.week_ma20 = self.get_week_ma(20)
        
        return True
