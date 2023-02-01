import os
from repository import Repository

repo = Repository()

class Result:

	def __init__(self, file, code, name, industry, big_money_left, price_drop) -> None:
		self.file = file
		self.code = code
		self.name = name
		self.industry = industry
		self.big_money_left = big_money_left
		self.price_drop = price_drop

def bytes_to_int(x:bytes):
	return int.from_bytes(x, 'little')

def read_sel_file(file_name):
	stocks = []
	with open('./sel/' + file_name, 'rb') as f:
		header = bytearray()
		byte = f.read(1)
		while byte != b'\x00':
			header += bytearray(byte)
			byte = f.read(1)
		len = bytes_to_int(bytes(header))
		for _ in range(len):
			stock = ''
			type = f.read(2)
			if type[0] == 0x07 and type[1] == 0x11:
				stock += 'SH'
			else:
				stock += 'SZ'
			byte = f.read(6)
			stock = byte.decode() + '.' + stock
			stocks.append(stock)
	return stocks

def get_all_sel_files():
	sel_files = []
	for path, dir_list, file_list in os.walk('./sel/'):
		for file_name in file_list:
			sel_files.append(file_name)
	return sel_files

def get_big_money_left(stock, days):
	big_money_left = 0
	all_money_flow = repo.get_all_money_flow(stock)
	for i in range(days):
		big_money = get_big_money(all_money_flow, -1-i)
		big_money_left += big_money
	return big_money_left

def get_big_money(money_flow, i):
	buy_lg_amount = money_flow['buy_lg_amount'].values[i]
	sell_lg_amount = money_flow['sell_lg_amount'].values[i]
	buy_elg_amount = money_flow['buy_elg_amount'].values[i]
	sell_elg_amount = money_flow['sell_elg_amount'].values[i]
	return buy_lg_amount+buy_elg_amount-sell_lg_amount-sell_elg_amount

def get_price_drop(stock, days):
	all_prices = repo.get_all_prices(stock)
	highest_price = 0
	close_price = all_prices['close'].values[-1]
	for i in range(days):
		open = all_prices['open'].values[-1-i]
		close = all_prices['close'].values[-1-i]
		highest_price = max(open, close, highest_price)
	return (1 - close_price / highest_price) * 100

def calc_stocks(stocks, file):
	results = []
	for stock in stocks:
		basic = repo.get_stock_basic(stock)
		big_money_left = get_big_money_left(stock, count-i)
		price_drop = get_price_drop(stock, count-i)
		if big_money_left > -1000 and price_drop > 7:
			results.append(Result(file, basic['ts_code'], basic['name'], basic['industry'], big_money_left, price_drop))
	return results

if __name__ == '__main__':
	files = get_all_sel_files()
	count = len(files)
	results = []
	for i, file in enumerate(files):
		stocks = read_sel_file(file)
		results.extend(calc_stocks(stocks, file))
	results = sorted(results, key=lambda r : r.price_drop, reverse=True)
	for result in results:
		print("{0}\t{1}\t{2:{6}<10}\t{3:{6}<10}\t{4}\t{5}".format(
			result.file, #0
			result.code, #1
			result.name, #2
			result.industry, #3
			"%.0f" % result.big_money_left, #4
			"%.2f" % result.price_drop, #5
			chr(12288) #6
		))
