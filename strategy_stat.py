import traceback
from stock import Stock
from repository import Repository
from strategy_factory import StrategyFactory

repo = Repository()
sf = StrategyFactory(repo)

X_MIN = 1
X_MAX = 20
Y_MIN = 1
Y_MAX = 10
N_MIN = 1
N_MAX = 20

def is_match(after_prices, x, y, n):
    buy_price = after_prices['open'].values[0]
    for i in range(1, n+1):
        close_price = after_prices['close'].values[i]
        high_price = after_prices['high'].values[i]
        if high_price >= buy_price * (1+x/100):
            return True
        if close_price <= buy_price * (1-y/100):
            return False
    return False

def get_profit_probability_o(result, x, y, n):
    total = result['total']
    match = result['match']
    if total == 0:
        return "--"
    return "%s/%s" % (match, total)

def get_profit_probability(result, x, y, n):
    total = result['total']
    match = result['match']
    if total == 0:
        return "--"
    p = match / total * 100
    return "%.2f" % (p)

def get_daily_profit_rate(result, x, y, n):
    total = result['total']
    match = result['match']
    if total == 0:
        return "--"
    p = match / total
    # print("%.2f %s %s" % (p, x, y))
    z = (x+y) * p - y
    # print("%.2f %.2f" % (z, z/n))
    return "%.4f" % (z/n)

def write_month_stat(month, group):
    for strategy in group:
        items = group[strategy]
        with open('stat/' + strategy + '-' + month, 'w') as f:
            for n in range(N_MIN, N_MAX+1):
                f.write("%s HOLDS %s DAYS\n" % (strategy, n))
                for x in range(X_MIN, X_MAX+1):
                    for y in range(Y_MIN, Y_MAX+1):
                        key = "%s-%s-%s" % (x, y, n)
                        f.write("%s\t" % (get_daily_profit_rate(items[key], x, y, n)))
                    f.write("\n")
                for x in range(X_MIN, X_MAX+1):
                    for y in range(Y_MIN, Y_MAX+1):
                        key = "%s-%s-%s" % (x, y, n)
                        f.write("%s\t" % (get_profit_probability(items[key], x, y, n)))
                    f.write("\n")
                for x in range(X_MIN, X_MAX+1):
                    for y in range(Y_MIN, Y_MAX+1):
                        key = "%s-%s-%s" % (x, y, n)
                        f.write("%s\t" % (get_profit_probability_o(items[key], x, y, n)))
                    f.write("\n")
                    
def get_month_stat(month_from, month_to):
    group = {}
    dates = repo.get_all_trade_dates_between('000001.SZ', month_from + '01', month_to + '01')
    for date in dates:
        print(date)
        stks = sf.do_strategy(date)
        for strategy in stks:
            if strategy not in group:
                group[strategy] = {}
            for stk in stks[strategy]:
                print("%s %s %s" % (date, stk.code, strategy))
                after_prices = repo.get_all_prices_after(stk.code, date)
                if len(after_prices['open'].values) <= 20:
                    print("ignore")
                    continue
                for n in range(N_MIN, N_MAX+1):
                    for x in range(X_MIN, X_MAX+1):
                        for y in range(Y_MIN, Y_MAX+1):
                            key = "%s-%s-%s" % (x, y, n)
                            if key not in group[strategy]:
                                group[strategy][key] = { "total": 0, "match": 0 }
                            group[strategy][key]["total"] += 1
                            match = is_match(after_prices, x, y, n)
                            if match:
                                group[strategy][key]["match"] += 1
    write_month_stat(month_from, group)
    
def show_month_stat():
    month_list = [
        # "202001",
        # "202002",
        # "202003",
        # "202004",
        # "202005",
        # "202006",
        # "202007",
        # "202008",
        # "202009",
        # "202010",
        # "202011",
        # "202012",
        # "202101",
        # "202102",
        "202103",
        "202104"
    ]
    for i in range(len(month_list) - 1):
        get_month_stat(month_list[i], month_list[i+1])


def get_profit(code, date):
    after_prices = repo.get_all_prices_after(code, date)
    buy_price = after_prices['open'].values[0]
    open_price = after_prices['close'].values[1]
    if open_price >= buy_price * 1.03:
        return (open_price-buy_price)/buy_price*100
    high_price = after_prices['high'].values[1]
    if high_price >= buy_price * 1.03:
        return 3
    close_price = after_prices['close'].values[1]
    return (close_price-buy_price)/buy_price*100

def get_profit_no_limit(code, date):
    after_prices = repo.get_all_prices_after(code, date)
    buy_price = after_prices['open'].values[0]
    for i in range(1, len(after_prices['close'].values)-1):
        prev_close_price = after_prices['close'].values[i-1]
        close_price = after_prices['close'].values[i]
        if (close_price-buy_price)/buy_price < -0.03:
            print("%.2f %.2f %d" % (buy_price, close_price, i))
            return (close_price-buy_price)/buy_price
        if (close_price-prev_close_price)/prev_close_price < -0.03:
            print("%.2f %.2f %d" % (buy_price, close_price, i))
            return (close_price-buy_price)/buy_price
    now_price = after_prices['close'].values[-1]
    print("%.2f %.2f now" % (buy_price, now_price))
    return (now_price-buy_price)/buy_price

def run_profit_test():
    dates = repo.get_all_trade_dates_between('000001.SZ', '20210201', '20210301')
    sum = 0
    total = 0
    for date in dates:
        print(date)
        stks = sf.do_strategy(date)
        for strategy in stks:
            for stk in stks[strategy]:
                profit = get_profit_no_limit(stk.code, date)
                print("%s %s %s %.2f" % (date, stk.code, strategy, profit))
                sum += profit
                total += 1
    if total > 0:
        print("%.2f / %d = %.2f" % (sum, total, sum/total))

if __name__ == '__main__':
    # show_month_stat()
    run_profit_test()