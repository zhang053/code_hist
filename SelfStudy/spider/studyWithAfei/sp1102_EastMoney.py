import requests

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

params = {
    "np": "1",
    "fltt": "1",
    "invt": "2",
    "cb": "jQuery37109155425940039459_1759754393521",
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

response = requests.get(
    "https://push2.eastmoney.com/api/qt/clist/get",
    params=params,
    cookies=cookies,
    headers=headers,
)
print(response)
# print(response.json())  # 获取的内容是jsonp，不是json
print(response.text)

# # 两种方法处理jsonp
# 1. 最常见最好用的  -- 使用正则
