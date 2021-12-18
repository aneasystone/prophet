import traceback
from stock import Stock
from updator import Updator
from repository import Repository

repo = Repository()

class Industry:
	def __init__(self, name) -> None:
		self.name = name
		self.stocks = []
		self.stocks_level = {
			"0": [],
			"1": [],
			"2": [],
			"3": [],
			"4": [],
			"5": [],
			"6": []
		}

def get_stock_level(stk, i):
	arr = [stk.ma30[i], stk.ma20[i], stk.ma10[i], stk.ma5[i]]
	steps = 0
	n = len(arr)
	for i in range(n-1):
		for j in range(0, n-i-1):
			if arr[j] > arr[j + 1] :
				arr[j], arr[j + 1] = arr[j + 1], arr[j]
				steps += 1
	return steps

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
				else:
					# print(stk.code, stk.name, stk.industry)
					continue
				if stk.industry not in industry_map:
					industry_map[stk.industry] = Industry(stk.industry)
				industry_map[stk.industry].stocks.append(stk)
				level = get_stock_level(stk, -1)
				# print(stk.code, stk.name, stk.industry, level)
				industry_map[stk.industry].stocks_level[str(level)].append(stk)
		except:
			# traceback.print_exc()
			pass
	return industry_map

def write_good_industry_stocks(trade_date, results, industry_map):
	for result in results:
		if result['score'] < 60:
			continue
		stocks = []
		industry = result['industry']
		for stock in industry_map[industry].stocks_level["0"]:
			stocks.append(stock)
		for stock in industry_map[industry].stocks_level["1"]:
			stocks.append(stock)
		for stock in industry_map[industry].stocks_level["2"]:
			stocks.append(stock)
		write_sel(trade_date, industry, stocks)

def int_to_bytes(x: int) -> bytes:
    return x.to_bytes((x.bit_length() + 7) // 8, 'little')

def write_sel(trade_date, industry, stks):
    with open('sel/' + trade_date + '_' + industry + '.sel', 'wb') as f:
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
		f.write("%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%.2f\n" % (
			trade_date,
			result['industry'], 
			result['all'],
			result['level_0'],
			result['level_1'],
			result['level_2'],
			result['level_3'],
			result['level_4'],
			result['level_5'],
			result['level_6'],
			result['score']
		))

def show_industry_trend_result(trade_date, industry_map):
	results = []
	for industry in industry_map:
		all = len(industry_map[industry].stocks)
		level_0 = len(industry_map[industry].stocks_level["0"])
		level_1 = len(industry_map[industry].stocks_level["1"])
		level_2 = len(industry_map[industry].stocks_level["2"])
		level_3 = len(industry_map[industry].stocks_level["3"])
		level_4 = len(industry_map[industry].stocks_level["4"])
		level_5 = len(industry_map[industry].stocks_level["5"])
		level_6 = len(industry_map[industry].stocks_level["6"])
		results.append({
			'industry': industry,
			'all': all,
			'level_0': level_0,
			'level_1': level_1,
			'level_2': level_2,
			'level_3': level_3,
			'level_4': level_4,
			'level_5': level_5,
			'level_6': level_6,
			'score': (level_0*6+level_1*5+level_2*4+level_3*3+level_4*2+level_5*1+level_6*0)*100/6/all
		})
	results = sorted(results, key=lambda x:x['score'], reverse=True)
	write_good_industry_stocks(trade_date, results, industry_map)

	print("{0:<15}\t{1:<10}\t{2:<10}\t{3:<10}\t{4:<10}\t{5:<10}\t{6:<10}\t{7:<10}\t{8:<10}\t{9:<10}".format(
		"行业", "总数", "零级", "一级", "二级", "三级", "四级", "五级", "六级", "行业评分"))
	for result in results:
		write_result(trade_date, result)
		print("{0:<15}\t{1:<10}\t{2:<10}\t{3:<10}\t{4:<10}\t{5:<10}\t{6:<10}\t{7:<10}\t{8:<10}\t{9:<10}".format(
			result['industry'], 
			result['all'],
			result['level_0'],
			result['level_1'],
			result['level_2'],
			result['level_3'],
			result['level_4'],
			result['level_5'],
			result['level_6'],
			"%.2f" % result['score']))

trade_date = '20211206'
updator = Updator()
updator.update_all_daily_by_trade_date(trade_date)
industry_map = get_industry_map(trade_date)
show_industry_trend_result(trade_date, industry_map)

# dates = repo.get_all_trade_dates_between('000001.SZ', '20200101', '20210101')
# for date in dates:
# 	industry_map = get_industry_map(date)
# 	show_industry_trend_result(date, industry_map)
