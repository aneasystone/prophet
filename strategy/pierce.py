from strategy import Strategy

class Pierce(Strategy):
    
    # check if today's kline is pierce
    def is_pierce(self):
        today_open = self.stk.prices['open'].values[-1]
        today_close = self.stk.prices['close'].values[-1]
        yesterday_open = self.stk.prices['open'].values[-2]
        yesterday_close = self.stk.prices['close'].values[-2]
        if today_close > today_open and yesterday_close < yesterday_open and today_open < yesterday_close:
            if today_close > yesterday_open:
                # 'SWALLOW'
                return False
            if yesterday_open - today_close < today_close - yesterday_close:
                # 'PIERCE'
                return True
        return False

    def is_recommended(self):
        if not self.is_low_macd():
            return False
        return self.is_lowest() and self.is_pierce()
