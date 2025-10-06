import requests
import re
import json

# 通过尝试发现只有ua就可以获得内容
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36 Edg/141.0.0.0",
}

params = {
    "np": "1",
    "fltt": "1",
    "invt": "2",
    "cb": "jQuery37109155425940039459_1759754393521",  # 这里是可以自定义的
    "fs": "m:0+t:6,m:0+t:80,m:1+t:2,m:1+t:23,m:0+t:81+s:2048",
    "fields": "f12,f13,f14,f1,f2,f4,f3,f152,f5,f6,f7,f15,f18,f16,f17,f10,f8,f9,f23",
    "fid": "f3",
    "pn": "1",
    "pz": "20",
    "po": "1",
    "dect": "1",
    "ut": "fa5fd1943c7b386f172d6893dbfba10b",
    "wbp2u": "|0|0|0|web",
    "_": "1759754393547",
}

# params的cb可以任意修改，自定义
# 把params的cb去掉会得到json，但是不是所有jsonp都可以做到

response = requests.get(
    "https://push2.eastmoney.com/api/qt/clist/get",
    params=params,
    headers=headers,
)
print(response)
# print(response.json())  # 获取的内容是jsonp，不是json
# print(response.text)

# # 两种方法处理jsonp
# 1. 最常见最好用的  -- 使用正则
# 第二种见sp1101
# 首先匹配括号，括号是有意义的所以前面加反斜线
parrent = re.compile(r"\((.+)\)")
# 不要问号，贪婪模式，匹配的越多越好，知道匹配不到
data = re.findall(parrent, response.text)[0]

# print(data)
# 成功转换成字符串，接下来要转化成json，并提取需要的信息
result = json.loads(data)
print(result["data"]["diff"])
