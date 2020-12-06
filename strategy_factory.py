from strategy.hammer import Hammer
from strategy.pierce import Pierce
from strategy.macd_goldcross import MacdGoldCross

class StrategyFactory:

    def match_strategies(self, stk):
        
        # define all strategies here
        strategies = {
            "HAMMER": Hammer(stk),
            "PIERCE": Pierce(stk),
            "MACDGOLDCROSS": MacdGoldCross(stk),
        }

        # which strategy is recommended
        ss = {}
        for s in strategies:
            if strategies[s].is_recommended():
                ss[s] = strategies[s]
        return ss
