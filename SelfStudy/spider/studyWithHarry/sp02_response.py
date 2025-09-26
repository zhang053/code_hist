import requests

# url = "https://www.google.com/"
# headers = {
#     "referer": "https://www.google.com/",
#     "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36",
# }
# response = requests.get(url, headers=headers)
# string = response.text
# print(string)

# url2 = "https://www.baidu.com/"
# header = {
#     "referer": "https://www.baidu.com/",
#     "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36 Edg/139.0.0.0",
# }

# res = requests.get(url2, headers=header)
# stri = res.text
# print(stri)

# 练习 应用
url3 = "https://ssl.gstatic.com/gb/images/sprites/p_2x_f2571996302d.png"

# 反反爬手段 构建 ua 池  或者使用fake库: pip install fake-useragent
ua_list = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36 Edg/139.0.0.0",
]

import random

ua = random.choices(ua_list)
# print(ua)

hd = {
    "Referer": "https://ogs.google.com/",
    "user-agent": ua,
}  # UA(user-agent:作用 识别设备信息，返回对应数据，调整对应格式。反爬：短时间内大量相同ua队同一个网站发起请求，会被认定非人行为——》爬虫)

# 如何 反 反爬


resp = requests.get(url3, headers=hd)

with open("picture.png", "wb") as p:
    p.write(resp.content)  # 如果是文本用txt，如果是图片，以字节流形式输出的用content
