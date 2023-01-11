import traceback
from stock import Stock
from repository import Repository
from strategy_factory import StrategyFactory

repo = Repository()

def get_highest_price(after_prices):
    high = after_prices['high'].values[1]
    for i in range(2, 10):
        if (len(after_prices['high'].values) < i+1):
            break
        if after_prices['high'].values[i] > high:
            high = after_prices['high'].values[i]
    return high

def get_profit_rate(close, low, high, buy_rate):
    buy = close * buy_rate
    if low > buy:
        return "MISS"
    return "%.2f" % ((high-buy)/buy*100)

def show_buy_result(trade_date, stk):
    after_prices = repo.get_all_prices_after(stk.code, trade_date)
    if (len(after_prices['open'].values) < 2):
        return "--"

    # 10日内的最高价
    high = get_highest_price(after_prices)
    # 第2天最低价
    low = after_prices['low'].values[0]

    return "%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s" % (
        get_profit_rate(stk.close, low, high, 1.00),
        get_profit_rate(stk.close, low, high, 0.99),
        get_profit_rate(stk.close, low, high, 0.98),
        get_profit_rate(stk.close, low, high, 0.97),
        get_profit_rate(stk.close, low, high, 0.96),
        get_profit_rate(stk.close, low, high, 0.95),
        get_profit_rate(stk.close, low, high, 0.94),
        get_profit_rate(stk.close, low, high, 0.93),
        get_profit_rate(stk.close, low, high, 0.92),
        get_profit_rate(stk.close, low, high, 0.91)
    )

def show_stock_result(trade_date, stk):
    info = "{0:<10}\t{1:{6}<10}\t{2:<10}\t{3:<10}\t{4:{6}<10}\t{5}\t{7}".format(
            trade_date,
            stk.name,
            stk.code,
            str(stk.close),
            stk.industry,
            ", ".join(stk.features),
            chr(12288), show_buy_result(trade_date, stk))
    print(info)

def int_to_bytes(x: int) -> bytes:
    return x.to_bytes((x.bit_length() + 7) // 8, 'little')

def write_sel(strategy, trade_date, stks):
    if len(stks) == 0:
        return
    with open('sel/' + trade_date + '_' + strategy + '.sel', 'wb') as f:
        f.write(int_to_bytes(len(stks)))
        f.write(bytes([0]))
        for stk in stks:
            xs = stk.code.split('.')
            if xs[1] == 'SH':
                f.write(bytes([0x07, 0x11]))
                f.write(bytes(xs[0], encoding='utf-8'))
            else:
                f.write(bytes([0x07, 0x21]))
                f.write(bytes(xs[0], encoding='utf-8'))

def show_recommended(trade_date):

    sf = StrategyFactory(repo)
    results = sf.do_strategy(trade_date)

    for s in results:
        print("=== " + trade_date + " ===")
        print("=== " + s + " ===")
        stks = results[s]
        for stk in stks:
            show_stock_result(trade_date, stk)
        write_sel(s, trade_date, stks)

if __name__ == '__main__':

    trade_date = '20230109'
    show_recommended(trade_date)
    
    # dates = repo.get_all_trade_dates_between('000001.SZ', '20220401', '20230101')
    # for date in dates:
    #     show_recommended(date)
