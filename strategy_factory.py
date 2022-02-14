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
from strategy.ma_open_four import MaOpenFour
from strategy.ma_open_red import MaOpenRed
from strategy.ma_open_low import MaOpenLow
from strategy.year_lowest import YearLowest
from strategy.year_double import YearDouble
from strategy.week_ma_open import WeekMaOpen
from strategy.breakthrough import BreakThrough
from strategy.rising_wave import RisingWave
from strategy.rising_wave_on_ma20 import RisingWaveOnMa20
from strategy.step_on_ma20 import StepOnMa20

from strategy.big_red import BigRed
from strategy.one_line_red import OneLineRed
from strategy.up_window import UpWindow
from strategy.big_red_1 import BigRed1
from strategy.big_red_2 import BigRed2
from strategy.big_red_3 import BigRed3
from strategy.big_red_4 import BigRed4
from strategy.big_break import BigBreak
from strategy.big_red_continuous import BigRedContinuous

class StrategyFactory:

    def __init__(self, repo):
        self.repo = repo

    def match_strategies(self, stk):
        
        # define all strategies here
        strategies = {
            # "HAMMER": Hammer(stk),
            # "HAMMERPLUS": HammerPlus(stk),
            # "PIERCE": Pierce(stk),
            # "SWALLOW": Swallow(stk),
            # "MACDGOLDCROSS": MacdGoldCross(stk),
            # "MACDGOLDCROSSMINUS": MacdGoldCrossMinus(stk),
            # "MACDREVERT": MacdRevert(stk),
            # "RIVERFLOWER": RiverFlower(stk),
            # "RED": Red(stk),
            # "AMPLITUDE": Amplitude(stk),
            # "TURNOVER": Turnover(stk),
            
            # "MAOPEN": MaOpen(stk),
            # "MAOPENFOUR": MaOpenFour(stk),
            # "MAOPENRED": MaOpenRed(stk),
            # "MAOPENLOW": MaOpenLow(stk),
            # "BREAKTHROUGH": BreakThrough(stk),

            # "YEARLOWEST": YearLowest(stk),
            # "YEARDOUBLE": YearDouble(stk),
            # "WEEKMAOPEN": WeekMaOpen(stk),
            
            # "RISINGWAVE": RisingWave(stk),
            # "RISINGWAVEONMA20": RisingWaveOnMa20(stk),
            # "STEPONMA20": StepOnMa20(stk),

            "涨停": BigRed(stk),
            "炸板": BigBreak(stk),
            "连板": BigRedContinuous(stk),
            
            # "跳空": UpWindow(stk),
            # "一板": BigRed1(stk),
            # "二板": BigRed2(stk),
            # "三板": BigRed3(stk),
            # "四板": BigRed4(stk),
        }

        # which strategy is recommended
        ss = {}
        for s in strategies:
            if strategies[s].is_recommended():
                ss[s] = strategies[s]
        return ss

    def do_strategy(self, trade_date):
        results = {}
        stocks = self.repo.get_all_stocks()
        for ss in stocks:
            try:
                # for debug
                # if ss['ts_code'] != '000819.SZ':
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