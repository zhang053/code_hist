"""
异步io的方案

    遇到等待，执行其他的任务
    短时间会发送大量请求，需要加间隔
"""

# request 不支持异步
# aiohttp 支持异步
import requests
from lxml import etree
import aiohttp
import asyncio
from requests import session
import re


class NovelSpider:
    def __init__(self, url):
        self.url = url
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36"
        }

    # 爬取所有的章节链接
    def get_hrefs(self):
        r = requests.get(self.url, headers=self.headers)
        HTML = etree.HTML(r.text)
        hrefs = HTML.xpath("//ul[@class='info']/li/a/@href")
        hrefs = ["https://www.biquge365.net" + href for href in hrefs]
        return hrefs

    # 单个章节标题和内容的爬取
    async def get_chapter(self, session, href):
        async with session.get(url=href, headers=self.headers) as r:
            HTML = etree.HTML(await r.text())
            title = HTML.xpath("//h1/text()")[0]
            # 处理标题，去掉非法文字
            title = re.sub(r"[\\/:*?\"<>|]", " ", title)
            content = HTML.xpath("//div[@id='txt']/text()")
            content = "\n".join(content)
            await self.save_txt(title, content)

    # 保存.txt文件
    async def save_txt(self, title, content):
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(None, self.save_txt_sync, title, content)

    # 同步的写入方法, 供异步使用
    def save_txt_sync(self, title, content):
        with open(f"Novel/{title}.txt", "w", encoding="utf-8") as f:
            f.write(content)
            print(f"save successful -> {title}")

    # 入口
    # 使用async异步，需要把函数定义为async函数
    async def run(self):
        hrefs = self.get_hrefs()
        # 创建异步http客户端会话
        async with aiohttp.ClientSession() as session:
            # 创建异步任务列表
            tasks = [self.get_chapter(session, href) for href in hrefs]
            await asyncio.gather(*tasks)


if __name__ == "__main__":
    spider = NovelSpider("https://www.biquge365.net/newbook/78201/")
    asyncio.run(spider.run())
