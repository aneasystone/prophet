from strategy import Strategy

class BigMoney(Strategy):

    def get_money_flow(self, i):
        buy_lg_amount = self.stk.money_flow['buy_lg_amount'].values[i]
        sell_lg_amount = self.stk.money_flow['sell_lg_amount'].values[i]
        buy_elg_amount = self.stk.money_flow['buy_elg_amount'].values[i]
        sell_elg_amount = self.stk.money_flow['sell_elg_amount'].values[i]
        # print(buy_lg_amount+buy_elg_amount-sell_lg_amount-sell_elg_amount)
        return buy_lg_amount+buy_elg_amount-sell_lg_amount-sell_elg_amount

    def is_big_money(self, i):
        return self.get_money_flow(i) > 3000

    def is_big_money_start_today(self):
        return self.is_big_money(-1) \
            and not self.is_big_money(-2) \
            and not self.is_big_money(-3) \
            and not self.is_big_money(-4) \
            and not self.is_big_money(-5)

    def is_recommended(self):
        return self.is_big_money_start_today()
