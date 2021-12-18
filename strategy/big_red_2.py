from strategy import Strategy

class BigRed2(Strategy):
    
    def is_very_red(self):
        close_1 = self.stk.prices['close'].values[-1]
        close_3 = self.stk.prices['close'].values[-3]
        close_4 = self.stk.prices['close'].values[-4]
        rate_1_3 = (close_1 - close_3) / close_3 * 100
        rate_1_4 = (close_1 - close_4) / close_4 * 100
        return rate_1_3 >= 14 and rate_1_4 < 21

    def is_recommended(self):
        return self.is_very_red()
            