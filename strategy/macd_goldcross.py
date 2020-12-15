from strategy import Strategy

class MacdGoldCross(Strategy):
    
    # check if macd meets gold cross
    def is_macd_gold_cross(self):
        _dif = self.stk.macd[0]
        _dea = self.stk.macd[1]
        _macd = self.stk.macd[2]
        for i in range(2, 11):
            if _dif[-i] > _dea[-i]:
                return False
        return _dif[-1] > _dea[-1] and _macd[-1] > 0

    # is close > open
    def is_red(self):
        _open = self.stk.prices['open'].values[-1]
        _close = self.stk.prices['close'].values[-1]
        return _close > _open

    # check if the head is very long
    def is_head_very_long(self):
        body, tail, head = self.get_body_head_tail()
        return head > body

    def is_recommended(self):
        # latest 7 days, average amplitude over 3%
        if not self.is_amplitude_over(7, 3):
            return False
        return self.is_macd_gold_cross() and self.is_red() and not self.is_head_very_long()
            