from stock import Stock
from repository import Repository

class Industry:
	def __init__(self, name) -> None:
		self.name = name
		self.stocks = []
		self.stocks_good = []
		self.stocks_not_bad = []
		self.stocks_not_good = []

industry_map = {}

def is_open(stk, i):
	return (stk.ma10[i] > stk.ma20[i] > stk.ma30[i] and stk.ma5[i] > stk.ma20[i]) or (stk.ma5[i] > stk.ma10[i] > stk.ma20[i] and stk.ma10[i] > stk.ma30[i])

def is_over_ma10(stk, i):
	_low = stk.prices['low'].values[i]
	_ma10 = stk.ma10[i]
	return _low > _ma10

trade_date = '20210930'
repo = Repository()
stocks = repo.get_all_stocks()
for ss in stocks:
	stk = Stock(ss['name'], ss['ts_code'], trade_date)
	if stk.init():
		if stk.industry not in industry_map:
			industry_map[stk.industry] = Industry(stk.industry)
		print(stk.code, stk.name)
		industry_map[stk.industry].stocks.append(stk)
		if is_open(stk, -1):
			if is_over_ma10(stk, -1):
				industry_map[stk.industry].stocks_good.append(stk)
			else:
				industry_map[stk.industry].stocks_not_bad.append(stk)
		else:
			industry_map[stk.industry].stocks_not_good.append(stk)
for industry in industry_map:
	all = len(industry_map[industry].stocks)
	good = len(industry_map[industry].stocks_good)
	not_bad = len(industry_map[industry].stocks_not_bad)
	not_good = len(industry_map[industry].stocks_not_good)
	print("{0:<10}\t{1:<10}\t{2:<10}\t{3:<10}\t{4:<10}\t{5:<10}\t{6:<10}\t{7:<10}".format(
		"行业", "总数", "很好", "还行", "挺差", "很好率", "还行率", "挺差率"))
	print("{0:<10}\t{1:<10}\t{2:<10}\t{3:<10}\t{4:<10}\t{5:<10}\t{6:<10}\t{7:<10}".format(
		industry, 
		all,
		good,
		not_bad,
		not_good,
		"%.2f" % (good/all*100),
		"%.2f" % (not_bad/all*100),
		"%.2f" % (not_good/all*100)))
