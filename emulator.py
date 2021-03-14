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

def print_result(stk, profit_rate, buy_miss = False):
    if buy_miss:
        info = "{0:{4}<10}\t{1:<10}\t{2:<10}\t{3:{4}<10}\t{5}\tMISS".format(
            stk.name, stk.code, str(stk.close), stk.industry, chr(12288), ','.join(stk.features))
        print(info)
    else:
        info = "{0:{4}<10}\t{1:<10}\t{2:<10}\t{3:{4}<10}\t{5}\t{6}".format(
            stk.name, stk.code, str(stk.close), stk.industry, chr(12288), ','.join(stk.features), "%.2f" % profit_rate)
        if profit_rate > 0:
            print_red(info)
        else:
            print_green(info)

def show_result_of_buy_open_and_sell_trend_break(stk, dates, i):
    Result.total_cnt += 1
    prices = repo.get_all_prices_after(stk.code, dates[i])

    # BUY DAY
    buy_price = prices['open'].values[0]
    highest_price = prices['high'].values[0]
    day = 1
    
    while True:
        low_price = prices['low'].values[day]
        high_price = prices['high'].values[day]
        # print(day, low_price, high_price, highest_price)
        if (low_price-highest_price)/highest_price < -0.06:
            sell_price = prices['close'].values[day]
            profit_rate = (sell_price-buy_price)/buy_price * 100
            Result.total_profit_rate += profit_rate
            print_result(stk, profit_rate)
            break
        else:
            highest_price = high_price if high_price > highest_price else highest_price
        day += 1


def show_result_of_buy_close_and_sell_103_in_3_days(stk, dates, i):
    Result.total_cnt += 1
    prices = repo.get_all_prices_after(stk.code, dates[i])

    # BUY DAY
    buy_price = stk.close

    # SELL DAY 1
    open_profit_rate = (prices['open'].values[0]-buy_price)/buy_price * 100
    if (open_profit_rate >= 3):
        Result.total_profit_rate += open_profit_rate
        # print_red("SELL at open price %.2f, profit: %.2f" % (prices['open'].values[0], open_profit_rate))
        return print_result(stk, open_profit_rate)
    else:
        sell_price = buy_price * 1.030
        if (prices['high'].values[0] > sell_price):
            profit_rate = 3.0
            Result.total_profit_rate += profit_rate
            # print_red("SELL at 1.030 price %.2f, profit: %.2f" % (sell_price, profit_rate))
            return print_result(stk, profit_rate)
        else:
            # print("SELL MISS")
            pass

    # SELL DAY 2
    open_profit_rate = (prices['open'].values[1]-buy_price)/buy_price * 100
    if (open_profit_rate >= 3):
        Result.total_profit_rate += open_profit_rate
        # print_red("SELL at open price %.2f, profit: %.2f" % (prices['open'].values[1], open_profit_rate))
        return print_result(stk, open_profit_rate)
    else:
        sell_price = buy_price * 1.030
        if (prices['high'].values[1] > sell_price):
            profit_rate = 3.0
            Result.total_profit_rate += profit_rate
            # print_red("SELL at 1.030 price %.2f, profit: %.2f" % (sell_price, profit_rate))
            return print_result(stk, profit_rate)
        else:
            # print("SELL MISS")
            pass

    # SELL DAY 3
    open_profit_rate = (prices['open'].values[2]-buy_price)/buy_price * 100
    if (open_profit_rate >= 3):
        Result.total_profit_rate += open_profit_rate
        # print_red("SELL at open price %.2f, profit: %.2f" % (prices['open'].values[2], open_profit_rate))
        return print_result(stk, open_profit_rate)
    else:
        sell_price = buy_price * 1.030
        if (prices['high'].values[2] > sell_price):
            profit_rate = 3.0
            Result.total_profit_rate += profit_rate
            # print_red("SELL at 1.030 price %.2f, profit: %.2f" % (sell_price, profit_rate))
            return print_result(stk, profit_rate)
        else:
            profit_rate = (prices['close'].values[2]-buy_price)/buy_price * 100
            Result.total_profit_rate += profit_rate
            Result.sell_miss_cnt += 1
            # print_green("SELL MISS, close price: %.2f, profit: %.2f" % (prices['close'].values[2], profit_rate))
            print_result(stk, profit_rate)

