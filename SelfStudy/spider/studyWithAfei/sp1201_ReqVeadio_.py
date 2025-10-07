"""
目标：采集bilibli的视频
目标主网站：
https://www.bilibili.com/
具体视频的链接
https://www.bilibili.com/video/BV1XS421K7v2/

第一步：找到对应的视频的请求
    -方法1: 寻找视频对应的链接方法1: 在network中以大小排序,从大的开始找,找到一个包含m4s的链接

    -方法2: 拖动视频光标，实时查看关于视频的请求，会看到有m4s的链接请求

.m4s : 比较流行的视频分段处理格式
    -在html里面的 src 链接开始有 blob ，代表要求浏览器进行分段处理，所以看到blob表示要寻找m4s
    -可以通过分片段请求的形式，来做到视频分段加载 --> 流
    --> 流媒体
    -每个m4s的链接的url都没有变化
    -通过两个header的对比发现，range的参数发生变化,用于控制请求哪个片段
        --"Range": "bytes=612037-786619"
        --不带range，可以请求到完整的视频内容
    注意！ 不是所有的 m4s 请求不带range都可以完整获取，但是没有声音

    音频视频没有规律，需要一个一个尝试

第二步：下载m4s分片
"""

import requests

headers = {
    "accept": "*/*",
    "accept-language": "ja,en;q=0.9,en-GB;q=0.8,en-US;q=0.7,zh-CN;q=0.6,zh;q=0.5",
    "cache-control": "no-cache",
    "origin": "https://www.bilibili.com",
    "pragma": "no-cache",
    "priority": "u=1, i",
    # "range": "bytes=1213887-1392046",
    "referer": "https://www.bilibili.com/video/BV1XS421K7v2/",
    "sec-ch-ua": '"Microsoft Edge";v="141", "Not?A_Brand";v="8", "Chromium";v="141"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Windows"',
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "cross-site",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36 Edg/141.0.0.0",
}

response = requests.get(
    "https://upos-sz-mirrorcosov.bilivideo.com/upgcxcode/77/76/1440427677/1440427677-1-100109.m4s?e=ig8euxZM2rNcNbdlhoNvNC8BqJIzNbfqXBvEqxTEto8BTrNvN0GvT90W5JZMkX_YN0MvXg8gNEV4NC8xNEV4N03eN0B5tZlqNxTEto8BTrNvNeZVuJ10Kj_g2UB02J0mN0B5tZlqNCNEto8BTrNvNC7MTX502C8f2jmMQJ6mqF2fka1mqx6gqj0eN0B599M=&trid=701922dd539545219f7eb55112f1833u&mid=0&nbs=1&deadline=1759851250&gen=playurlv3&os=cosovbv&og=hw&uipk=5&platform=pc&oi=3681062357&upsig=88cb73994e2cb1c277059d1c6690c763&uparams=e,trid,mid,nbs,deadline,gen,os,og,uipk,platform,oi&bvc=vod&nettype=0&bw=310150&buvid=E47527FD-ADA4-388B-0E51-FAE3F500DE0A93607infoc&build=0&dl=0&f=u_0_0&agrr=0&orderid=0,2",
    headers=headers,
)
print(response)  # 206 : 访问正常，成功获取部分内容

# with open("sp1202_biliDL.mp4", "wb") as f:
#     f.write(response.content)
# 无法正常打开，不可以通过修改后缀名强制转换

with open("sp1202_biliDL.mp4", "wb") as f:
    f.write(response.content)
# 把range注释掉，不带range，可以请求到完整的视频，但是没有声音
# 获取声音需要挨个尝试，b站的情况 链接中间的数字中有 xxxxxx-1-30216 大概率有可能是音频
