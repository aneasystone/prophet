from strategy import Strategy

class HammerPlus(Strategy):

    # check if yesterday's kline is hammer
    def is_yesterday_hammer(self):
        body, tail, head = self.get_body_head_tail(-2)
        if body == 0:
            body = 0.1
        if head == 0:
            head = 0.1
        return tail / body > 2 and tail / head > 3

    # today's close > yesterday's close
    # today's low > yesterday's low
    def is_today_rise(self):
        today_close = self.stk.prices['close'].values[-1]
        yesterday_close = self.stk.prices['close'].values[-2]
        today_low = self.stk.prices['low'].values[-1]
        yesterday_low = self.stk.prices['low'].values[-2]
        return today_close > yesterday_close and today_low > yesterday_low

    def is_recommended(self):
        # latest 7 days, average amplitude over 3%
        if not self.is_amplitude_over(7, 3):
            return False
        if not self.is_low_macd():
            return False
        return self.is_lowest(-2) and self.is_yesterday_hammer() and self.is_today_rise()
