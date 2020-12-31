from strategy.hammer import Hammer
from strategy.hammer_plus import HammerPlus
from strategy.pierce import Pierce
from strategy.swallow import Swallow
from strategy.macd_goldcross import MacdGoldCross
from strategy.macd_goldcross_minus import MacdGoldCrossMinus
from strategy.river_flower import RiverFlower
from strategy.red import Red
from strategy.amplitude import Amplitude
from strategy.turnover import Turnover

class StrategyFactory:

    def match_strategies(self, stk):
        
        # define all strategies here
        strategies = {
            # "HAMMER": Hammer(stk),
            # "HAMMERPLUS": HammerPlus(stk),
            # "PIERCE": Pierce(stk),
            # "SWALLOW": Swallow(stk),
            "MACDGOLDCROSS": MacdGoldCross(stk),
            "MACDGOLDCROSSMINUS": MacdGoldCrossMinus(stk),
            # "RIVERFLOWER": RiverFlower(stk),
            # "RED": Red(stk),
            # "AMPLITUDE": Amplitude(stk),
            # "TURNOVER": Turnover(stk),
        }

        # which strategy is recommended
        ss = {}
        for s in strategies:
            if strategies[s].is_recommended():
                ss[s] = strategies[s]
        return ss
