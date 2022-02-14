from strategy import Strategy

class BigRed(Strategy):
    
    # close price over ma5
    def is_over_ma5(self, i):
        _close = self.stk.prices['close'].values[i]
        _ma5 = self.stk.ma5[i]
        return _close > _ma5

    # ma is open
    def is_ma_open(self, i):
        level = self.get_stock_level(i)
        return level < 3

    # rate +7%
    def is_very_red(self, i):
        today_close = self.stk.prices['close'].values[i]
        yesterday_close = self.stk.prices['close'].values[i-1]
        rate = (today_close - yesterday_close) / yesterday_close * 100
        return rate > 7

    def is_recommended_at(self, i):
        return self.is_very_red(i) and self.is_ma_open(i) and self.is_over_ma5(i)

    def is_highest_in_120(self, i):
        today_close = self.stk.prices['close'].values[i]
        for day in range(1, 120):
            _close = self.stk.prices['close'].values[i-day]
            if _close*0.9 > today_close:
                return False
        return True

    def is_first_big_red(self):
        is_recommended_today = self.is_recommended_at(-1) and self.is_highest_in_120(-1)
        # print(is_recommended_today)
        if is_recommended_today:
            for i in range(2, 60):
                if self.is_recommended_at(-i):
                    # print(i)
                    return False
            return True
        return False

    def is_recommended(self):
        return self.is_first_big_red()
