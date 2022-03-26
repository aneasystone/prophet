from strategy import Strategy

class Dragon(Strategy):
    
    def is_rise_stop(self, i):
        today_close = self.stk.prices['close'].values[i]
        today_high = self.stk.prices['high'].values[i]
        yesterday_close = self.stk.prices['close'].values[i-1]
        # print(today_close,yesterday_close)
        return today_close/yesterday_close > 1.0985 and today_close == today_high

    def is_rise_stop_twice(self):
        b1 = self.is_rise_stop(-1) and self.is_rise_stop(-2)
        b2 = self.is_rise_stop(-1) and self.is_rise_stop(-3)
        # print(b1, b2)
        return b1 or b2

    def is_money_flow_in(self):
        buy_lg_amount = self.stk.money_flow['buy_lg_amount'].values[-1]
        sell_lg_amount = self.stk.money_flow['sell_lg_amount'].values[-1]
        buy_elg_amount = self.stk.money_flow['buy_elg_amount'].values[-1]
        sell_elg_amount = self.stk.money_flow['sell_elg_amount'].values[-1]
        # print(buy_lg_amount+buy_elg_amount-sell_lg_amount-sell_elg_amount)
        return buy_lg_amount+buy_elg_amount-sell_lg_amount-sell_elg_amount > 3000

    def is_big_amount(self):
        b1 = self.stk.prices['amount'].values[-1] > 600_000
        b2 = self.stk.prices['amount'].values[-2] > 600_000
        b3 = self.stk.prices['amount'].values[-3] > 600_000
        # print(b1, b2, b3)
        return b1 or b2 or b3

    def is_recommended(self):
        return self.is_rise_stop_twice() and self.is_money_flow_in() and self.is_big_amount()
