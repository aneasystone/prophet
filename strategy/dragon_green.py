from strategy import Strategy

class DragonGreen(Strategy):

    def is_green(self):
        close = self.stk.prices['close'].values[-1]
        open = self.stk.prices['open'].values[-1]
        return close < open

    # ma is open
    def is_ma_open(self):
        level = self.get_stock_level(-1)
        return level <= 1

    def is_money_flow_in(self):
        buy_lg_amount = self.stk.money_flow['buy_lg_amount'].values[-1]
        sell_lg_amount = self.stk.money_flow['sell_lg_amount'].values[-1]
        buy_elg_amount = self.stk.money_flow['buy_elg_amount'].values[-1]
        sell_elg_amount = self.stk.money_flow['sell_elg_amount'].values[-1]
        # print(buy_lg_amount+buy_elg_amount-sell_lg_amount-sell_elg_amount)
        return buy_lg_amount+buy_elg_amount-sell_lg_amount-sell_elg_amount > 1000

    def is_recommended(self):
        return self.is_money_flow_in() and self.is_ma_open() and self.is_green()
