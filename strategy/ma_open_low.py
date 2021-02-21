from strategy import Strategy

class MaOpenLow(Strategy):

    def get_ma_open_days(self):
        i = 1
        while True:
            # print(self.stk.ma5[-i], self.stk.ma10[-i], self.stk.ma20[-i])
            if self.stk.ma5[-i] > self.stk.ma10[-i] and self.stk.ma10[-i] > self.stk.ma20[-i]:
                i += 1
                continue
            break
        # print(i)
        return i
        
    def get_low_rate_in_days(self, ma_open_days, before_days):
        low_days = 0
        for i in range(before_days):
            if self.stk.ma5[-i-ma_open_days] < self.stk.ma10[-i-ma_open_days]:
                low_days += 1
        return low_days / before_days

    def is_recommended(self):
        ma_open_days = self.get_ma_open_days()
        low_rate = self.get_low_rate_in_days(ma_open_days, 45)
        self.stk.features.append('MA_OPEN_%02d' % (ma_open_days))
        self.stk.features.append('LOW_RATE_%.2f' % (low_rate))
        return ma_open_days == 5 and low_rate >= 0.6

