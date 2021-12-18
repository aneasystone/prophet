from strategy import Strategy

class BigRed4(Strategy):
    
    def is_very_red(self):
        close_1 = self.stk.prices['close'].values[-1]
        close_5 = self.stk.prices['close'].values[-5]
        rate_1_5 = (close_1 - close_5) / close_5 * 100
        return rate_1_5 >= 28

    def is_recommended(self):
        return self.is_very_red()
            