import requests
from lxml import etree
import json
import os
import time
import random

# 通过request请求到的是被js渲染前的源代码，其中包括了通过js来渲染的东西
# 浏览器会自动运行js脚本，但是请求到的源代码中的js不会被运行
# 不会获得通过js脚本创建的标签
# xpath获取不到这种被通过代码创建的标签

# 解决方案1，自动化采集工具 playwright
# 以后讲

# # # 解决方案2，分析实际数据接口，获取图片原始数据

# 在网页中，用户即将将滚动条拉到底的时候，网页会自动加载下一页的内容。叫做瀑布流
# 最开始只会加载填满整个屏幕的

# 右键检查的network 页面中的Fetch/XHR，叫做异步请求，就是不会刷新整个页面的请求

# 瀑布流，每次发出请求都是朝 开头是acjson的链接发起的
# 所以直接朝那个acjson发请求就可以了

# "https://image.baidu.com/search/acjson?tn=resultjson_com&word=%E7%8C%AB%E5%92%AA%E5%9B%BE%E7%89%87&ie=utf-8&fp=result&fr=&ala=0&applid=12310490245225309583&pn=120&rn=30&nojc=0&gsm=78&newReq=1"
# 这个是目标的acjson链接

cookies = {
    "BAIDUID": "48E3DE22FA1321E55C136CBB9CB85853:FG=1",
    "newlogin": "1",
    "PSTM": "1756477320",
    "BIDUPSID": "69E5D72C5201B08F2D08B986BC3D835D",
    "BDUSS": "ldISmtOdDlMOVIzflowdEZIMDZ6TWVoekJjdndDclF4Y1dTM2E5bjBrd3FzZWRvRVFBQUFBJCQAAAAAAQAAAAEAAAA0YFSTAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACokwGgqJMBob",
    "BDUSS_BFESS": "ldISmtOdDlMOVIzflowdEZIMDZ6TWVoekJjdndDclF4Y1dTM2E5bjBrd3FzZWRvRVFBQUFBJCQAAAAAAQAAAAEAAAA0YFSTAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACokwGgqJMBob",
    "BDORZ": "B490B5EBF6F3CD402E515D22BCDA1598",
    "H_PS_PSSID": "63142_63327_63947_64660_64748_64701_64815_64834_64878_64892_64911_64923_64935_64980_65048_65076_65083_65116_65141_65140_65137_65188_65204_65219_65250_65256_65143_65274_65281",
    "BA_HECTOR": "8k840l0l8g2l802g810g2l8k2k01051kcflqf25",
    "BAIDUID_BFESS": "48E3DE22FA1321E55C136CBB9CB85853:FG=1",
    "H_WISE_SIDS": "63947_64660_64748_64815_64834_64878_64911_64923_64980_65048_65076_65083_65116_65141_65140_65137_65188_65204_65219_65250_65256_65143_65274_65281",
    "arialoadData": "false",
    "BDRCVFR[feWj1Vr5u3D]": "mk3SLVN4HKm",
    "delPer": "0",
    "PSINO": "7",
    "ab_sr": "1.0.1_YmJiYWZhNWEwZDNjOTYyYzdmMDgyZDA2ZTY5YWNhNTY3MWY2NWNmYzU4NDIzMWE1ODMxNmRiOTJmMGNjNjNhMTkxMTc4ZTRkMWQ4MWY4ZjMyZTAyYjc1ZDY4NTNmNGRmOTc0NDY2MjIyZTNmYThkYWJiMGJhMDBmYzFhZTEwOWNlNTM3MDU0ZWU3NmI2MDNjNzNiNzUzYWMzZDY0M2RmYQ==",
}
headers = {
    "accept": "image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8",
    "accept-language": "ja,en;q=0.9,en-GB;q=0.8,en-US;q=0.7,zh-CN;q=0.6,zh;q=0.5",
    "cache-control": "no-cache",
    "pragma": "no-cache",
    "priority": "i",
    "referer": "https://image.baidu.com/",
    "sec-ch-ua": '"Chromium";v="140", "Not=A?Brand";v="24", "Microsoft Edge";v="140"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Windows"',
    "sec-fetch-dest": "image",
    "sec-fetch-mode": "no-cors",
    "sec-fetch-site": "same-site",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36 Edg/140.0.0.0",
    # 'cookie': 'BAIDUID=48E3DE22FA1321E55C136CBB9CB85853:FG=1; newlogin=1; PSTM=1756477320; BIDUPSID=69E5D72C5201B08F2D08B986BC3D835D; BDUSS=ldISmtOdDlMOVIzflowdEZIMDZ6TWVoekJjdndDclF4Y1dTM2E5bjBrd3FzZWRvRVFBQUFBJCQAAAAAAQAAAAEAAAA0YFSTAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACokwGgqJMBob; BDUSS_BFESS=ldISmtOdDlMOVIzflowdEZIMDZ6TWVoekJjdndDclF4Y1dTM2E5bjBrd3FzZWRvRVFBQUFBJCQAAAAAAQAAAAEAAAA0YFSTAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACokwGgqJMBob; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; H_PS_PSSID=63142_63327_63947_64660_64748_64701_64815_64834_64878_64892_64911_64923_64935_64980_65048_65076_65083_65116_65141_65140_65137_65188_65204_65219_65250_65256_65143_65274_65281; BA_HECTOR=8k840l0l8g2l802g810g2l8k2k01051kcflqf25; BAIDUID_BFESS=48E3DE22FA1321E55C136CBB9CB85853:FG=1; H_WISE_SIDS=63947_64660_64748_64815_64834_64878_64911_64923_64980_65048_65076_65083_65116_65141_65140_65137_65188_65204_65219_65250_65256_65143_65274_65281; arialoadData=false; BDRCVFR[feWj1Vr5u3D]=mk3SLVN4HKm; delPer=0; PSINO=7; ab_sr=1.0.1_YmJiYWZhNWEwZDNjOTYyYzdmMDgyZDA2ZTY5YWNhNTY3MWY2NWNmYzU4NDIzMWE1ODMxNmRiOTJmMGNjNjNhMTkxMTc4ZTRkMWQ4MWY4ZjMyZTAyYjc1ZDY4NTNmNGRmOTc0NDY2MjIyZTNmYThkYWJiMGJhMDBmYzFhZTEwOWNlNTM3MDU0ZWU3NmI2MDNjNzNiNzUzYWMzZDY0M2RmYQ==',
}
params = {
    "tn": "resultjson_com",
    "word": "猫咪",
    "ie": "utf-8",
    "fp": "result",
    "fr": "",
    "ala": "0",
    "applid": "10537659423693859337",
    "pn": "0",
    "rn": "100",
    "nojc": "0",
    "gsm": "1e",
    "newReq": "1",
}
response = requests.get(
    "https://image.baidu.com/search/acjson",
    params=params,
    cookies=cookies,
    headers=headers,
)
print(response)
r = response.text
# print(r)

