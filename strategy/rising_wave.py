from strategy import Strategy
import matplotlib.pyplot as plt
import numpy as np
import os

class RisingWave(Strategy):

    # 是否为波谷
    def is_trough(self, d, day):
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
            if i >= d - day:
                break
            _close = self.stk.prices['close'].values[-d+i]
            if _close < today_close:
                return False
            if _close / today_close > 1.1:
                break
        # print("TROUGH %s %.2f" % (today, today_close))
        return True

    # 是否为波峰
    def is_crest(self, d, day):
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
            if i >= d - day:
                break
            _close = self.stk.prices['close'].values[-d+i]
            if _close > today_close:
                return False
            if today_close / _close > 1.1:
                break
        # print("CREST %s %.2f" % (today, today_close))
        return True

    def save_wave_jpg(self, peaks):
        plt.cla()
        plt.title(self.stk.code)
        plt.plot(
            [peak['date'] for peak in peaks],
            [peak['close'] for peak in peaks],
            label="close", color='g', linewidth=2, linestyle=':')
        plt.legend()
        plt.grid()
        # plt.show()
        if not os.path.exists('wave/' + self.stk.date):
            os.makedirs('wave/' + self.stk.date)
        plt.savefig('wave/' + self.stk.date + '/' + self.stk.code + '.jpg')

    def get_peaks(self, day):
        peaks = []
        for d in range(60,day,-1):
            today_close = self.stk.prices['close'].values[-d]
            today = self.stk.prices['trade_date'].values[-d]
            # print("%s %.2f" % (today, today_close))
            if self.is_crest(d, day):
                peaks.append({
                    'date': today,
                    'close': today_close,
                    'type': 'crest',
                })
            if self.is_trough(d, day):
                peaks.append({
                    'date': today,
                    'close': today_close,
                    'type': 'trough',
                })
        return peaks

    def is_recommended(self):
        peaks_today = self.get_peaks(0)
        peaks_yesterday = self.get_peaks(1)
        # print(peaks_today)
        # print(peaks_yesterday)
        if peaks_today[-1]['type'] != peaks_yesterday[-1]['type'] and peaks_today[-1]['type'] == 'crest':
            self.save_wave_jpg(peaks_today)
            return True
        return False
