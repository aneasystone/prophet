from strategy import Strategy
import matplotlib.pyplot as plt
import numpy as np
import os

class RisingWaveOnMa20(Strategy):

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

    def is_crest_peak(self, d):
        peaks_today = self.get_peaks(d)
        peaks_yesterday = self.get_peaks(d+1)
        # print(peaks_today)
        # print(peaks_yesterday)
        if peaks_today[-1]['type'] != peaks_yesterday[-1]['type'] and peaks_today[-1]['type'] == 'crest':
            # self.save_wave_jpg(peaks_today)
            return True
        return False

    def get_crest_peak_day(self):
        for d in range(0, 20):
            # print(d)
            if self.is_crest_peak(d):
                return d
        return -1

    def is_ma_open(self, ma5, ma10, ma20):
        is_open = ma5 > ma10 and ma10 > ma20
        if not is_open:
            return False
        d_5_10 = abs((ma5-ma10)/ma10)
        d_10_20 = abs((ma10-ma20)/ma20)
        return d_5_10 > 0.01 and d_10_20 > 0.005

    def is_step_on_ma20(self):
        low_today = self.stk.prices['low'].values[-1]
        low_yesterday = self.stk.prices['low'].values[-2]
        # print("is_step_on_ma20")
        # print(low_today <= self.stk.ma20[-1])
        # print(low_yesterday >= self.stk.ma20[-2])
        return low_today <= self.stk.ma20[-1] and low_yesterday >= self.stk.ma20[-2]

    def is_recommended(self):
        
        d = self.get_crest_peak_day()
        if d <= 0:
            return False
        
        has_ma_open = False
        for i in range(d):
            if self.is_ma_open(self.stk.ma5[-i], self.stk.ma10[-i], self.stk.ma20[-i]):
                has_ma_open = True
                break
        # print(has_ma_open)
        if not has_ma_open:
            return False

        return self.is_step_on_ma20()
