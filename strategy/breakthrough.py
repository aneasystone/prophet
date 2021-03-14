from strategy import Strategy

class BreakThrough(Strategy):

    # 计算当日涨幅
    def get_increase_rate(self):
        today_close = self.stk.prices['close'].values[-1]
        yesterday_close = self.stk.prices['close'].values[-2]
        return (today_close - yesterday_close) / yesterday_close * 100

    # 最近 60 日，最高价
    def get_highest_price(self):
        highest = -9999
        for i in range(60):
            # 忽略最近 10 天
            if i < 10:
                continue
            _close = self.stk.prices['close'].values[-i]
            if _close > highest:
                highest = _close
        return highest
    
    # 最近 10 日，均线发散率
    def get_ma_open_rate(self):
        total_days = 10
        open_days = 0
        for i in range(1, total_days+1):
            if self.stk.ma5[-i] > self.stk.ma10[-i] and self.stk.ma10[-i] > self.stk.ma20[-i]:
                open_days += 1
        return open_days / total_days

    def is_recommended(self):
        # 当日涨幅大于 5%
        # 且
        # 突破 60 日最高价
        # 且
        # 均线发散率大于 0.5
        increase_rate = self.get_increase_rate()
        highest_price = self.get_highest_price()
        today_close = self.stk.prices['close'].values[-1]
        ma_open_rate = self.get_ma_open_rate()
        # print(increase_rate)
        # print(highest_price)
        # print(ma_open_rate)
        
        return increase_rate > 5  and 1.1 > today_close / highest_price > 1 and ma_open_rate > 0.5
