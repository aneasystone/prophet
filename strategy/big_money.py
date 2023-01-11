from strategy import Strategy

class BigMoney(Strategy):


    def is_money_flow_in(self):
        buy_lg_amount = self.stk.money_flow['buy_lg_amount'].values[-1]
        sell_lg_amount = self.stk.money_flow['sell_lg_amount'].values[-1]
        buy_elg_amount = self.stk.money_flow['buy_elg_amount'].values[-1]
        sell_elg_amount = self.stk.money_flow['sell_elg_amount'].values[-1]
        # print(buy_lg_amount+buy_elg_amount-sell_lg_amount-sell_elg_amount)
        return buy_lg_amount+buy_elg_amount-sell_lg_amount-sell_elg_amount > 3000

    def is_recommended(self):
        return self.is_money_flow_in()
