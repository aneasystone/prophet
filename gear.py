from stock import Stock

if __name__ == '__main__':

    date = "20201230"
    stocks = ["601598.SH", "000545.SZ", "600707.SH", "600733.SH"]
    for stock in stocks:
        stk = Stock('', stock, date)
        if stk.init():
            average_amplitude = stk.get_average_amplitude(7)
            b1 = stk.close * (1 - average_amplitude * 0.25)
            b2 = stk.close * (1 - average_amplitude * 0.5)
            b3 = stk.close * (1 - average_amplitude * 0.75)
            b4 = stk.close * (1 - average_amplitude * 1)
            u1 = stk.close * (1 + average_amplitude * 0.25)
            u2 = stk.close * (1 + average_amplitude * 0.5)
            u3 = stk.close * (1 + average_amplitude * 0.75)
            u4 = stk.close * (1 + average_amplitude * 1)

            print("%s %s %s" % (stk.code, stk.name, stk.industry))
            print("close price       = %.2f" % stk.close)
            print("average amplitude = %.2f%%" % (average_amplitude * 100))
            print("gear delta        = %.2f" % (stk.close * average_amplitude * 0.25))
            print("gear prices:")
            print("%.2f\t%.2f\t%.2f\t%.2f\t%.2f\t%.2f\t%.2f\t%.2f\t%.2f" % (
                b4, b3, b2, b1, stk.close, u1, u2, u3, u4
            ))
            print("---------------------------------------------")