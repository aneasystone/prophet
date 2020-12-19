from abc import abstractmethod
import traceback
from stock import Stock
from repository import Repository

class Strategy:

    stk = None
    repo = None

    def __init__(self, stk):
        self.stk = stk
        self.repo = stk.repo

    @abstractmethod
    def is_recommended(self):
        pass

    # check if macd metric is low
    def is_low_macd(self):
        dif = self.stk.macd[0]
        dea = self.stk.macd[1]
        count = 0
        for i in range(1, 11):
            if dif[-i] < dea[-i]:
                count += 1
        return count >= 8
    
    # check if average amplitude of latest n days is over m%
    def is_amplitude_over(self, days, percent):
        cnt = 0
        for i in range(1, days + 1):
            _high = self.stk.prices['high'].values[-i]
            _low = self.stk.prices['low'].values[-i]
            _pre_close = self.stk.prices['pre_close'].values[-i]
            amplitude = (_high - _low) / _pre_close
            # print(amplitude)
            if 100 * amplitude > percent:
                cnt += 1
        return cnt >= days - 1

    # check if today's low price is the lowest in recent days
    def is_lowest(self):
        _low = self.stk.prices['low'].values[-1]
        for i in range(2, 15):
            if self.stk.prices['low'].values[-i] < _low:
                return False
        return True

    # get today's body, head and tail
    def get_body_head_tail(self):
        _open = self.stk.prices['open'].values[-1]
        _close = self.stk.prices['close'].values[-1]
        _high = self.stk.prices['high'].values[-1]
        _low = self.stk.prices['low'].values[-1]
        if _open > _close:
            body = _open - _close
            tail = _close - _low
            head = _high - _open
        else:
            body = _close - _open
            tail = _open - _low
            head = _high - _close
        return body, tail, head

    # check if tomorrow's open price can profit in n days, and calculate the max profit rate
    @abstractmethod
    def get_max_profit_rate(self, n):
        after_prices = self.repo.get_all_prices_after(self.stk.code, self.stk.date)
        buy_price = after_prices['open'].values[0]
        high = after_prices['high'].values[n]
        return (high - buy_price) / buy_price

    # get profit statistics
    def get_profit_statistics(self):
        statistics = []
        for n in range(1, 31):
            max_profit_rate = self.get_max_profit_rate(n)
            if max_profit_rate == -999:
                return None
            statistics.append(max_profit_rate)
        return statistics
