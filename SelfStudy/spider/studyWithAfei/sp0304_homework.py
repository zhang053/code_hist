import requests
from lxml import etree

url = "https://www.xunsouzaixian.com/"
headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36 Edg/139.0.0.0"
}

request = requests.get(url, headers=headers)
rq_html = request.text

# with open("0305_XunSou.html", "w", encoding="utf-8") as f:
#     f.write(request.text)

HTML = etree.HTML(rq_html)

# titles = HTML.xpath('//dl[@class="homepcat"]/dt/a/text()')
# print(titles)
# # element = HTML.xpath('//dl[@class="homepcat"]/dd/a/text()')
# # print(element)

result = []

titles = HTML.xpath('//dl[@class="homepcat"]')
# 先找到规律，然后找到统一的父级，然后 ./
for tit in titles:
    title = tit.xpath("./dt/a/text()")
    elements = tit.xpath("./dd/a/text()")
    result.append({"title": title, "element": elements})
print(*result, sep="\n")

# xpath语法对于python来说只是一个字符串，所以可以用print(f'   )来进行编辑
