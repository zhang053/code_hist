import requests

url1 = "https://www.baidu.com"

r = requests.get(url1)
r.encoding = r.apparent_encoding

with open("baidu.html", "w", encoding="utf-8") as f:
    f.write(r.text)
