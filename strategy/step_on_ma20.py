from strategy import Strategy

class StepOnMa20(Strategy):

    # check if ma is open
    def is_ma_open(self, ma5, ma10, ma20):
        # print("%.2f %.2f %.2f" % (ma5, ma10, ma20))
        is_open = ma5 > ma10 and ma10 > ma20
        if not is_open:
            return False
        # open is big
        d_5_10 = abs((ma5-ma10)/ma10)
        d_10_20 = abs((ma10-ma20)/ma20)
        # print("%.4f %.4f" % (d_5_10, d_10_20))
        return d_5_10 > 0.01 and d_10_20 > 0.005

    def get_ma_open_days(self, d):
        i = 1
        while True:
            if self.is_ma_open(self.stk.ma5[-i-d], self.stk.ma10[-i-d], self.stk.ma20[-i-d]):
                i += 1
                continue
            break
        return i

    def is_step_on_ma20(self):
        today_low = self.stk.prices['low'].values[-1]
        return today_low < self.stk.ma20[-1]

    def is_recommended(self):
        ma_open_count = 0
        last_open = -1
        d = 0
        while d < 60:
            today = self.stk.prices['trade_date'].values[-1-d]
            ma_open_days = self.get_ma_open_days(d)
            # print("%d %s %d" % (d, today, ma_open_days))
            if ma_open_days >= 5:
                ma_open_count += 1
                if last_open == -1:
                    last_open = d
                d += ma_open_days
            d += 1
        self.stk.features.append('MA_OPEN_C_%02d' % (ma_open_count))
        # print("last open %d" % (last_open))
        return ma_open_count == 1 and last_open < 5 and self.is_step_on_ma20()
