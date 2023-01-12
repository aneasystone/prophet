import os
from repository import Repository

repo = Repository()

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
	return 1

def get_price_drop(stock, days):
	return 1

if __name__ == '__main__':
	files = get_all_sel_files()
	count = len(files)
	for i, file in enumerate(files):
		stocks = read_sel_file(file)
		print(count-i, file, len(stocks))
		for stock in stocks:
			basic = repo.get_stock_basic(stock)
			big_money_left = get_big_money_left(stock, count-i)
			price_drop = get_price_drop(stock, count-i)
			print("%s\t%s\t%s\t%s\t%s" % (
				basic['ts_code'], basic['name'], basic['industry'], big_money_left, price_drop
			))
