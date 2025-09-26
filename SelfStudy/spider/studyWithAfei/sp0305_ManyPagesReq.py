# 遇到有很多页数网站，寻找网页链接的规律
# 豆瓣网站为例

# 第二页，https://movie.douban.com/top250?start=25&filter=    因为filter=后面没有值，就是说这个filter有没有都没有影响
# 第三页，https://movie.douban.com/top250?start=50
# 第四页，https://movie.douban.com/top250?start=75
# 第五页，https://movie.douban.com/top250?start=100
# .....
# 最后的start=225

# 查询字段 ？键=值 & 键=值 & 键=值 &。。。。

import requests
import re
from lxml import etree


cookies = {
    "bid": "0_w3By5v7uU",
    "_pk_id.100001.4cf6": "796df7ae0d43c7e8.1756823549.",
    "__utmc": "30149280",
    "__utmz": "30149280.1756823550.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none)",
    "__utmc": "223695111",
    "__utmz": "223695111.1756823550.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none)",
    "__yadk_uid": "CapdE8sEJb4Dh6FWMXkHWKWbJH87lvmw",
    "ll": '"108169"',
    "_vwo_uuid_v2": "D9FF1219C93C5F9C544491F85609A49B4|201699e30da01d47f70825bcd930312b",
    "cto_bundle": "9O-uqV9Tdzc2bnlwUFpCZjNLb21uM092VzVYdmx5YW1UeDdlaEZQOTNpJTJCWlRwVkhTWG5iemZUbE5HNXFUbG1jTUU5eWtSWksxaFRRc2tFd29hUUlCMGE5Umh5MW0wM1VhR2tCaWhISUdEclF0SjUlMkJaQyUyRiUyQlpQb0Z4Nk4lMkI4VEZIcDA0V1BtdjhnSGNKaWdIZmdQTW1uQngwdE5BJTNEJTNE",
    "ap_v": "0,6.0",
    "_pk_ses.100001.4cf6": "1",
    "__utma": "30149280.1451705010.1756823550.1756826591.1757215808.3",
    "__utma": "223695111.149158184.1756823550.1756826591.1757215808.3",
    "__utmb": "223695111.0.10.1757215808",
    "__utmt_t1": "1",
    "__utmb": "30149280.3.8.1757215808",
    "__gads": "ID=9fc49e77f9e45c41:T=1756823551:RT=1757215817:S=ALNI_MaNDmzc7kPM6YHnOc-oVc0GW7ensw",
    "__gpi": "UID=0000118cd3db64da:T=1756823551:RT=1757215817:S=ALNI_MaQGb4GsvlQFPy6q-qGfU_vAk9lgA",
    "__eoi": "ID=078084a8688bd4a0:T=1756823551:RT=1757215817:S=AA-AfjbGTDKREMV1HHZ_19W4f9dY",
    "FCNEC": "%5B%5B%22AKsRol9myJp-TtGKTs1J3QVSm-po-jtRdr6YRdTo_hgcUgJtliYTFvX60HmdcJWAWtKCu0fG4EE-AhnMgkX3FMcSX3QTI1f7FsJeFdKnoSzbJvKqYONyrdbLkbEFWwDL2J5PhKYVTXtmG5zOWDYMH4HxLeO5-7x6uA%3D%3D%22%5D%5D",
    "RT": "s=1757215834424&r=https%3A%2F%2Fmovie.douban.com%2Ftop250",
}

headers = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "accept-language": "ja,en;q=0.9,en-GB;q=0.8,en-US;q=0.7,zh-CN;q=0.6,zh;q=0.5",
    "cache-control": "no-cache",
    "pragma": "no-cache",
    "priority": "u=0, i",
    "sec-ch-ua": '"Not;A=Brand";v="99", "Microsoft Edge";v="139", "Chromium";v="139"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Windows"',
    "sec-fetch-dest": "document",
    "sec-fetch-mode": "navigate",
    "sec-fetch-site": "none",
    "sec-fetch-user": "?1",
    "upgrade-insecure-requests": "1",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36 Edg/139.0.0.0",
    # 'cookie': 'bid=0_w3By5v7uU; _pk_id.100001.4cf6=796df7ae0d43c7e8.1756823549.; __utmc=30149280; __utmz=30149280.1756823550.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); __utmc=223695111; __utmz=223695111.1756823550.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); __yadk_uid=CapdE8sEJb4Dh6FWMXkHWKWbJH87lvmw; ll="108169"; _vwo_uuid_v2=D9FF1219C93C5F9C544491F85609A49B4|201699e30da01d47f70825bcd930312b; cto_bundle=9O-uqV9Tdzc2bnlwUFpCZjNLb21uM092VzVYdmx5YW1UeDdlaEZQOTNpJTJCWlRwVkhTWG5iemZUbE5HNXFUbG1jTUU5eWtSWksxaFRRc2tFd29hUUlCMGE5Umh5MW0wM1VhR2tCaWhISUdEclF0SjUlMkJaQyUyRiUyQlpQb0Z4Nk4lMkI4VEZIcDA0V1BtdjhnSGNKaWdIZmdQTW1uQngwdE5BJTNEJTNE; ap_v=0,6.0; _pk_ses.100001.4cf6=1; __utma=30149280.1451705010.1756823550.1756826591.1757215808.3; __utma=223695111.149158184.1756823550.1756826591.1757215808.3; __utmb=223695111.0.10.1757215808; __utmt_t1=1; __utmb=30149280.3.8.1757215808; __gads=ID=9fc49e77f9e45c41:T=1756823551:RT=1757215817:S=ALNI_MaNDmzc7kPM6YHnOc-oVc0GW7ensw; __gpi=UID=0000118cd3db64da:T=1756823551:RT=1757215817:S=ALNI_MaQGb4GsvlQFPy6q-qGfU_vAk9lgA; __eoi=ID=078084a8688bd4a0:T=1756823551:RT=1757215817:S=AA-AfjbGTDKREMV1HHZ_19W4f9dY; FCNEC=%5B%5B%22AKsRol9myJp-TtGKTs1J3QVSm-po-jtRdr6YRdTo_hgcUgJtliYTFvX60HmdcJWAWtKCu0fG4EE-AhnMgkX3FMcSX3QTI1f7FsJeFdKnoSzbJvKqYONyrdbLkbEFWwDL2J5PhKYVTXtmG5zOWDYMH4HxLeO5-7x6uA%3D%3D%22%5D%5D; RT=s=1757215834424&r=https%3A%2F%2Fmovie.douban.com%2Ftop250',
}

result = []
for i in range(0, 10):
    url = f"https://movie.douban.com/top250?start={i*25}"
    response = requests.get(url, cookies=cookies, headers=headers)
    html = response.text

    HTML = etree.HTML(html)
    # fmt: off
    titles = HTML.xpath('//div[@id="content"]//div[@class="hd"]//span[@class="title"][1]/text()')
    directors = re.compile(r"导演: (.+?) ").findall(html)
    rating = HTML.xpath('//span[@class="rating_num"]/text()')

    # print(titles)
    # print(directors)
    # print(rating)
    # fmt: off
    for t,d,r in zip(titles,directors,rating):   # zip的使用方法，像拉链一样，把多个列表对齐
        result.append([t,d,r])
print(result)
# fmt: on
