# 异步 获取豆瓣 https://movie.douban.com/top250
# https://movie.douban.com/top250?start=25&filter=

import requests
from lxml import etree
import asyncio
import aiohttp
import re
from fake_useragent import UserAgent


class douban:
    def __init__(self):
        ua = UserAgent()
        ua_output = ua.random
        self.headers = {"user-agent": ua_output}

    # 解析请求的内容，获取标题，评分
    async def get_content(self, session, url):
        async with session.get(url, headers=self.headers) as response:
            HTML = await response.text()
            HTML = etree.HTML(HTML)
            # 获取电影名
            titles = HTML.xpath(
                '//div[@id="content"]//div[@class="hd"]//span[@class="title"][1]/text()'
            )
            # 获取评分
            rate = HTML.xpath('//span[@class="rating_num"]/text()')
            for t, r in zip(titles, rate):
                t.strip()
                title_clean = re.sub(r"[\\/:*?\"<>|]", " ", t)
                line = f"{t}\t{r}"
                await self.save_text(line)

    async def save_text(self, line):
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(None, self.save_file, line)

    def save_file(self, line):
        with open("4.1_result_douban.txt", "a", encoding="utf-8") as f:
            f.write(line + "\n")

    async def run(self):
        # 第一页到第十页
        urls = []
        for i in range(10):
            print(f"正在获取第{i + 1}页")
            url = f"https://movie.douban.com/top250?start={i*25}"
            urls.append(url)

        self.save_file(f"电影名\t评分")
        async with aiohttp.ClientSession() as session:
            tasks = [self.get_content(session, url) for url in urls]
            await asyncio.gather(*tasks)


if __name__ == "__main__":
    d = douban()
    asyncio.run(d.run())
