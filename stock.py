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

    prices = None
    macd = None
    pre_macd = None
    close = 0
    ma5 = None
    ma10 = None
    ma20 = None

    def __init__(self, name, code, date):
        self.name = name
        self.code = code
        self.date = date
        
    # get all prices of this stock
    def get_all_prices(self):
        return self.repo.get_all_prices_before(self.code, self.date)

    # get macd metric of this stock
    def get_macd(self):
        close = self.prices["close"].values
        return talib.MACD(close, fastperiod = 12, slowperiod = 26, signalperiod = 9)

    # get pre macd metric of this stock, as is, if tomorrow's price rise of 7 days average amplitude
    def get_pre_macd(self):
        average_amplitude = self.get_average_amplitude(7)
        close = self.prices["close"].values
        possible_high = close[-1] * (1 + average_amplitude / 2)
        close = np.append(close, possible_high)
        return talib.MACD(close, fastperiod = 12, slowperiod = 26, signalperiod = 9)

    # get ma metric of this stock
    def get_ma(self, timeperiod):
        close = self.prices["close"].values
        return talib.SMA(close, timeperiod = timeperiod)

    # get average amplitude
    def get_average_amplitude(self, days):
        amplitude = 0
        for i in range(1, days + 1):
            _high = self.prices['high'].values[-i]
            _low = self.prices['low'].values[-i]
            _pre_close = self.prices['pre_close'].values[-i]
            amplitude += (_high - _low) / _pre_close
        return amplitude / days

    # Initialize price information
    def init(self):

        # ignore these stocks
        if self.code.startswith('300'):
            return False
        if self.code.startswith('688'):
            return False
        if self.code.startswith('003'):
            return False
        if 'ST' in self.name:
            return False
        
        basic = self.repo.get_stock_basic(self.code)
        if basic:
            self.industry = basic['industry']

        self.prices = self.get_all_prices()
        self.macd = self.get_macd()
        self.pre_macd = self.get_pre_macd()
        self.ma5 = self.get_ma(5)
        self.ma10 = self.get_ma(10)
        self.ma20 = self.get_ma(20)
        self.close = self.prices['close'].values[-1]
        return True
