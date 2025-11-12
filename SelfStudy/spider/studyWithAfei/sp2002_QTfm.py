"""
获取蜻蜓fm
目标网址 https://www.qtfm.cn/channels/428295

链接分析
发现 重定向 --> 输入的地址转接到别的网址

https://audio.qtfm.cn/audiostream/redirect/428295/21047632?access_token=&device_id=MOBILESITE&qingting_id=&t=1762680748886&sign=d1f7d712041993dcfd44b648bfee0081

https://audio.qtfm.cn/audiostream/redirect/428295/20820595?access_token=&device_id=MOBILESITE&qingting_id=&t=1762680611131&sign=6fb28fadbd8840ed36dfd683e0a87329

t : timestamp 时间戳
sign 未知 用途: 用来确认是否是自己网站发来的请求  --> 推测md5

    sign 是常用词, 不方便特定内容  -->  可以搜索别的一起的单词, access_token, device_id,....
                                                            device_id没有变化过, 搜索这个的值
    寻找同类关键词

"""

from lxml import etree
import re
import requests
import json
import subprocess

cookies = {
    "HWWAFSESID": "1c61c761d40254df38",
    "HWWAFSESTIME": "1762487998172",
    "Hm_lvt_bbe853b61e20780bcb59a7ea2d051559": "1762488000",
    "HMACCOUNT": "42F592952044B1A2",
    "cloudwaf_baseurl": "23d4f100244041fea8b5587800fef4ee",
    "WAFSESSCC_TAG": "d3d3LnF0Zm0uY24yM2Q0ZjEwMDI0NDA0MWZlYThiNTU4NzgwMGZlZjRlZV9Nb3ppbGxhLzUuMCAoV2luZG93cyBOVCAxMC4wOyBXaW42NDsgeDY0KSBBcHBsZVdlYktpdC81MzcuMzYgKEtIVE1MLCBsaWtlIEdlY2tvKSBDaHJvbWUvMTQxLjAuMC4wIFNhZmFyaS81MzcuMzYgRWRnLzE0MS4wLjAuMA==",
    "captcha_rand_code": "MTc2MjY4OTE0MC4xNjN8MjEzNHxkY2Y1MjUzNjUxZjFjZWE4ZThhNTFkOWQyOGQxYTAxNmExMTgxNGViZWFmNTdmNDU2NDVmYjcyNjkyZmJlNGQ0",
    "preurl": "/categories/521/3.999bf61058d20a4edffb.js/",
    "Hm_lpvt_bbe853b61e20780bcb59a7ea2d051559": "1762695616",
}

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36 Edg/141.0.0.0",
}

response = requests.get(
    "https://www.qtfm.cn/channels/293643/", cookies=cookies, headers=headers
)
print(response)
html = response.text

pattern = re.compile(r"window.__initStores=(.+?)\n")
json_str = pattern.findall(html)[0]
# print(json_str)
plist = json.loads(json_str)["AlbumStore"]["plist"]
url_list = []
for item in plist:
    # 获取音频的地址
    _id = item["id"]
    title = item["title"]
    result = subprocess.run(
        ["node", "sp2003_ParamsReverse.js", str(_id)],
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    url = result.stdout.strip()
    # 下载音频
    with open(f"sp2004_tempDLmp3/{title}.mp3", "wb") as f:
        f.write(requests.get(url, headers=headers).content)
        print(f"下载成功: {title}")
# print(url_list)