def show_result_of_buy_0985_and_sell_1015_in_3_days(stk, dates, i):
    Result.total_cnt += 1
    prices = repo.get_all_prices_after(stk.code, dates[i])

    # BUY DAY
    # print("%s: %.2f\t%.2f\t%.2f\t%.2f" % (
    #     dates[i+1], prices['open'].values[0], prices['close'].values[0], prices['low'].values[0], prices['high'].values[0]
    # ), end=" ")
    buy_price = prices['open'].values[0] * 0.985
    if (prices['low'].values[0] < buy_price):
        # print("BUY at 0.985 price %.2f" % (buy_price))
        pass
    else:
        # print("BUY MISS")
        Result.buy_miss_cnt += 1
        return print_result(stk, 0, True)

    # SELL DAY 1
    # print("%s: %.2f\t%.2f\t%.2f\t%.2f" % (
    #     dates[i+2], prices['open'].values[1], prices['close'].values[1], prices['low'].values[1], prices['high'].values[1]
    # ), end=" ")
    open_profit_rate = (prices['open'].values[1]-buy_price)/buy_price * 100
    if (open_profit_rate >= 3):
        Result.total_profit_rate += open_profit_rate
        # print_red("SELL at open price %.2f, profit: %.2f" % (prices['open'].values[1], open_profit_rate))
        return print_result(stk, open_profit_rate)
    else:
        sell_price = buy_price * 1.030
        if (prices['high'].values[1] > sell_price):
            profit_rate = 3.0
            Result.total_profit_rate += profit_rate
            # print_red("SELL at 1.030 price %.2f, profit: %.2f" % (sell_price, profit_rate))
            return print_result(stk, profit_rate)
        else:
            # print("SELL MISS")
            pass

    cost_price = buy_price
    dip_price = buy_price * 0.940
    if (prices['close'].values[1] < dip_price):
        cost_price = (buy_price + dip_price)/2
        # print("BUY A DIP at 0.940 price %.2f, COST %.2f" % (dip_price, cost_price))
    else:
        # print("NO BUY A DIP, COST %.2f" % (cost_price))
        pass

    # SELL DAY 2
    # print("%s: %.2f\t%.2f\t%.2f\t%.2f" % (
    #     dates[i+3], prices['open'].values[2], prices['close'].values[2], prices['low'].values[2], prices['high'].values[2]
    # ), end=" ")
    open_profit_rate = (prices['open'].values[2]-cost_price)/cost_price * 100
    if (open_profit_rate >= 2):
        Result.total_profit_rate += open_profit_rate
        # print_red("SELL at open price %.2f, profit: %.2f" % (prices['open'].values[2], open_profit_rate))
        return print_result(stk, open_profit_rate)
    else:
        sell_price = cost_price * 1.020
        if (prices['high'].values[2] > sell_price):
            profit_rate = 2.0
            Result.total_profit_rate += profit_rate
            # print_red("SELL at 1.020 price %.2f, profit: %.2f" % (sell_price, profit_rate))
            return print_result(stk, profit_rate)
        else:
            # print("SELL MISS")
            pass

    # SELL DAY 3
    # print("%s: %.2f\t%.2f\t%.2f\t%.2f" % (
    #     dates[i+4], prices['open'].values[3], prices['close'].values[3], prices['low'].values[3], prices['high'].values[3]
    # ), end=" ")
    open_profit_rate = (prices['open'].values[3]-cost_price)/cost_price * 100
    if (open_profit_rate >= 1):
        Result.total_profit_rate += open_profit_rate
        # print_red("SELL at open price %.2f, profit: %.2f" % (prices['open'].values[3], open_profit_rate))
        return print_result(stk, open_profit_rate)
    else:
        sell_price = cost_price * 1.010
        if (prices['high'].values[3] > sell_price):
            profit_rate = 1.0
            Result.total_profit_rate += profit_rate
            # print_red("SELL at 1.010 price %.2f, profit: %.2f" % (sell_price, profit_rate))
            return print_result(stk, profit_rate)
        else:
            profit_rate = (prices['close'].values[3]-cost_price)/cost_price * 100
            Result.total_profit_rate += profit_rate
            Result.sell_miss_cnt += 1
            # print_green("SELL MISS, close price: %.2f, profit: %.2f" % (prices['close'].values[3], profit_rate))
            print_result(stk, profit_rate)

def select_stocks(results):
    selected = []
    for s in results:
        for stk in results[s]:
            selected.append(stk)
    return selected

if __name__ == '__main__':

    repo = Repository()
    dates = repo.get_all_trade_dates_between('000001.SZ', '20200101', '20210101')
    # print(dates)
    for i in range(0, len(dates)):
        date = dates[i]
        print("=== " + date + " ===")

        # if date != '20210111':
        #     continue

        Result.total_cnt = 0
        Result.buy_miss_cnt = 0
        Result.sell_miss_cnt = 0
        Result.total_profit_rate = 0

        sf = StrategyFactory(repo)
        results = sf.do_strategy(date)
        selected = select_stocks(results)
        for stk in selected:
            try:
                # show_result_of_buy_0985_and_sell_1015_in_3_days(stk, dates, i)
                # show_result_of_buy_close_and_sell_103_in_3_days(stk, dates, i)
                show_result_of_buy_open_and_sell_trend_break(stk, dates, i)
            except:
                traceback.print_exc()
                pass

        print("-----------------------------")
        print("Total count: %d" % (Result.total_cnt))
        print("Buy miss count: %d" % (Result.buy_miss_cnt))
        print("Sell miss count: %d" % (Result.sell_miss_cnt))
        print("Total profit rate: %.2f" % (Result.total_profit_rate))
    