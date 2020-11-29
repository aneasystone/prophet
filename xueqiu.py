import requests
import json

res = requests.get("https://xueqiu.com/service/v5/stock/screener/quote/list?page=1&size=90&order=desc&orderby=percent&order_by=percent&market=CN&type=sh_sz&_=1604935184543", headers={
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36"
})

#print(res.content)
json = json.loads(str(res.content, "utf-8"))
for item in json["data"]["list"]:
    print(item["symbol"])
