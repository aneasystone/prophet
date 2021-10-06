from strategy import Strategy

class MaOpenFour(Strategy):

    def is_open(self, i):
        # print(i, self.stk.ma5[i], self.stk.ma10[i], self.stk.ma20[i], self.stk.ma30[i])
        return (self.stk.ma10[i] > self.stk.ma20[i] > self.stk.ma30[i] and self.stk.ma5[i] > self.stk.ma20[i]) or (self.stk.ma5[i] > self.stk.ma10[i] > self.stk.ma20[i] and self.stk.ma10[i] > self.stk.ma30[i])

    def is_very_red(self, i):
        today_close = self.stk.prices['close'].values[i]
        yesterday_close = self.stk.prices['close'].values[i-1]
        rate = (today_close - yesterday_close) / yesterday_close * 100
        return rate >= 5

    def get_ma_open_days(self, i):
        day = -i
        while True:
            if self.is_open(-day):
                day += 1
                continue
            break
        return day + i
    
    def get_very_red_days(self, i):
        very_red_days = 0
        for day in range(-i, -i+30):
            if self.is_very_red(-day):
                very_red_days += 1
        return very_red_days

    def is_over_ma10(self, i):
        _low = self.stk.prices['low'].values[i]
        _ma10 = self.stk.ma10[i]
        return _low > _ma10
    
    def is_recommended_at(self, i):
        ma_open_days = self.get_ma_open_days(i)
        very_red_days = self.get_very_red_days(i)
        # print(i, ma_open_days, very_red_days, self.is_over_ma10(i))
        return ma_open_days >= 1 and very_red_days >= 1 and self.is_over_ma10(i)

    def is_recommended(self):
        if not self.is_recommended_at(-1):
            return False            
        for day in range(2, 32):
            if self.is_recommended_at(-day):
                return False
        return True
