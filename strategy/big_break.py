from strategy import Strategy

class BigBreak(Strategy):
    
    # ma is open
    def is_ma_open(self):
        level = self.get_stock_level(-1)
        return level < 3

    def is_break(self):
        today_open = self.stk.prices['open'].values[-1]
        today_close = self.stk.prices['close'].values[-1]
        yesterday_close = self.stk.prices['close'].values[-2]
        open_rate = (today_open - yesterday_close) / yesterday_close * 100
        close_rate = (today_close - yesterday_close) / yesterday_close * 100
        return open_rate >= 9 and close_rate <= 5

    def is_recommended(self):
        return self.is_break() and self.is_ma_open()
            