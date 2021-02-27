from strategy import Strategy

class WeekMaOpen(Strategy):

    def get_ma_open_weeks(self):
        i = 1
        while True:
            # print(self.stk.ma5[-i], self.stk.ma10[-i], self.stk.ma20[-i])
            if self.stk.week_ma5[-i] > self.stk.week_ma10[-i] and self.stk.week_ma10[-i] > self.stk.week_ma20[-i]:
                i += 1
                continue
            break
        # print(i)
        return i

    def is_recommended(self):
        ma_open_weeks = self.get_ma_open_weeks()
        self.stk.features.append('MA_OPEN_%02d' % (ma_open_weeks))
        return ma_open_weeks == 2

