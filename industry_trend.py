from stock import Stock
from repository import Repository

repo = Repository()

class Industry:
	def __init__(self, name) -> None:
		self.name = name
		self.stocks = []
		self.stocks_good = []
		self.stocks_not_bad = []
		self.stocks_not_good = []

def is_open(stk, i):
	return (stk.ma10[i] > stk.ma20[i] > stk.ma30[i] and stk.ma5[i] > stk.ma20[i]) or (stk.ma5[i] > stk.ma10[i] > stk.ma20[i] and stk.ma10[i] > stk.ma30[i])

def is_over_ma10(stk, i):
	_low = stk.prices['low'].values[i]
	_ma10 = stk.ma10[i]
	return _low > _ma10

def init_thshy_map():
	thshy_map = {}
	with open('shshy.txt', 'r') as f:
		for line in f.read().splitlines():
			code = line.split('\t')[0]
			hy = line.split('\t')[2] + "[THS]"
			if code.startswith('6'):
				thshy_map[code + ".SH"] = hy
			else:
				thshy_map[code + ".SZ"] = hy
	return thshy_map

def get_industry_map(trade_date):
	print("=== " + trade_date + " ===")
	thshy_map = init_thshy_map()
	industry_map = {}
	stocks = repo.get_all_stocks()
	for ss in stocks:
		try:
			stk = Stock(ss['name'], ss['ts_code'], trade_date)
			if stk.init():
				if stk.code in thshy_map:
					stk.industry = thshy_map[stk.code]
				# else:
				# 	print(stk.code, stk.name, stk.industry)
				if stk.industry not in industry_map:
					industry_map[stk.industry] = Industry(stk.industry)
				# print(stk.code, stk.name)
				industry_map[stk.industry].stocks.append(stk)
				if is_open(stk, -1):
					if is_over_ma10(stk, -1):
						industry_map[stk.industry].stocks_good.append(stk)
					else:
						industry_map[stk.industry].stocks_not_bad.append(stk)
				else:
					industry_map[stk.industry].stocks_not_good.append(stk)
		except:
			pass
	return industry_map

def get_top5_industry_stocks(results, industry_map):
	stocks = []
	for i in range(5):
		industry = results[i]['industry']
		for stock in industry_map[industry].stocks_good:
			stocks.append(stock)
	return stocks

def int_to_bytes(x: int) -> bytes:
    return x.to_bytes((x.bit_length() + 7) // 8, 'little')

def write_sel(trade_date, stks):
    with open('sel/' + trade_date + '.sel', 'wb') as f:
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

def write_result(trade_date, result):
	with open('results.txt', 'a') as f:
		f.write("%s\t%s\t%s\t%s\t%s\t%s\t%.2f\t%.2f\t%.2f\n" % (
			trade_date,
			result['industry'], 
			result['all'],
			result['good'],
			result['not_bad'],
			result['not_good'],
			result['good_rate'],
			result['not_bad_rate'],
			result['not_good_rate']
		))

def show_industry_trend_result(trade_date, industry_map):
	results = []
	for industry in industry_map:
		all = len(industry_map[industry].stocks)
		good = len(industry_map[industry].stocks_good)
		not_bad = len(industry_map[industry].stocks_not_bad)
		not_good = len(industry_map[industry].stocks_not_good)
		results.append({
			'industry': industry,
			'all': all,
			'good': good,
			'not_bad': not_bad,
			'not_good': not_good,
			'good_rate': good/all*100,
			'not_bad_rate': not_bad/all*100,
			'not_good_rate': not_good/all*100
		})
	results = sorted(results, key=lambda x:x['good_rate'], reverse=True)
	stocks = get_top5_industry_stocks(results, industry_map)
	write_sel(trade_date, stocks)

	print("{0:<15}\t{1:<10}\t{2:<10}\t{3:<10}\t{4:<10}\t{5:<10}\t{6:<10}\t{7:<10}".format(
		"行业", "总数", "很好", "还行", "挺差", "很好率", "还行率", "挺差率"))
	for result in results:
		write_result(trade_date, result)
		print("{0:<15}\t{1:<10}\t{2:<10}\t{3:<10}\t{4:<10}\t{5:<10}\t{6:<10}\t{7:<10}".format(
			result['industry'], 
			result['all'],
			result['good'],
			result['not_bad'],
			result['not_good'],
			"%.2f" % result['good_rate'],
			"%.2f" % result['not_bad_rate'],
			"%.2f" % result['not_good_rate']))

trade_date = '20210930'
industry_map = get_industry_map(trade_date)
show_industry_trend_result(trade_date, industry_map)

# dates = repo.get_all_trade_dates_between('000001.SZ', '20200101', '20220101')
# for date in dates:
# 	industry_map = get_industry_map(date)
# 	show_industry_trend_result(date, industry_map)
