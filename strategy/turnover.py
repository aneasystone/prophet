from strategy import Strategy

class Turnover(Strategy):
    
    # check if today's turnover is far more than previous days
    def is_huge_turnover(self):
        vol_today = self.stk.prices['vol'].values[-1]
        vol_sum = 0
        for i in range(2, 17):
            vol = self.stk.prices['vol'].values[-i]
            if vol / vol_today > 0.5:
                return False
            vol_sum += vol
        vol_avg = vol_sum / 15
        return vol_today > vol_avg * 2

    def is_recommended(self):
        return self.is_huge_turnover() and self.is_red() and not self.is_head_very_long()
