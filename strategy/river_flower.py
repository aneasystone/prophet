from strategy import Strategy

class RiverFlower(Strategy):
    
    # check if ma is open
    def is_ma_open(self, ma5, ma10, ma20):
        # print("%.2f %.2f %.2f" % (ma5, ma10, ma20))
        is_open = ma5 > ma10 and ma10 > ma20
        if not is_open:
            return False
        # open is big
        d_5_10 = abs((ma5-ma10)/ma10)
        d_10_20 = abs((ma10-ma20)/ma20)
        # print("%.4f %.4f" % (d_5_10, d_10_20))
        return d_5_10 > 0.01 and d_10_20 > 0.005

    # check if ma is close
    def is_ma_close(self, ma5, ma10, ma20):
        # print("%.2f %.2f %.2f" % (ma5, ma10, ma20))
        # close is small
        d_5_10 = abs((ma10-ma5)/ma5)
        d_10_20 = abs((ma20-ma10)/ma10)
        # print("%.4f %.4f" % (d_5_10, d_10_20))
        return d_5_10 < 0.01 and d_10_20 < 0.01

    # check if the ma's trend is opening
    def is_ma_opening(self):

        # ma is open today
        if not self.is_ma_open(self.stk.ma5[-1], self.stk.ma10[-1], self.stk.ma20[-1]):
            return False
        
        # ma is close in last 20 days
        for i in range(2, 22):
            if self.is_ma_close(self.stk.ma5[-i], self.stk.ma10[-i], self.stk.ma20[-i]):
                return True
        return False

    # check if the closed price is upon ma5
    def is_close_upon_ma(self):
        today_close = self.stk.prices['close'].values[-1]
        return today_close > self.stk.ma5[-1]

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
            