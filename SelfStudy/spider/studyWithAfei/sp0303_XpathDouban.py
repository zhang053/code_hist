import requests
from fake_useragent import UserAgent
import random

# 豆瓣的情况，如果请求过多会被封ip，如何解决。豆瓣通过cookie来判断是否有异常
# 先登录，然后把登录后的headers的所有参数携带
# 一个一个复制太麻烦，浏览器 https://tool.lu/curl/ 解析工具
# 点击检查页面选择要爬取的那个链接，右键，复制，copy as cURL (bash)
# 然后粘贴到搜索的链接页面，点击生成python，就可复制粘贴全部headers的cookie了
""" 这些是粘贴过来的，是登录后的状态，反反爬手段
import requests

cookies = {
    'bid': '0_w3By5v7uU',
    '_pk_id.100001.4cf6': '796df7ae0d43c7e8.1756823549.',
    '__utmc': '30149280',
    '__utmz': '30149280.1756823550.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none)',
    '__utmc': '223695111',
    '__utmz': '223695111.1756823550.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none)',
    '__yadk_uid': 'CapdE8sEJb4Dh6FWMXkHWKWbJH87lvmw',
    'll': '"108169"',
    '_vwo_uuid_v2': 'D9FF1219C93C5F9C544491F85609A49B4|201699e30da01d47f70825bcd930312b',
    'cto_bundle': '9O-uqV9Tdzc2bnlwUFpCZjNLb21uM092VzVYdmx5YW1UeDdlaEZQOTNpJTJCWlRwVkhTWG5iemZUbE5HNXFUbG1jTUU5eWtSWksxaFRRc2tFd29hUUlCMGE5Umh5MW0wM1VhR2tCaWhISUdEclF0SjUlMkJaQyUyRiUyQlpQb0Z4Nk4lMkI4VEZIcDA0V1BtdjhnSGNKaWdIZmdQTW1uQngwdE5BJTNEJTNE',
    'ap_v': '0,6.0',
    '_pk_ses.100001.4cf6': '1',
    '__utma': '30149280.1451705010.1756823550.1756826591.1757215808.3',
    '__utma': '223695111.149158184.1756823550.1756826591.1757215808.3',
    '__utmb': '223695111.0.10.1757215808',
    '__utmt_t1': '1',
    '__utmb': '30149280.3.8.1757215808',
    '__gads': 'ID=9fc49e77f9e45c41:T=1756823551:RT=1757215817:S=ALNI_MaNDmzc7kPM6YHnOc-oVc0GW7ensw',
    '__gpi': 'UID=0000118cd3db64da:T=1756823551:RT=1757215817:S=ALNI_MaQGb4GsvlQFPy6q-qGfU_vAk9lgA',
    '__eoi': 'ID=078084a8688bd4a0:T=1756823551:RT=1757215817:S=AA-AfjbGTDKREMV1HHZ_19W4f9dY',
    'FCNEC': '%5B%5B%22AKsRol9myJp-TtGKTs1J3QVSm-po-jtRdr6YRdTo_hgcUgJtliYTFvX60HmdcJWAWtKCu0fG4EE-AhnMgkX3FMcSX3QTI1f7FsJeFdKnoSzbJvKqYONyrdbLkbEFWwDL2J5PhKYVTXtmG5zOWDYMH4HxLeO5-7x6uA%3D%3D%22%5D%5D',
    'RT': 's=1757215834424&r=https%3A%2F%2Fmovie.douban.com%2Ftop250',
}

headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'ja,en;q=0.9,en-GB;q=0.8,en-US;q=0.7,zh-CN;q=0.6,zh;q=0.5',
    'cache-control': 'no-cache',
    'pragma': 'no-cache',
    'priority': 'u=0, i',
    'sec-ch-ua': '"Not;A=Brand";v="99", "Microsoft Edge";v="139", "Chromium";v="139"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'none',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36 Edg/139.0.0.0',
    # 'cookie': 'bid=0_w3By5v7uU; _pk_id.100001.4cf6=796df7ae0d43c7e8.1756823549.; __utmc=30149280; __utmz=30149280.1756823550.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); __utmc=223695111; __utmz=223695111.1756823550.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); __yadk_uid=CapdE8sEJb4Dh6FWMXkHWKWbJH87lvmw; ll="108169"; _vwo_uuid_v2=D9FF1219C93C5F9C544491F85609A49B4|201699e30da01d47f70825bcd930312b; cto_bundle=9O-uqV9Tdzc2bnlwUFpCZjNLb21uM092VzVYdmx5YW1UeDdlaEZQOTNpJTJCWlRwVkhTWG5iemZUbE5HNXFUbG1jTUU5eWtSWksxaFRRc2tFd29hUUlCMGE5Umh5MW0wM1VhR2tCaWhISUdEclF0SjUlMkJaQyUyRiUyQlpQb0Z4Nk4lMkI4VEZIcDA0V1BtdjhnSGNKaWdIZmdQTW1uQngwdE5BJTNEJTNE; ap_v=0,6.0; _pk_ses.100001.4cf6=1; __utma=30149280.1451705010.1756823550.1756826591.1757215808.3; __utma=223695111.149158184.1756823550.1756826591.1757215808.3; __utmb=223695111.0.10.1757215808; __utmt_t1=1; __utmb=30149280.3.8.1757215808; __gads=ID=9fc49e77f9e45c41:T=1756823551:RT=1757215817:S=ALNI_MaNDmzc7kPM6YHnOc-oVc0GW7ensw; __gpi=UID=0000118cd3db64da:T=1756823551:RT=1757215817:S=ALNI_MaQGb4GsvlQFPy6q-qGfU_vAk9lgA; __eoi=ID=078084a8688bd4a0:T=1756823551:RT=1757215817:S=AA-AfjbGTDKREMV1HHZ_19W4f9dY; FCNEC=%5B%5B%22AKsRol9myJp-TtGKTs1J3QVSm-po-jtRdr6YRdTo_hgcUgJtliYTFvX60HmdcJWAWtKCu0fG4EE-AhnMgkX3FMcSX3QTI1f7FsJeFdKnoSzbJvKqYONyrdbLkbEFWwDL2J5PhKYVTXtmG5zOWDYMH4HxLeO5-7x6uA%3D%3D%22%5D%5D; RT=s=1757215834424&r=https%3A%2F%2Fmovie.douban.com%2Ftop250',
}

response = requests.get('https://movie.douban.com/top250', cookies=cookies, headers=headers)

"""

