"""
只需要输入链接，就可以自动得到视频m4s地址，和音频m4s地址

通过json或者html的src属性，可以找到m4s的地址

目标链接
https://www.bilibili.com/video/BV1cqWgzGEoB/
在主页的html中查找

如果没在的话，找sources源代码，在检查页面找
"""

import requests
import re
import json
from jsonpath import jsonpath
import os

headers = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "accept-language": "ja,en;q=0.9,en-GB;q=0.8,en-US;q=0.7,zh-CN;q=0.6,zh;q=0.5",
    "cache-control": "no-cache",
    "pragma": "no-cache",
    "priority": "u=0, i",
    "sec-ch-ua": '"Microsoft Edge";v="141", "Not?A_Brand";v="8", "Chromium";v="141"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Windows"',
    "sec-fetch-dest": "document",
    "sec-fetch-mode": "navigate",
    "sec-fetch-site": "same-origin",
    "sec-fetch-user": "?1",
    "upgrade-insecure-requests": "1",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36 Edg/141.0.0.0",
    # 'cookie': "buvid3=E47527FD-ADA4-388B-0E51-FAE3F500DE0A93607infoc; b_nut=1754133793; buvid_fp=579054ec491e2fac30e98c9bb97790eb; _uuid=10C793107C-9BD4-1042D-662B-9C6C5156C8B950572infoc; theme-tip-show=SHOWED; rpdid=|(ullY~m)JJR0J'u~lRuJJ))u; buvid4=97AD0FC9-33DA-8153-BB27-D55A11071DED23393-024041707-NOYiWiv6XIn250mFCaOlBA%3D%3D; enable_web_push=DISABLE; LIVE_BUVID=AUTO1117548275209106; theme-avatar-tip-show=SHOWED; theme-switch-show=SHOWED; home_feed_column=5; hit-dyn-v2=1; PVID=1; sid=7aqnbhj0; bp_t_offset_3546751768201487=1120998876711485440; CURRENT_QUALITY=0; bili_ticket=eyJhbGciOiJIUzI1NiIsImtpZCI6InMwMyIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3NjAxNDUwMDIsImlhdCI6MTc1OTg4NTc0MiwicGx0IjotMX0.CZtwx43ZqKj50IHf12I8kx1lfFTuxAmm8G-slSvOc_E; bili_ticket_expires=1760144942; browser_resolution=1838-969; bmg_af_switch=1; bmg_src_def_domain=i2.hdslb.com; CURRENT_FNVAL=4048; b_lsid=5EFD51D9_199C43873BF",
}
# 请求初始html
resp = requests.get("https://www.bilibili.com/video/BV14zD3YCE1s/", headers=headers)
print(resp)

# 使用正则去匹配，找到.m4s的标签
# 通过查找html发现，是在一个叫window.__playinfo__里面的一个json数据
html = resp.text
pattern = re.compile(r"window\.__playinfo__=(.+?)</script>")
# 非贪婪模式，遇到的第一个结束
json_str = pattern.findall(html)[0]
# print(json_str)
json_data = json.loads(json_str)
# print(json_data)

# 有很多不同的m4s的链接，代表不同的分辨率，在所在的{}中有
# 想要找到的结构 window.__playinfo__ ---> data --->  dash ---> video
match_video = jsonpath(json_data, "$.data.dash.video..baseUrl")[0]
# print(match_video)

response = requests.get(match_video, headers=headers)
print(response)
with open("sp1207_AutoDLvideo.mp4", "wb") as f:
    f.write(response.content)
print("视频下载完成")

match_audio = jsonpath(json_data, "$.data.dash.audio..baseUrl")[0]
response = requests.get(match_audio, headers=headers)
print(response)
with open("sp1208_AutoDLaudio.mp3", "wb") as f:
    f.write(response.content)
print("音频下载完成")

# 使用ffmpeg命令行工具，将两个文件合并
# 通过python调用命令行工具
import subprocess

subprocess.run(
    [
        "ffmpeg",
        "-i",
        "sp1207_AutoDLvideo.mp4",
        "-i",
        "sp1208_AutoDLaudio.mp3",
        "-c:v",
        "copy",
        "-c:a",
        "aac",
        "sp1209_AutoDL.mp4",
        "-y",
    ]
)
print("合并完成")

# 合并完成后清理临时的音频视频
os.remove("sp1207_AutoDLvideo.mp4")
os.remove("sp1208_AutoDLaudio.mp3")
