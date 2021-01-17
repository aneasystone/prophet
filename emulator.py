import traceback
from stock import Stock
from repository import Repository
from strategy_factory import StrategyFactory

class Result:
    total_cnt = 0
    buy_miss_cnt = 0
    sell_miss_cnt = 0
    total_profit_rate = 0

def print_green(s):
    print(f"\033[0;32;40m%s\033[0m" % (s))

def print_red(s):
    print(f"\033[0;31;40m%s\033[0m" % (s))

def show_basic_info(stk):
    
    average_amplitude = stk.average_amplitude
    b1 = stk.get_gear_price(-1)
    b2 = stk.get_gear_price(-2)
    b3 = stk.get_gear_price(-3)
    b4 = stk.get_gear_price(-4)
    u1 = stk.get_gear_price(1)
    u2 = stk.get_gear_price(2)
    u3 = stk.get_gear_price(3)
    u4 = stk.get_gear_price(4)
    delta = "%.2f" % (stk.close * average_amplitude * 0.25)

    print("{0:{5}<10}\t{1:<10}\t{2:<10}\t{3:<10}\t{4:{5}<10}".format(
        stk.name, stk.code, str(stk.close), delta, stk.industry, chr(12288)))
    print("%.2f\t%.2f\t%.2f\t%.2f\t%.2f\t%.2f\t%.2f\t%.2f\t%.2f" % (
        b4, b3, b2, b1, stk.close, u1, u2, u3, u4
    ))

def show_result_of_min_and_max_price_in_5_days(stk, dates, i):
    Result.total_cnt += 1
    prices = repo.get_all_prices_after(stk.code, dates[i])

    low = 9999
    high = -9999
    for d in range(1, 6):
        print("%s: %.2f\t%.2f\t%.2f\t%.2f" % (
            dates[i+d], prices['open'].values[d-1], prices['close'].values[d-1], prices['low'].values[d-1], prices['high'].values[d-1]
        ))
        if prices['high'].values[d-1] > high:
            high = prices['high'].values[d-1]
        if prices['low'].values[d-1] < low:
            low = prices['low'].values[d-1]
    print("low  %.2f %.2f" % (low, (low-stk.close)/stk.close))
    print("high %.2f %.2f" % (high, (high-stk.close)/stk.close))

def show_result_of_buy_b1_and_sell_u1_in_2_days(stk, dates, i):
    Result.total_cnt += 1
    prices = repo.get_all_prices_after(stk.code, dates[i])

    # BUY DAY
    print("%s: %.2f\t%.2f\t%.2f\t%.2f" % (
        dates[i+1], prices['open'].values[0], prices['close'].values[0], prices['low'].values[0], prices['high'].values[0]
    ), end=" ")
    b1 = stk.get_gear_price(-1)
    if (prices['low'].values[0] < b1):
        print("BUY at b1 price %.2f" % (b1))
    else:
        print("BUY MISS")
        Result.buy_miss_cnt += 1
        return

    # SELL DAY 1
    print("%s: %.2f\t%.2f\t%.2f\t%.2f" % (
        dates[i+2], prices['open'].values[1], prices['close'].values[1], prices['low'].values[1], prices['high'].values[1]
    ), end=" ")
    u1 = stk.get_gear_price(1)
    if (prices['high'].values[1] > u1):
        profit_rate = (u1-b1)/b1 * 100
        Result.total_profit_rate += profit_rate
        print_red("SELL at u1 price %.2f, profit: %.2f" % (u1, profit_rate))
        return
    else:
        print("SELL MISS")

    # SELL DAY 2
    print("%s: %.2f\t%.2f\t%.2f\t%.2f" % (
        dates[i+3], prices['open'].values[2], prices['close'].values[2], prices['low'].values[2], prices['high'].values[2]
    ), end=" ")
    if (prices['high'].values[2] > u1):
        profit_rate = (u1-b1)/b1 * 100
        Result.total_profit_rate += profit_rate
        print_red("SELL at u1 price %.2f, profit: %.2f" % (u1, profit_rate))
    else:
        profit_rate = (prices['close'].values[2]-b1)/b1 * 100
        Result.total_profit_rate += profit_rate
        Result.sell_miss_cnt += 1
        print_green("SELL MISS, close price: %.2f, profit: %.2f" % (prices['close'].values[2], profit_rate))
    
