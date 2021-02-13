from strategy import Strategy

class MaOpenRed(Strategy):

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
        
    def get_increase_rate(self):
        today_close = self.stk.prices['close'].values[-1]
        yesterday_close = self.stk.prices['close'].values[-2]
        return (today_close - yesterday_close) / yesterday_close * 100

    def is_recommended(self):
        ma_open_days = self.get_ma_open_days()
        self.stk.features.append('MA_OPEN_' + str(ma_open_days))
        increase_rate = self.get_increase_rate()
        return ma_open_days >= 10 and increase_rate > 5

