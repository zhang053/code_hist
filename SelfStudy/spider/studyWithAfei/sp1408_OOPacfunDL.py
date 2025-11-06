"""
需要解决的问题
    合并的txt文件需要在请求到的时候就创建
    m3u8的链接地址，需要通过视频链接的html文档中获取
"""

import requests
import re
import json
from jsonpath import jsonpath
import time
import os
import subprocess
import shutil


class AcFun:
    def __init__(self, url):
        self.url = url
        self.m3u8_headers = {
            "Accept": "*/*",
            "Accept-Language": "ja,en;q=0.9,en-GB;q=0.8,en-US;q=0.7,zh-CN;q=0.6,zh;q=0.5",
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "Origin": "https://www.acfun.cn",
            "Pragma": "no-cache",
            "Referer": "https://www.acfun.cn/",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-site",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36 Edg/141.0.0.0",
            "sec-ch-ua": '"Microsoft Edge";v="141", "Not?A_Brand";v="8", "Chromium";v="141"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
        }
        self.ts_headers = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36 Edg/139.0.0.0"
        }
        self.name = ""

    # 创建临时缓存文件，比如ts文件
    def create_dir(self):
        self.name = "sp1404_temp"
        os.makedirs(self.name, exist_ok=True)

    # 获取html文档
    def get_html(self):
        headers = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36 Edg/139.0.0.0"
        }
        response = requests.get(self.url, headers=headers)
        print(response)
        return response.text

    # 获取m3u8链接
    def get_m3u8_url(self, html):
        p = re.compile(r"window.pageInfo = window.videoInfo =(.+?});")
        result = p.findall(html)[0]
        data = json.loads(result)
        # 写入json文件，方便分析
        # with open("sp1409_temp_json.json", "w", encoding="utf-8") as f:
        #     json.dump(data, f, ensure_ascii=False, indent=4)
        ksPlayJson = data["currentVideoInfo"]["ksPlayJson"]
        ksPlayData = json.loads(ksPlayJson)
        # print(
        #     ksPlayData["adaptationSet"][0]["representation"][0]["url"]
        # )  # 列表的第一个，画质最高
        ## 使用jsonpath获取
        return jsonpath(ksPlayData, "$..representation[0]..url")[0]

    # 提取所有ts的链接地址
    def get_ts_urls(self, m3u8_url):
        response = requests.get(m3u8_url, headers=self.m3u8_headers)
        txt = response.text
        lines = txt.split("\n")
        ts_urls = []
        for line in lines:
            if line.strip() and not line.startswith("#"):
                # fmt: off
                ts_urls.append("https://tx-safety-video.acfun.cn/mediacloud/acfun/acfun_video/"+line)
                # fmt: on
        print(len(ts_urls))
        return ts_urls

    # 下载所有ts分片
    def download_ts_urls(self, ts_urls):
        txt = ""
        for index, ts_url in enumerate(ts_urls):
            resp = requests.get(ts_url, headers=self.ts_headers)
            with open(f"{self.name}/{index}.ts", "wb") as f:
                f.write(resp.content)
            print(f"成功下载{index+1}.ts 文件，总共{len(ts_urls)}个文件")
            txt += f"file {index}.ts\n"
            time.sleep(0.5)
        # 创建txt文件
        with open(f"{self.name}/list.txt", "w", encoding="utf-8") as f:
            f.write(txt)
        print("创建list.txt文件成功")

    # 合并ts文件
    def merge_ts(self):
        # fmt: off
        subprocess.run(
            [
                "ffmpeg", # ffmpeg命令
                "-f", "concat", # 指定格式为concat
                "-safe", "0", # 允许输入文件中的相对路径
                "-i", f"{self.name}/list.txt", # 指定输入文件
                "-c", "copy", # 指定编码方式为copy
                "sp1409_output.mp4", # 指定输出文件为mp4
                "-y" # 允许覆盖输出文件
            ]
        )
        # fmt: on
        print("合并成功!输出文件为sp1409_output.mp4")

    def delete_temp_dir(self):
        # os命令不能删除
        shutil.rmtree(self.name)
        print("已删除临时文件")

    def run(self):
        html = self.get_html()  # 请求html文件
        m3u8_url = self.get_m3u8_url(html)  # 获取m3u8链接
        ts_urls = self.get_ts_urls(m3u8_url)  # 获取所有ts的链接地址
        self.create_dir()  # 创建文件夹
        self.download_ts_urls(ts_urls)  # 下载ts链接
        self.merge_ts()  # 合并ts文件
        self.delete_temp_dir()


if __name__ == "__main__":
    url = "https://www.acfun.cn/v/ac43624858"
    ac = AcFun(url)
    ac.run()
