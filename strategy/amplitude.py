from strategy import Strategy

class Amplitude(Strategy):

    def is_damn_down(self):
        pct_chg = self.stk.prices['pct_chg'].values[-1]
        return pct_chg < -5

    def is_recommended(self):
        if not self.is_low_macd():
            return False
        if self.is_damn_down():
            return False
        # latest 7 days
        # average amplitude over 3%
        return self.is_amplitude_over(7, 3)

    def get_max_profit_rate(self, n):
        after_prices = self.repo.get_all_prices_after(self.stk.code, self.stk.date)
        pre_close = after_prices['pre_close'].values[0]
        low = after_prices['low'].values[0]

        # calculate a fit buy price
        average_amplitude = self.stk.get_average_amplitude(7)
        buy_price = pre_close * (1 - average_amplitude/2)
        if (buy_price <= low):
            return -999
        high = after_prices['high'].values[n]
        return (high - buy_price) / buy_price