from strategy import Strategy

class UpWindow(Strategy):
    
    def is_up_window(self):
        today_low = self.stk.prices['low'].values[-1]
        yesterday_high = self.stk.prices['high'].values[-2]
        return today_low > yesterday_high

    def is_recommended(self):
        return self.is_up_window()
            