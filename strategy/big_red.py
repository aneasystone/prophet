from strategy import Strategy

class BigRed(Strategy):
    
    # close price over ma5
    def is_over_ma5(self, i):
        _close = self.stk.prices['close'].values[i]
        _ma5 = self.stk.ma5[i]
        return _close > _ma5

    def get_stock_level(self, i):
        arr = [self.stk.ma30[i], self.stk.ma20[i], self.stk.ma10[i], self.stk.ma5[i]]
        steps = 0
        n = len(arr)
        for i in range(n-1):
            for j in range(0, n-i-1):
                if arr[j] > arr[j + 1] :
                    arr[j], arr[j + 1] = arr[j + 1], arr[j]
                    steps += 1
        return steps

    # ma is open
    def is_ma_open(self, i):
        level = self.get_stock_level(self, i)
        return level < 3

    # rate +7%
    def is_very_red(self, i):
        today_close = self.stk.prices['close'].values[i]
        yesterday_close = self.stk.prices['close'].values[i-1]
        rate = (today_close - yesterday_close) / yesterday_close * 100
        return rate >= 7

    def is_recommended_at(self, i):
        return self.is_very_red(i) and self.is_ma_open(i) and self.is_over_ma5(i)

    def is_recommended(self):
        is_recommended_today = self.is_recommended_at(-1)
        if is_recommended_today:
            for i in range(2, 60):
                if self.is_recommended_at(-i):
                    return False
            return True
        return False
