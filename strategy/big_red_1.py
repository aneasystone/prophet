from strategy import Strategy

class BigRed1(Strategy):
    
    def is_very_red(self):
        close_1 = self.stk.prices['close'].values[-1]
        close_2 = self.stk.prices['close'].values[-2]
        close_3 = self.stk.prices['close'].values[-3]
        rate_1_2 = (close_1 - close_2) / close_2 * 100
        rate_1_3 = (close_1 - close_3) / close_3 * 100
        return rate_1_2 >= 7 and rate_1_3 < 14

    def is_recommended(self):
        return self.is_very_red()
            