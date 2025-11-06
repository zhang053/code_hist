"""
分段下载
-如果文件很大，一旦下载失败，需要重新下载，如果从头开始，效率太低，分段下载可以解决这个问题

并非所有的m4s没有range都可以全部下载

携带range参数进行下载
在Request Headers 中的range参数：bytes=260083-292526

1. 首先需要知道总长度
    - 打开m4s的链接，找到 headers --> Response headers --> Content-Range: bytes 260083-292526/1273637
    - 斜杠("/")后的数字是总长度 1273637

2. 分段发送请求
    -
"""

import requests

# fmt: off
url = "https://upos-sz-mirrorcosov.bilivideo.com/upgcxcode/97/18/25689591897/25689591897-1-30216.m4s?e=ig8euxZM2rNcNbdlhoNvNC8BqJIzNbfqXBvEqxTEto8BTrNvN0GvT90W5JZMkX_YN0MvXg8gNEV4NC8xNEV4N03eN0B5tZlqNxTEto8BTrNvNeZVuJ10Kj_g2UB02J0mN0B5tZlqNCNEto8BTrNvNC7MTX502C8f2jmMQJ6mqF2fka1mqx6gqj0eN0B599M=&trid=bc1d6e425b4b456086009b5dd943417u&mid=0&os=cosovbv&oi=3681062357&nbs=1&platform=pc&deadline=1761064515&gen=playurlv3&og=cos&uipk=5&upsig=185921d51bf71f73be4e9e15de01a003&uparams=e,trid,mid,os,oi,nbs,platform,deadline,gen,og,uipk&bvc=vod&nettype=0&bw=49702&agrr=0&buvid=E47527FD-ADA4-388B-0E51-FAE3F500DE0A93607infoc&build=0&dl=0&f=u_0_0&orderid=0,2"
# fmt: on
headers = {
    "referer": url,
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36 Edg/141.0.0.0",
}

# range获取的值越小越好，因为只需要获取到回应头的后面的总长度，不宜太小，有可能有最小限制
# response = requests.get(
#     "https://upos-sz-mirrorcosov.bilivideo.com/upgcxcode/97/18/25689591897/25689591897-1-30216.m4s?e=ig8euxZM2rNcNbdlhoNvNC8BqJIzNbfqXBvEqxTEto8BTrNvN0GvT90W5JZMkX_YN0MvXg8gNEV4NC8xNEV4N03eN0B5tZlqNxTEto8BTrNvNeZVuJ10Kj_g2UB02J0mN0B5tZlqNCNEto8BTrNvNC7MTX502C8f2jmMQJ6mqF2fka1mqx6gqj0eN0B599M=&platform=pc&trid=e1f531f6ba484002afffb89c05e4162u&deadline=1759943091&oi=3681062357&og=cos&mid=0&nbs=1&uipk=5&gen=playurlv3&os=cosovbv&upsig=bcd23ecd505f4d251b8656fec836366e&uparams=e,platform,trid,deadline,oi,og,mid,nbs,uipk,gen,os&bvc=vod&nettype=0&bw=49702&f=u_0_0&agrr=0&buvid=E47527FD-ADA4-388B-0E51-FAE3F500DE0A93607infoc&build=0&dl=0&orderid=0,2",
#     headers=headers,
# )

"""
如果只为了获取响应头的参数的话可以用request.head
只请求头的信息就结束了，不会下载资源
"""
response = requests.head(
    url,
    headers=headers,
)
print(response)
# print(response.headers)  # 获取响应头,请求发过去获得的回应
print(response.headers["Content-Range"])  # bytes 260083-292526/1273637
content_range = response.headers["Content-Range"]
total_range = int(content_range.split("/")[1])
# 以 / 进行分割，1的意思是第二个，取后半部分
print(total_range)

# 获取到总长度后，规划分段请求的参数
# content-range格式是 bytes 0-99/1273637 起始是0，终止是总长度-1
# bytes 0-99 包含0和9 ， 下一段应该从10开始
chunk = 1024 * 1024 * 1  # 单次请求1M
# 通常是3-5M，因为本次获取内容比较小，所以获取1M

for i in range(0, total_range, chunk):
    start = i
    end = min(i + chunk - 1, total_range - 1)
    # 在最后一段的时候避免超出
    print(f"正在下载{start}-{end}")
    # 构建请求头
    headers["range"] = f"bytes={start}-{end}"
    response = requests.get(url, headers=headers)
    with open("sp1302_DLbilibili.mp3", "ab") as f:
        f.write(response.content)
print("finish DL")