def show_result_of_buy_b1_and_sell_u1_in_3_days(stk, dates, i):
    Result.total_cnt += 1
    prices = repo.get_all_prices_after(stk.code, dates[i])

    # BUY DAY
    print("%s: %.2f\t%.2f\t%.2f\t%.2f" % (
        dates[i+1], prices['open'].values[0], prices['close'].values[0], prices['low'].values[0], prices['high'].values[0]
    ), end=" ")
    b1 = stk.get_gear_price(-1)
    if (prices['low'].values[0] < b1):
        print("BUY at b1 price %.2f" % (b1))
    else:
        print("BUY MISS")
        Result.buy_miss_cnt += 1
        return

    # SELL DAY 1
    print("%s: %.2f\t%.2f\t%.2f\t%.2f" % (
        dates[i+2], prices['open'].values[1], prices['close'].values[1], prices['low'].values[1], prices['high'].values[1]
    ), end=" ")
    u1 = stk.get_gear_price(1)
    if (prices['high'].values[1] > u1):
        profit_rate = (u1-b1)/b1 * 100
        Result.total_profit_rate += profit_rate
        print_red("SELL at u1 price %.2f, profit: %.2f" % (u1, profit_rate))
        return
    else:
        print("SELL MISS")

    # SELL DAY 2
    print("%s: %.2f\t%.2f\t%.2f\t%.2f" % (
        dates[i+3], prices['open'].values[2], prices['close'].values[2], prices['low'].values[2], prices['high'].values[2]
    ), end=" ")
    if (prices['high'].values[2] > u1):
        profit_rate = (u1-b1)/b1 * 100
        Result.total_profit_rate += profit_rate
        print_red("SELL at u1 price %.2f, profit: %.2f" % (u1, profit_rate))
        return
    else:
        print("SELL MISS")

    # SELL DAY 3
    print("%s: %.2f\t%.2f\t%.2f\t%.2f" % (
        dates[i+4], prices['open'].values[3], prices['close'].values[3], prices['low'].values[3], prices['high'].values[3]
    ), end=" ")
    if (prices['high'].values[3] > u1):
        profit_rate = (u1-b1)/b1 * 100
        Result.total_profit_rate += profit_rate
        print_red("SELL at u1 price %.2f, profit: %.2f" % (u1, profit_rate))
    else:
        profit_rate = (prices['close'].values[3]-b1)/b1 * 100
        Result.total_profit_rate += profit_rate
        Result.sell_miss_cnt += 1
        print_green("SELL MISS, close price: %.2f, profit: %.2f" % (prices['close'].values[3], profit_rate))

