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
        if not self.is_low_macd():
            return False
        return self.is_lowest() and self.is_hammer()
