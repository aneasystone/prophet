from .big_red import BigRed

class OneLineRed(BigRed):
	
    def is_one_line_red(self):
        today_open = self.stk.prices['open'].values[-1]
        today_close = self.stk.prices['close'].values[-1]
        today_low = self.stk.prices['low'].values[-1]
        today_high = self.stk.prices['high'].values[-1]
        return today_open == today_close == today_low == today_high

    def is_recommended(self):
        return self.is_first_big_red() and self.is_one_line_red()