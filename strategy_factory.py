from stock import Stock
from repository import Repository

import traceback

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
from strategy.macd_revert import MacdRevert
from strategy.ma_open import MaOpen
from strategy.ma_open_red import MaOpenRed
from strategy.ma_open_low import MaOpenLow
from strategy.year_lowest import YearLowest
from strategy.year_double import YearDouble
from strategy.week_ma_open import WeekMaOpen

class StrategyFactory:

    def match_strategies(self, stk):
        
        # define all strategies here
        strategies = {
            # "HAMMER": Hammer(stk),
            # "HAMMERPLUS": HammerPlus(stk),
            # "PIERCE": Pierce(stk),
            # "SWALLOW": Swallow(stk),
            # "MACDGOLDCROSS": MacdGoldCross(stk),
            # "MACDGOLDCROSSMINUS": MacdGoldCrossMinus(stk),
            # "RIVERFLOWER": RiverFlower(stk),
            # "MACDREVERT": MacdRevert(stk),
            # "RED": Red(stk),
            # "AMPLITUDE": Amplitude(stk),
            # "TURNOVER": Turnover(stk),
            
            # "MAOPEN": MaOpen(stk),
            # "MAOPENRED": MaOpenRed(stk),
            # "MAOPENLOW": MaOpenLow(stk),
            # "YEARLOWEST": YearLowest(stk),
            # "YEARDOUBLE": YearDouble(stk),
            "WEEKMAOPEN": WeekMaOpen(stk),
        }

        # which strategy is recommended
        ss = {}
        for s in strategies:
            if strategies[s].is_recommended():
                ss[s] = strategies[s]
        return ss

    def do_strategy(self, trade_date):
        results = {}
        repo = Repository()
        stocks = repo.get_all_stocks()
        for ss in stocks:
            try:
                # for debug
                # if ss['ts_code'] != '000004.SZ':
                #     continue
                
                stk = Stock(ss['name'], ss['ts_code'], trade_date)
                # print(stk.name + " " + stk.code)
                if stk.init():
                    strategies = self.match_strategies(stk)
                    for s in strategies:
                        if s not in results:
                            results[s] = list()
                        results[s].append(stk)
            except:
                # traceback.print_exc()
                pass
        return results