from strategy import Strategy

class MacdRevert(Strategy):
    
    # check if macd revert from red to green, and convert to red again
    def is_macd_revert(self):
        _dif = self.stk.macd[0]
        _dea = self.stk.macd[1]
        if _dif[-1] < 0 and _dea[-1] < 0:
            return False
        _macd = self.stk.macd[2]
        if _macd[-1] < 0 or _macd[-2] >= 0:    
            return False
        
        red_days = 0
        idx = -3
        while True:
            if _macd[idx] >= 0:
                red_days += 1
                idx -= 1
            else:
                break
        if red_days >= 5:
            self.stk.features.append('MACD_RED_' + str(red_days))
            return True
        return False

    def is_recommended(self):
        return self.is_macd_revert()
            