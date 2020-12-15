from strategy import Strategy

class Hammer(Strategy):

    # check if today's kline is hammer
    def is_hammer(self):
        body, tail, head = self.get_body_head_tail()
        if body == 0:
            body = 0.1
        if head == 0:
            head = 0.1
        return tail / body > 2 and tail / head > 3

    def is_recommended(self):
        # latest 7 days, average amplitude over 3%
        if not self.is_amplitude_over(7, 3):
            return False
        if not self.is_low_macd():
            return False
        return self.is_lowest() and self.is_hammer()
