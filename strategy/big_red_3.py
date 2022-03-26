from strategy import Strategy

class BigRed3(Strategy):
    
    def is_red_3(self):
        close_1 = self.stk.prices['close'].values[-1]
        close_4 = self.stk.prices['close'].values[-4]
        rate_1_4 = (close_1 - close_4) / close_4 * 100
        # print(close_2, close_5, rate_2_5)
        return rate_1_4 >= 29

    def is_recommended(self):
        return self.is_red_3()
            