def show_result_of_buy_0985_and_sell_1015_in_3_days(stk, dates, i):
    Result.total_cnt += 1
    prices = repo.get_all_prices_after(stk.code, dates[i])

    # BUY DAY
    print("%s: %.2f\t%.2f\t%.2f\t%.2f" % (
        dates[i+1], prices['open'].values[0], prices['close'].values[0], prices['low'].values[0], prices['high'].values[0]
    ), end=" ")
    buy_price = prices['open'].values[0] * 0.985
    if (prices['low'].values[0] < buy_price):
        print("BUY at 0.985 price %.2f" % (buy_price))
    else:
        print("BUY MISS")
        Result.buy_miss_cnt += 1
        return

    # SELL DAY 1
    print("%s: %.2f\t%.2f\t%.2f\t%.2f" % (
        dates[i+2], prices['open'].values[1], prices['close'].values[1], prices['low'].values[1], prices['high'].values[1]
    ), end=" ")
    open_profit_rate = (prices['open'].values[1]-buy_price)/buy_price * 100
    if (open_profit_rate >= 3):
        Result.total_profit_rate += open_profit_rate
        print_red("SELL at open price %.2f, profit: %.2f" % (prices['open'].values[1], open_profit_rate))
        return
    else:
        sell_price = buy_price * 1.030
        if (prices['high'].values[1] > sell_price):
            profit_rate = 3.0
            Result.total_profit_rate += profit_rate
            print_red("SELL at 1.030 price %.2f, profit: %.2f" % (sell_price, profit_rate))
            return
        else:
            print("SELL MISS")

    cost_price = buy_price
    dip_price = buy_price * 0.940
    if (prices['close'].values[1] < dip_price):
        cost_price = (buy_price + dip_price)/2
        print("BUY A DIP at 0.940 price %.2f, COST %.2f" % (dip_price, cost_price))
    else:
        print("NO BUY A DIP, COST %.2f" % (cost_price))

    # SELL DAY 2
    print("%s: %.2f\t%.2f\t%.2f\t%.2f" % (
        dates[i+3], prices['open'].values[2], prices['close'].values[2], prices['low'].values[2], prices['high'].values[2]
    ), end=" ")
    open_profit_rate = (prices['open'].values[2]-cost_price)/cost_price * 100
    if (open_profit_rate >= 2):
        Result.total_profit_rate += open_profit_rate
        print_red("SELL at open price %.2f, profit: %.2f" % (prices['open'].values[2], open_profit_rate))
        return
    else:
        sell_price = cost_price * 1.020
        if (prices['high'].values[2] > sell_price):
            profit_rate = 2.0
            Result.total_profit_rate += profit_rate
            print_red("SELL at 1.020 price %.2f, profit: %.2f" % (sell_price, profit_rate))
            return
        else:
            print("SELL MISS")

    # SELL DAY 3
    print("%s: %.2f\t%.2f\t%.2f\t%.2f" % (
        dates[i+4], prices['open'].values[3], prices['close'].values[3], prices['low'].values[3], prices['high'].values[3]
    ), end=" ")
    open_profit_rate = (prices['open'].values[3]-cost_price)/cost_price * 100
    if (open_profit_rate >= 1):
        Result.total_profit_rate += open_profit_rate
        print_red("SELL at open price %.2f, profit: %.2f" % (prices['open'].values[3], open_profit_rate))
        return
    else:
        sell_price = cost_price * 1.010
        if (prices['high'].values[3] > sell_price):
            profit_rate = 1.0
            Result.total_profit_rate += profit_rate
            print_red("SELL at 1.010 price %.2f, profit: %.2f" % (sell_price, profit_rate))
            return
        else:
            profit_rate = (prices['close'].values[3]-cost_price)/cost_price * 100
            Result.total_profit_rate += profit_rate
            Result.sell_miss_cnt += 1
            print_green("SELL MISS, close price: %.2f, profit: %.2f" % (prices['close'].values[3], profit_rate))

if __name__ == '__main__':

    repo = Repository()
    dates = repo.get_all_trade_dates_between('000001.SZ', '20210101', '20210115')
    # print(dates)
    for i in range(0, len(dates) - 4):
        date = dates[i]
        print("=== " + date + " ===")

        # if date != '20210107':
        #     continue

        sf = StrategyFactory()
        results = sf.do_strategy(date)
        for s in results:
            for stk in results[s]:
                try:
                    show_basic_info(stk)
                    # show_result_of_min_and_max_price_in_5_days(stk, dates, i)
                    # show_result_of_buy_b1_and_sell_u1_in_3_days(stk, dates, i)
                    show_result_of_buy_0985_and_sell_1015_in_3_days(stk, dates, i)
                except:
                    traceback.print_exc()
                    pass
    print("-----------------------------")
    print("Total count: %d" % (Result.total_cnt))
    print("Buy miss count: %d" % (Result.buy_miss_cnt))
    print("Sell miss count: %d" % (Result.sell_miss_cnt))
    print("Total profit rate: %.2f" % (Result.total_profit_rate))
    