# 通过数据的解析发现，每个图片都是一个thumburl的图片链接，但是这个每个都不一样，但是都是https开头的

# # # json字符串

"""
# json 有特定的格式规则
# 1，最外层必须是个字典
# {
    花括号
    },
    [
    方括号
    ]
最外层只能是这两种括号

# 2，值允许的格式
    数字10，12
    字符串"afsojl"
    null
    true/false  ....之类的

# 3，属性和字符串的值必须是双引号， 区分双引号和单引号，只能是用双引号
"""

# json 最经常用于前后端数据传输，因为大部分语言都能很好的解析json

# data = json.loads(r)
# print(data)
# 成功获取到json格式的代码，字典形式的代码

# 另一种方法，使用request自带的功能
data = response.json()
print("text is been changed into json")

# 以字典形式获取
img_lists = data["data"]["images"]
# print(img_lists)

# for img_link in img_lists:
#     src = img_link["thumburl"]
#     print(src)
# 大概有30来张图片
# 这些是一个瀑布流的一部分，可以通过寻找规律，获得所有瀑布流的链接，来获得所有图片的链接

# 尝试寻找请求文件的规律
#
# https://image.baidu.com/search/acjson?tn=resultjson_com&word=%E7%8C%AB%E5%92%AA&ie=utf-8&fp=result&fr=&ala=0&applid=10766165304425089332&pn=30&rn=30&nojc=0&gsm=1e&newReq=1
# https://image.baidu.com/search/acjson?tn=resultjson_com&word=%E7%8C%AB%E5%92%AA&ie=utf-8&fp=result&fr=&ala=0&applid=10766165304425089332&pn=60&rn=30&nojc=0&gsm=3c&newReq=1
# https://image.baidu.com/search/acjson?tn=resultjson_com&word=%E7%8C%AB%E5%92%AA&ie=utf-8&fp=result&fr=&ala=0&applid=10766165304425089332&pn=90&rn=30&nojc=0&gsm=5a&newReq=1

# 通过观察发现，后半部分的pn = xx 的地方有不一样 ， 然后是 gsm = xxx 的地方不同
# 可以发现 pn 是表示图片的编号
# rn 值控制的获取的图片的数量，最多一次获取60张

# 下载图片并保存
file_name = "cat"
os.makedirs(file_name, exist_ok=True)

for i, img in enumerate(img_lists):
    src = img["thumburl"]
    resp = requests.get(src, headers=headers, cookies=cookies)
    with open(f"{file_name}/{i}.jpg", "wb") as f:
        f.write(resp.content)
        time.sleep(random.uniform(1.0, 2.0))
    print("图片以保存，第 ", i, " 张")