url = "https://movie.douban.com/top250"
ua = UserAgent()
ua_output = ua.random
headers = {"user-agent": ua_output}

resp = requests.get(url, headers=headers)

from lxml import etree

ht = resp.text
# 获取爬过来的html文件
# 解析纯文本内容的解析方法
HTL = etree.HTML(ht)
# fmt: off
# 获取电影标题
titles = HTL.xpath('//div[@id="content"]//div[@class="hd"]//span[@class="title"][1]/text()')
# 想要获取的是电影标题，只要第一个，所以是列表形式的第一个
### 可以把xpath路径复制到检查栏，搜索，可以确定想要获取的信息是否争取，不要带text

# 一个偷懒但不稳定的方法，在检查，想要爬取得那一行，右键，复制，copy Xpath 就是下面的路径
# //*[@id="content"]/div/div[1]/ol/li[8]/div/div[2]/div[1]/a/span[1]
print(titles)
# fmt: on
directors = HTL.xpath('//div[@class="bd"]/p[1]/text()')
# 但是这个获取的并不精确，而且中文和英文没有被分开，xpath只能定位路径，内容无法进行筛选。所以只能用正则表达式
# 标签中包含的文本很干净，没有别的东西的时候用xpath，有很多杂的东西的时候用正则进行匹配

import re

director_pattern = re.compile(r"导演: (.+?) ")
directors = director_pattern.findall(ht)
print(directors)


# 获取评分
rating = HTL.xpath('//span[@class="rating_num"]/text()')
print(rating)

"""
# xpath可以进行循环遍历
lis = HTML.xpath("//navi[@class='main-nav']/ul/li) 这个可以获取好几个对象
然后遍历 lis
for i in lis:
    print(i.xpath(./a))  点 . 代表当前层级，该行意思是从当前层级的子层级寻找a标签
"""
