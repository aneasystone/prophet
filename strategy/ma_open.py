from strategy import Strategy

class MaOpen(Strategy):

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

    def is_recommended(self):
        ma_open_days = self.get_ma_open_days()
        self.stk.features.append('MA_OPEN_%02d' % (ma_open_days))
        return ma_open_days >= 5

