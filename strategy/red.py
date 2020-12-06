from strategy import Strategy

class Red(Strategy):
    
    # rate +5%
    def is_very_red(self):
        today_close = self.stk.prices['close'].values[-1]
        yesterday_close = self.stk.prices['close'].values[-2]
        rate = (today_close - yesterday_close) / yesterday_close * 100
        return rate >= 5

    def is_recommended(self):
        return self.is_very_red()
            