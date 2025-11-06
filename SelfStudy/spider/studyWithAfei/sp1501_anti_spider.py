""" "
反爬
    爬取网站内容
反爬
    网站不给内容
反反爬
    突破网站的限制达到爬取的内容

1.user-agent
反爬: 不带ua的话,浏览器认为我们不是浏览器,不给内容
反反爬: headers中带上ua信息

2.cookie
反爬: 不带关键cookie信息,不给内容
反反爬: 使用curl去解析

3.referer 来源
反爬： 来源不是本站,不给信息(通常在访问网站内部网页的时候,比如登录,或者请求分片内容)
反反爬: 带上referer

1,2,3 总结 --> 只要合理的使用curl解析的方式都可以应对(反反爬)
---------------------------------------------------------------------------------------
4.短时间大量同一ip的访问
反爬: 封ip
反反爬: 链接vpn,进行ip代理
# ip封禁
# ip查询,百度搜索ip查询

# 很多形式--> 加验证,不给内容(404 notfound)
# 处理方法: 改变ip地址
# 方法1: 使用/更换vpn(违法)
# 1. 找一个能提供ip代理的网站, 获取有效的ip地址(免费的基本用不了)
# 2. 选便宜的,按使用量收费的,大概4块钱
--------------------------------------------------------------------------------------
5.数据动态加载
反爬: 初始页面,没有目标数据,数据通过后续ajax请求加载
反反爬.1: 分析ajax链接,向真实的数据链接发送请求

---后续内容-------
反反爬.2: 完全模拟浏览器行为(运行js) -- playwright

6.字体反爬
7.js加密
"""

# # 1对策.构建ua池

# ua_list = [
#     "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
#     "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.96 Safari/537.3",
#     "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.96 Safari/537.3",
#     "Mozilla/5.0 (MacOSX 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
#     "Mozilla/5.0 (MacOSX 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
# ]
# import random
# import requests

# url = "https://www.baidu.com"

# for i in range(10):
#     headers = {"User-Agent": random.choice(ua_list)}
#     print(headers)

# # 1对策.fakeua
# 注意，有些网站的ua发给手机的内容不一样
from fake_useragent import UserAgent
import requests

url = "https://www.baidu.com"

ua = UserAgent()

for i in range(10):
    headers = {"User-Agent": ua.random}
    print(headers)
