from strategy import Strategy

class MacdGoldCrossMinus(Strategy):
    
    # check if pre macd meets gold cross
    def is_macd_gold_cross_minus(self):
        _dif = self.stk.pre_macd[0]
        _dea = self.stk.pre_macd[1]
        _macd = self.stk.pre_macd[2]
        for i in range(2, 15):
            if _dif[-i] > _dea[-i]:
                return False
        return _dif[-1] > _dea[-1] and _macd[-1] > 0

    # check if dif is low
    def is_dif_low(self):
        _dif = self.stk.macd[0]
        return _dif[-1] < 0

    # check if tommorow's ma is still open
    def is_pre_ma_open(self):
        return self.stk.pre_ma5[-1] < self.stk.pre_ma10[-1] < self.stk.pre_ma20[-1]

    # check if the head is very long
    def is_head_very_long(self):
        body, tail, head = self.get_body_head_tail()
        return head > body

    def is_recommended(self):
        
        # latest 7 days, average amplitude over 3%
        #
        if not self.is_amplitude_over(7, 3):
            return False

        # ma is still open
        #
        if self.is_pre_ma_open():
            return False

        # dif is too high
        #
        if not self.is_dif_low():
            return False

        # not red
        #
        if not self.is_red():
            return False

        # head too long
        #
        if self.is_head_very_long():
            return False
        
        return self.is_macd_gold_cross_minus()
