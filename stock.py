import talib
from repository import Repository

# How to install talib
# https://blog.csdn.net/weixin_40327641/article/details/81076438

class Stock:

    repo = Repository()
    
    name = ''
    code = ''
    date = ''

    prices = None
    macd = None
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

    # get ma metric of this stock
    def get_ma(self, timeperiod):
        close = self.prices["close"].values
        return talib.SMA(close, timeperiod = timeperiod)

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
        
        self.prices = self.get_all_prices()
        self.macd = self.get_macd()
        self.ma5 = self.get_ma(5)
        self.ma10 = self.get_ma(10)
        self.ma20 = self.get_ma(20)
        self.close = self.prices['close'].values[-1]
        return True
