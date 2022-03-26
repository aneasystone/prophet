from strategy import Strategy

class BigRed3OpenLow(Strategy):
    
    def is_red_3(self):
        close_2 = self.stk.prices['close'].values[-2]
        close_5 = self.stk.prices['close'].values[-5]
        rate_2_5 = (close_2 - close_5) / close_5 * 100
        # print(close_2, close_5, rate_2_5)
        return rate_2_5 >= 29

    def is_today_open_low(self):
        open_1 = self.stk.prices['open'].values[-1]
        close_2 = self.stk.prices['close'].values[-2]
        rate_1_2 = (open_1 - close_2) / close_2 * 100
        # print(rate_1_2)
        return -4 <= rate_1_2 <= 4

    def is_recommended(self):
        return self.is_red_3() and self.is_today_open_low()
            