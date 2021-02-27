from strategy import Strategy

class YearLowest(Strategy):
    
    def is_gold_cross(self, delta):
        if delta[0] == -1 or delta[-1] == 1:
            return False
        return all(delta[i] >= delta[i+1] for i in range(len(delta)-1))

    # check if week macd meets gold cross
    def is_week_macd_gold_cross(self):
        _dif = self.stk.week_macd[0]
        _dea = self.stk.week_macd[1]
        _macd = self.stk.week_macd[2]
        delta = []
        for i in range(1, 15):
            if _dif[-i] > _dea[-i]:
                delta.append(1)
            else:
                delta.append(-1)
        return self.is_gold_cross(delta) and _macd[-1] > 0

    def is_lowest(self):
        lowest = 9999
        highest = -9999
        today_close = self.stk.prices['close'].values[-1]
        for i in range(200):
            _close = self.stk.prices['close'].values[-2-i]
            # print(_close)
            if _close > highest:
                highest = _close
            if _close < lowest:
                lowest = _close
        # print(highest, lowest)
        self.stk.features.append('HIGHEST_%.2f' % (highest))
        self.stk.features.append('LOWEST_%.2f' % (lowest))
        rate = (today_close - lowest) / (highest - lowest)
        # print(rate)
        self.stk.features.append('RATE_%.2f' % (rate))
        return rate < 0.3

    def is_recommended(self):
        return self.is_lowest() and self.is_week_macd_gold_cross()
            