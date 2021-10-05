import requests
import time
from lxml import etree

COOKIE = "A7oshHp6j2mA_wOFlqc6yWKJC-vZaz5FsO-y6cSzZs0Yt1RVrPuOVYB_AviX"

def write_thshy(stock, hy):
	with open('shshy.txt', 'a') as f:
		f.write("%s\t%s\t%s\n" % (stock['code'], stock['name'], hy['name']))

def send_ths_request(url):
	global COOKIE
	headers = {
		"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.87 Safari/537.36",
		"Cookie": "v=" + COOKIE
	}
	# time.sleep(10)
	result = requests.get(url, headers=headers)
	if result.status_code == 200:
		return result.content.decode("gbk")
	COOKIE = input("Change cookie: ")
	return send_ths_request(url)

def get_stocks(hy, page):
	url = "https://q.10jqka.com.cn/thshy/detail/field/199112/order/desc/page/" + str(page) + "/ajax/1/code/" + hy['id']
	results = []
	content = send_ths_request(url)
	selector = etree.HTML(content)
	for tr in selector.xpath('/html/body/table/tbody/tr'):
		codes = []
		names = []
		for a in tr.xpath('td[2]/a'):
			codes.append(a.text)
		for a in tr.xpath('td[3]/a'):
			names.append(a.text)
		for i in range(len(codes)):
			results.append({ 'code': codes[i], 'name': names[i] })
	return results

def get_all_stocks(hy):
	for page in range(1,100):
		stocks = get_stocks(hy, page)
		if len(stocks) == 0:
			break
		for stock in stocks:
			print(page, stock['code'], stock['name'])
			write_thshy(stock, hy)

def get_thshy(url):
	results = []
	content = send_ths_request(url)
	selector = etree.HTML(content)
	for tr in selector.xpath('/html/body/table/tbody/tr'):
		for a in tr.xpath('td[2]/a'):
			href = a.get('href')
			url = href[0:len(href)-1]
			results.append({ 'name': a.text, 'id': url[url.rindex('/')+1:] })
	return results

def get_all_thshy():
	hy1 = get_thshy("https://q.10jqka.com.cn/thshy/index/field/199112/order/desc/page/1/ajax/1/")
	print(len(hy1))
	hy2 = get_thshy("https://q.10jqka.com.cn/thshy/index/field/199112/order/desc/page/2/ajax/1/")
	print(len(hy2))
	
	results = []
	for item in hy1:
		results.append(item)
	for item in hy2:
		results.append(item)
	return results

all_thshy = get_all_thshy()
for hy in all_thshy:
	print(hy['id'], hy['name'], '=====================')
	get_all_stocks(hy)
