from strategy import Strategy

class YearDouble(Strategy):

    def has_double(self):
        max_max_profit = -999999
        max_i = -1
        for i in range(200):
            # -200 ~ -2
            close_i = self.stk.prices['close'].values[-200+i-1]
            max_profit = -9999
            max_j = -1
            for j in range(200):
                # -199 ~ -1
                close_j = self.stk.prices['close'].values[-200+j]
                profit = close_j / close_i
                # print(i, close_i, j, close_j, profit)
                if profit > max_profit:
                    max_profit = profit
                    max_j = j
            if max_profit > max_max_profit:
                max_max_profit = max_profit
                max_i = i
        if max_max_profit > 2:
            self.stk.features.append('PROFIT_%.2f' % (max_max_profit))
            self.stk.features.append('I_%d' % (max_i))
            self.stk.features.append('J_%d' % (max_j))
            return True
        return False

    def is_recommended(self):
        return self.has_double()
            