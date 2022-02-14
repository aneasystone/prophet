from strategy import Strategy

class BigRedContinuous(Strategy):
    
    def is_very_red(self):
        close_1 = self.stk.prices['close'].values[-1]
        close_4 = self.stk.prices['close'].values[-4]
        rate_1_4 = (close_1 - close_4) / close_4 * 100
        return rate_1_4 >= 27

    def is_recommended(self):
        return self.is_very_red()
            