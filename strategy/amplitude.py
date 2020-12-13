from strategy import Strategy

class Amplitude(Strategy):

    # check if average amplitude of latest n days is over m%
    def is_amplitude_over(self, days, percent):
        cnt = 0
        for i in range(1, days + 1):
            _high = self.stk.prices['high'].values[-i]
            _low = self.stk.prices['low'].values[-i]
            _pre_close = self.stk.prices['pre_close'].values[-i]
            amplitude = (_high - _low) / _pre_close
            # print(amplitude)
            if 100 * amplitude > percent:
                cnt += 1
        return cnt >= days - 1

    def is_recommended(self):
        if not self.is_low_macd():
            return False
        # latest 7 days
        # average amplitude over 3%
        return self.is_amplitude_over(7, 3)
