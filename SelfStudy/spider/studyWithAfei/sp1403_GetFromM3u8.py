# 找到对应的m3u8链接

import os
import requests
import time

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36 Edg/141.0.0.0",
}

params = {
    "pkey": "ABDecsyanFNcmQ3J4TKk0rQoUONBHrbbKqFuAr4qejX_bHcwAIEqGHSJ8sKdFC_rtDAKW8f5dDHdCNU6UWldicv4_pzmcSLG16lxpJoIfPTi1TRhI78o_dfCtJzCoCbixciBPqLYKNRO25BKGxllQZouSp6XHqHLklIP2Wm-UojvL8JPhI2IzTJmKQTIzxvXAkeg1nkLHgiMJOp9BTL64iYfmjWO2_UcgJbIJYQF78-m88A0pdWKyW-dOAwAJNeEjIM",
    "safety_id": "AAIcFoRjyJws7q73Pl1MwxBQ",
}

response = requests.get(
    "https://tx-safety-video.acfun.cn/mediacloud/acfun/acfun_video/9e0ab2abd5c038ec-ee859ae7e3a73dca02bfd8ef6a786c1a-hls_720p_2.m3u8",
    params=params,
    headers=headers,
)
print(response)
# print(response.text)

# 得到m3u8文件内的文本内容
txt = response.text
# 以换行进行切割
lines = txt.split("\n")
ts_urls = []
for line in lines:
    # 如果不是以#开头，就添加到列表里
    if line.strip() and not line.startswith("#"):
        # strip删除空字符为空表示false，所以可以通过该方法去掉空字符
        # fmt: off
        ts_urls.append("https://tx-safety-video.acfun.cn/mediacloud/acfun/acfun_video/"+line)
        # 补全链接
        # fmt: on
# print(ts_urls)
# 以获取所有分片文件链接

# 循环下载所有ts文件
# 可以在前面的循环中请求到之后直接下载

# for index, ts_url in enumerate(ts_urls):
#     resp = requests.get(ts_url, headers=headers)
#     with open(f"sp1404_TSurlsDL/{index}.ts", "wb") as f:
#         f.write(resp.content)
#         print(f"downloading {index}.ts, total:{len(ts_urls)}")
#         time.sleep(1)
# 成功获取所有ts文件
# 合并所有ts文件

# # 尝试把所有的ts写入mp4
# # 一部分ts文件可以通过改为.mp4直接进行转换,并非一定可以
# with open("sp1405_TS.mp4", "wb") as f:
#     for index, ts_url in enumerate(ts_urls):
#         resp = requests.get(ts_url, headers=headers)
#         f.write(resp.content)
#         print(f"downloading {index}.ts, total:{len(ts_urls)}")
#         time.sleep(1)

import subprocess

# fmt: off
subprocess.run(
    [
        "ffmpeg", # ffmpeg命令
        "-f", "concat", # 指定格式为concat
        "-safe", "0", # 允许输入文件中的相对路径
        "-i", "sp1406_file.txt", # 指定输入文件
        "-c", "copy", # 指定编码方式为copy
        "sp1407_output.mp4", # 指定输出文件为mp4
        "-y" # 允许覆盖输出文件
    ]
)
# fmt: on
