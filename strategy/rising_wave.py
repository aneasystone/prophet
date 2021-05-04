from strategy import Strategy
import matplotlib.pyplot as plt
import numpy as np
import os

class RisingWave(Strategy):

    # 是否为波谷
    def is_trough(self, d):
        today = self.stk.prices['trade_date'].values[-d]
        today_close = self.stk.prices['close'].values[-d]
        i = 0
        while True:
            i += 1
            if i + d >= 60 or i + d >= len(self.stk.prices['close'].values):
                break
            _close = self.stk.prices['close'].values[-d-i]
            if _close < today_close:
                return False
            if _close / today_close > 1.1:
                break
        i = 0
        while True:
            i += 1
            if i >= d:
                break
            _close = self.stk.prices['close'].values[-d+i]
            if _close < today_close:
                return False
            if _close / today_close > 1.1:
                break
        # print("TROUGH %s %.2f" % (today, today_close))
        return True

    # 是否为波峰
    def is_crest(self, d):
        today = self.stk.prices['trade_date'].values[-d]
        today_close = self.stk.prices['close'].values[-d]
        i = 0
        while True:
            i += 1
            if i + d >= 60 or i + d >= len(self.stk.prices['close'].values):
                break
            _close = self.stk.prices['close'].values[-d-i]
            if _close > today_close:
                return False
            if today_close / _close > 1.1:
                break
        i = 0
        while True:
            i += 1
            if i >= d:
                break
            _close = self.stk.prices['close'].values[-d+i]
            if _close > today_close:
                return False
            if today_close / _close > 1.1:
                break
        # print("CREST %s %.2f" % (today, today_close))
        return True

    def save_wave_jpg(self, dates, peaks):
        plt.cla()
        plt.title(self.stk.code)
        plt.plot(dates, peaks, label="close", color='g', linewidth=2, linestyle=':')
        plt.legend()
        plt.grid()
        # plt.show()
        if not os.path.exists('wave/' + self.stk.date):
            os.makedirs('wave/' + self.stk.date)
        plt.savefig('wave/' + self.stk.date + '/' + self.stk.code + '.jpg')

    def is_recommended(self):

        crests = []
        troughs = []
        peaks = []
        dates = []
        now_is_trough = False
        for d in range(60,0,-1):
            today_close = self.stk.prices['close'].values[-d]
            today = self.stk.prices['trade_date'].values[-d]
            if self.is_crest(d):
                now_is_trough = False
                crests.append(today_close)
                peaks.append(today_close)
                dates.append(today)
            if self.is_trough(d):
                now_is_trough = True
                troughs.append(today_close)
                peaks.append(today_close)
                dates.append(today)
        
        today = self.stk.prices['trade_date'].values[-1]
        if len(crests) >= 3 and len(troughs) >= 2 and now_is_trough and today != dates[-1]:
            self.save_wave_jpg(dates, peaks)
            return True
        return False
