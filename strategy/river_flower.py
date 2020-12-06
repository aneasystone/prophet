from strategy import Strategy

class RiverFlower(Strategy):
    
    # check if today's ma is open
    def is_ma_open(self, mas):
        return mas[0] > mas[1] and mas[1] > mas[2]

    # check if the ma's trend is opening
    def is_ma_opening(self):
        if not self.is_ma_open([self.stk.ma5[-1], self.stk.ma10[-1], self.stk.ma20[-1]]):
            return False
        mix_count = 0
        for i in range(2, 12):
            if not self.is_ma_open([self.stk.ma5[-i], self.stk.ma10[-i], self.stk.ma20[-i]]):
                mix_count += 1
        return mix_count > 3

    # check if the closed price is upon one or more ma lines
    def is_close_upon_ma(self):
        today_open = self.stk.prices['open'].values[-1]
        today_close = self.stk.prices['close'].values[-1]
        upon_count = 0
        mas = [self.stk.ma5[-1], self.stk.ma10[-1], self.stk.ma20[-1]]
        for ma in mas:
            if today_open < ma and today_close > ma:
                upon_count += 1
        return upon_count > 1

    # rate +5%
    def is_very_red(self):
        today_close = self.stk.prices['close'].values[-1]
        yesterday_close = self.stk.prices['close'].values[-2]
        rate = (today_close - yesterday_close) / yesterday_close * 100
        return rate >= 5

    # check if the kline state is The flower on river
    # a positive kline upon one or more ma lines (moving average)
    def is_river_flower(self):
        return self.is_very_red() and self.is_close_upon_ma() and self.is_ma_opening()

    def is_recommended(self):
        return self.is_river_flower()
            