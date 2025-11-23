"""
多线程
    适合爬虫

    通常使用在发送几千次请求的爬虫
"""

"""
多线程爬虫任务
"""
import requests
from lxml import etree
from concurrent.futures import ThreadPoolExecutor


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
    def get_chapter(self, href):
        r = requests.get(url=href, headers=self.headers)
        HTML = etree.HTML(r.text)
        title = HTML.xpath("//h1/text()")[0]
        content = HTML.xpath("//div[@id='txt']/text()")
        content = "\n".join(content)
        self.save_txt(title, content)

    # 保存.txt文件
    def save_txt(self, title, content):
        with open(f"Novel/{title}.txt", "w", encoding="utf-8") as f:
            f.write(content)

    # 入口
    def run(self):
        hrefs = self.get_hrefs()
        # # 多半时间浪费在读写上
        # for href in hrefs:
        #     self.get_chapter(href)

        # 多线程
        with ThreadPoolExecutor(max_workers=8) as p:  # 开8个线程
            p.map(self.get_chapter, hrefs)
            # 可以发现，下载的顺序不一样，哪个先执行完


if __name__ == "__main__":
    spider = NovelSpider("https://www.biquge365.net/newbook/78201/")
    spider.run()
