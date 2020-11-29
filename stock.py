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
    features = ''

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

    # check if macd metric is low
    def is_low_macd(self):
        dif = self.macd[0]
        dea = self.macd[1]
        count = 0
        for i in range(1, 11):
            if dif[-i] < dea[-i]:
                count += 1
        return count >= 8

    # get today's body, head and tail
    def get_body_head_tail(self):
        _open = self.prices['open'].values[-1]
        _close = self.prices['close'].values[-1]
        _high = self.prices['high'].values[-1]
        _low = self.prices['low'].values[-1]
        if _open > _close:
            body = _open - _close
            tail = _close - _low
            head = _high - _open
        else:
            body = _close - _open
            tail = _open - _low
            head = _high - _close
        return body, tail, head

    # check if today's kline is hammer
    def is_hammer(self):
        body, tail, head = self.get_body_head_tail()
        if body == 0:
            body = 0.1
        if head == 0:
            head = 0.1
        return tail / body > 2 and tail / head > 3

    # check if today's kline is swallow or pierce
    def is_swallow_or_pierce(self):
        today_open = self.prices['open'].values[-1]
        today_close = self.prices['close'].values[-1]
        yesterday_open = self.prices['open'].values[-2]
        yesterday_close = self.prices['close'].values[-2]
        if today_close > today_open and yesterday_close < yesterday_open and today_open < yesterday_close:
            if today_close > yesterday_open:
                return 'SWALLOW'
            if yesterday_open - today_close < today_close - yesterday_close:
                return 'PIERCE'
        return ''

    # check if today's kline is pierce
    def is_pierce(self):
        today_open = self.prices['open'].values[-1]
        today_close = self.prices['close'].values[-1]
        yesterday_open = self.prices['open'].values[-2]
        yesterday_close = self.prices['close'].values[-2]
        return today_close > today_open and yesterday_close < yesterday_open and today_close > yesterday_close

    # check if today's low price is the lowest in recent days
    def is_lowest(self):
        _low = self.prices['low'].values[-1]
        count = 0
        for i in range(2, 15):
            if self.prices['low'].values[-i] <= _low:
                count += 1
        return count <= 2

    # check if macd meets gold cross
    def is_macd_gold_cross(self):
        _dif = self.macd[0]
        _dea = self.macd[1]
        _macd = self.macd[2]
        for i in range(2, 11):
            if _dif[-i] > _dea[-i]:
                return False
        return _dif[-1] > _dea[-1] and _macd[-1] > 0

    # check if the head is very long
    def is_head_very_long(self):
        body, tail, head = self.get_body_head_tail()
        return head > body
        
    # is close > open
    def is_red(self):
        _open = self.prices['open'].values[-1]
        _close = self.prices['close'].values[-1]
        return _close > _open

    # check if tomorrow's open price can profit
    def can_profit(self):
        after_prices = self.repo.get_all_prices_after(self.code, self.date)
        tomorrow_open = after_prices['open'].values[0]
        high1 = after_prices['high'].values[1]
        high2 = after_prices['high'].values[2]
        high3 = after_prices['high'].values[3]
        return high1 > tomorrow_open or high2 > tomorrow_open or high3 > tomorrow_open        

    # check if this stock is recommended
    # First, macd is low
    # Second, hammer or swallow or pierce
    def is_recommended(self):
        
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
        self.close = self.prices['close'].values[-1]

        # TODO One day earlier
        if self.is_macd_gold_cross() and self.is_red() and not self.is_head_very_long():
            self.features = 'GOLDCROSS'
            return True

        if not self.is_low_macd():
            return False
        
        if self.is_lowest():
            if self.is_hammer():
                self.features = 'HAMMER'
            else:
                self.features = self.is_swallow_or_pierce()

        return True
