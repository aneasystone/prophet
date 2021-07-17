from strategy import Strategy

class MaOpenFour(Strategy):

    def is_open(self, i):
        return self.stk.ma10[i] > self.stk.ma20[i] > self.stk.ma30[i] and self.stk.ma5[i] > self.stk.ma20[i]

    def is_very_red(self, i):
        today_close = self.stk.prices['close'].values[i]
        yesterday_close = self.stk.prices['close'].values[i-1]
        rate = (today_close - yesterday_close) / yesterday_close * 100
        return rate >= 7

    def get_ma_open_days(self):
        i = 1
        while True:
            if self.is_open(-i):
                i += 1
                continue
            break
        return i
    
    def get_very_red_days(self):
        very_red_days = 0
        for i in range(1, 30):
            if self.is_very_red(-i):
                very_red_days += 1
        return very_red_days

    def get_ma20_diff(self):
        _close = self.stk.prices['close'].values[-1]
        _ma20 = self.stk.ma20[-1]
        return (_ma20 - _close) / _close * 100
    
    def is_recommended(self):
        ma_open_days = self.get_ma_open_days()
        very_red_days = self.get_very_red_days()
        self.stk.features.append('MA_OPEN_%02d' % (ma_open_days))
        self.stk.features.append('RED_%02d' % (very_red_days))
        return ma_open_days >= 3 and very_red_days > 2 and self.get_ma20_diff() < 0
