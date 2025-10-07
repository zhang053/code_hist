"""
目标链接
https://push2.eastmoney.com/api/qt/clist/get?np=1&fltt=1&invt=2&cb=jQuery37109155425940039459_1759754393521&fs=m%3A0%2Bt%3A6%2Cm%3A0%2Bt%3A80%2Cm%3A1%2Bt%3A2%2Cm%3A1%2Bt%3A23%2Cm%3A0%2Bt%3A81%2Bs%3A2048&fields=f12%2Cf13%2Cf14%2Cf1%2Cf2%2Cf4%2Cf3%2Cf152%2Cf5%2Cf6%2Cf7%2Cf15%2Cf18%2Cf16%2Cf17%2Cf10%2Cf8%2Cf9%2Cf23&fid=f3&pn=2&pz=20&po=1&dect=1&ut=fa5fd1943c7b386f172d6893dbfba10b&wbp2u=%7C0%7C0%7C0%7Cweb&_=1759754393626
https://push2.eastmoney.com/api/qt/clist/get?np=1&fltt=1&invt=2&cb=jQuery37109155425940039459_1759754393521&fs=m%3A0%2Bt%3A6%2Cm%3A0%2Bt%3A80%2Cm%3A1%2Bt%3A2%2Cm%3A1%2Bt%3A23%2Cm%3A0%2Bt%3A81%2Bs%3A2048&fields=f12%2Cf13%2Cf14%2Cf1%2Cf2%2Cf4%2Cf3%2Cf152%2Cf5%2Cf6%2Cf7%2Cf15%2Cf18%2Cf16%2Cf17%2Cf10%2Cf8%2Cf9%2Cf23&fid=f3&pn=3&pz=20&po=1&dect=1&ut=fa5fd1943c7b386f172d6893dbfba10b&wbp2u=%7C0%7C0%7C0%7Cweb&_=1759754393627

通过对比发现,只有pn=1,2,3 的不同
pn 代表页码
通过len发现 pz 控制获取数量,最多获取100条数据
"""

import requests
import re
import json
import csv

# 通过尝试发现只有ua就可以获得内容
headers = {
    "Accept": "*/*",
    "Accept-Language": "ja,en;q=0.9,en-GB;q=0.8,en-US;q=0.7,zh-CN;q=0.6,zh;q=0.5",
    "Cache-Control": "no-cache",
    "Connection": "keep-alive",
    "Pragma": "no-cache",
    "Referer": "https://quote.eastmoney.com/center/gridlist.html",
    "Sec-Fetch-Dest": "script",
    "Sec-Fetch-Mode": "no-cors",
    "Sec-Fetch-Site": "same-site",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36 Edg/141.0.0.0",
    "sec-ch-ua": '"Microsoft Edge";v="141", "Not?A_Brand";v="8", "Chromium";v="141"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Windows"',
    # 'Cookie': 'qgqp_b_id=cf8f65d060c40a5ad8cca75ab3a2d17d; fullscreengg=1; fullscreengg2=1; st_si=51833639911228; st_asi=delete; st_nvi=fmWNwLFxHDEV8h8i5NvYa77f9; nid=038c878841ee8431b54a91cc4becec08; nid_create_time=1759754045599; gvi=iVjZfReoYY5-0yIAvOjIB9f99; gvi_create_time=1759754045599; st_pvi=25594665634844; st_sp=2025-10-06%2021%3A34%3A04; st_inirUrl=; st_sn=12; st_psi=20251006213953956-113200301321-5242357191',
}

cookies = {
    "qgqp_b_id": "cf8f65d060c40a5ad8cca75ab3a2d17d",
    "fullscreengg": "1",
    "fullscreengg2": "1",
    "st_si": "51833639911228",
    "st_asi": "delete",
    "st_nvi": "fmWNwLFxHDEV8h8i5NvYa77f9",
    "nid": "038c878841ee8431b54a91cc4becec08",
    "nid_create_time": "1759754045599",
    "gvi": "iVjZfReoYY5-0yIAvOjIB9f99",
    "gvi_create_time": "1759754045599",
    "st_pvi": "25594665634844",
    "st_sp": "2025-10-06%2021%3A34%3A04",
    "st_inirUrl": "",
    "st_sn": "12",
    "st_psi": "20251006213953956-113200301321-5242357191",
}

params = {
    "np": "1",
    "fltt": "1",
    "invt": "2",
    "cb": "jQuery37109155425940039459_1759754393521",  # 这里是可以自定义的
    "fs": "m:0+t:6,m:0+t:80,m:1+t:2,m:1+t:23,m:0+t:81+s:2048",
    "fields": "f12,f13,f14,f1,f2,f4,f3,f152,f5,f6,f7,f15,f18,f16,f17,f10,f8,f9,f23",
    "fid": "f3",
    "pn": "57",
    "pz": "100",
    "po": "1",
    "dect": "1",
    "ut": "fa5fd1943c7b386f172d6893dbfba10b",
    "wbp2u": "|0|0|0|web",
    "_": "1759754393547",  # 时间戳，time.time 乘以一千，取整
}

# params的cb可以任意修改，自定义
# 把params的cb去掉会得到json，但是不是所有jsonp都可以做到


def get_data(pn):
    params["pn"] = pn
    response = requests.get(
        "https://push2.eastmoney.com/api/qt/clist/get",
        cookies=cookies,
        params=params,
        headers=headers,
    )
    # print(response)
    # print(response.json())  # 获取的内容是jsonp，不是json
    # print(response.text)

    # # 两种方法处理jsonp
    # 1. 最常见最好用的  -- 使用正则
    # 第二种见sp1101
    # 首先匹配括号，括号是有意义的所以前面加反斜线
    parrent = re.compile(r"\((.+)\)")
    # 不要问号，贪婪模式，匹配的越多越好，知道匹配不到
    result = re.findall(parrent, response.text)[0]

    # print(data)
    # 成功转换成字符串，接下来要转化成json，并提取需要的信息
    result = json.loads(result)["data"]
    if result is None:
        print("没有更多数据了")
        return False
    else:
        data = result["diff"]
        return data
    # 运行到最后一页获取的data是null 空值 --> 判断条件


def save_data(data):
    for i in data:
        with open("stock.csv", "a", encoding="utf-8") as f:
            f.write(json.dumps(i, ensure_ascii=False) + "\n")


pn = 1
while 1:
    data = get_data(pn)
    if not data:
        break
    print(f"第{pn}页")
    print(len(data))
    save_data(data)
    pn += 1
