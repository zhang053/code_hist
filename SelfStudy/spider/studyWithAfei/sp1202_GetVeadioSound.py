"""
使用 ffmpeg 工具，对视频进行合并
ffmpeg 是一个纯命令行工具，没有GUI界面

第一步:解压安装包，把安装包放到喜欢的地址：D:\ffmpeg\bin
第二步:复制bin目录，添加到环境变量
第三步:cmd面板里 ffmpeg --version 确认是否正确安装

添加环境变量步骤：
1. 右键此电脑，在文件夹中的PC
2. 自动打开设置，然后选择システムの詳細設定
3. 打开的窗口最下面環境変数(N)...
4. 下面的システム環境変数里面找到path
5. 打开后右上角有个新建，添加复制的地址，然后点击ok->ok->ok

ffmpeg 命令
-合并
    如果有一个mp4
"""

import requests

headers = {
    "Accept": "*/*",
    "Accept-Language": "ja,en;q=0.9,en-GB;q=0.8,en-US;q=0.7,zh-CN;q=0.6,zh;q=0.5",
    "Cache-Control": "no-cache",
    "Connection": "keep-alive",
    "Origin": "https://www.bilibili.com",
    "Pragma": "no-cache",
    "Referer": "https://www.bilibili.com/video/BV1XS421K7v2/",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "cross-site",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36 Edg/141.0.0.0",
    "sec-ch-ua": '"Microsoft Edge";v="141", "Not?A_Brand";v="8", "Chromium";v="141"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Windows"',
}

# 获取视频的画面
response = requests.get(
    "https://upos-sz-mirrorcosov.bilivideo.com/upgcxcode/77/76/1440427677/1440427677-1-100109.m4s?e=ig8euxZM2rNcNbdlhoNvNC8BqJIzNbfqXBvEqxTEto8BTrNvN0GvT90W5JZMkX_YN0MvXg8gNEV4NC8xNEV4N03eN0B5tZlqNxTEto8BTrNvNeZVuJ10Kj_g2UB02J0mN0B5tZlqNCNEto8BTrNvNC7MTX502C8f2jmMQJ6mqF2fka1mqx6gqj0eN0B599M=&trid=701922dd539545219f7eb55112f1833u&mid=0&nbs=1&deadline=1759851250&gen=playurlv3&os=cosovbv&og=hw&uipk=5&platform=pc&oi=3681062357&upsig=88cb73994e2cb1c277059d1c6690c763&uparams=e,trid,mid,nbs,deadline,gen,os,og,uipk,platform,oi&bvc=vod&nettype=0&bw=310150&buvid=E47527FD-ADA4-388B-0E51-FAE3F500DE0A93607infoc&build=0&dl=0&f=u_0_0&agrr=0&orderid=0,2",
    headers=headers,
)
with open("sp1203_bili_pic.mp4", "wb") as f:
    f.write(response.content)

# 获取视频的音频
response = requests.get(
    "https://upos-hz-mirrorakam.akamaized.net/upgcxcode/77/76/1440427677/1440427677-1-30216.m4s?e=ig8euxZM2rNcNbdlhoNvNC8BqJIzNbfqXBvEqxTEto8BTrNvN0GvT90W5JZMkX_YN0MvXg8gNEV4NC8xNEV4N03eN0B5tZlqNxTEto8BTrNvNeZVuJ10Kj_g2UB02J0mN0B5tZlqNCNEto8BTrNvNC7MTX502C8f2jmMQJ6mqF2fka1mqx6gqj0eN0B599M=&mid=0&platform=pc&oi=3681062357&gen=playurlv3&og=hw&trid=701922dd539545219f7eb55112f1833u&nbs=1&deadline=1759851250&uipk=5&os=akam&upsig=bec0376dac50757d005b434887261963&uparams=e,mid,platform,oi,gen,og,trid,nbs,deadline,uipk,os&hdnts=exp=1759851250~hmac=df3ad7688d995c997ebbcefc81638ce0f9ac362163c6026949180c9df297923c&bvc=vod&nettype=0&bw=51379&agrr=0&buvid=E47527FD-ADA4-388B-0E51-FAE3F500DE0A93607infoc&build=0&dl=0&f=u_0_0&orderid=0,2",
    headers=headers,
)
with open("sp1204_bili_Sound.mp3", "wb") as f:
    f.write(response.content)

# # 合并获取的音频和画面
