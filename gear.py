from stock import Stock

if __name__ == '__main__':

    date = "20201230"
    stocks = ["601598.SH", "000545.SZ", "600707.SH", "600733.SH"]
    for stock in stocks:
        stk = Stock('', stock, date)
        if stk.init():
            b1 = stk.get_gear_price(-1)
            b2 = stk.get_gear_price(-2)
            b3 = stk.get_gear_price(-3)
            b4 = stk.get_gear_price(-4)
            u1 = stk.get_gear_price(1)
            u2 = stk.get_gear_price(2)
            u3 = stk.get_gear_price(3)
            u4 = stk.get_gear_price(4)

            print("%s %s %s" % (stk.code, stk.name, stk.industry))
            print("close price       = %.2f" % stk.close)
            print("average amplitude = %.2f%%" % (stk.average_amplitude * 100))
            print("gear delta        = %.2f" % (stk.close * stk.average_amplitude * 0.25))
            print("gear prices:")
            print("%.2f\t%.2f\t%.2f\t%.2f\t%.2f\t%.2f\t%.2f\t%.2f\t%.2f" % (
                b4, b3, b2, b1, stk.close, u1, u2, u3, u4
            ))
            print("---------------------------------------------")