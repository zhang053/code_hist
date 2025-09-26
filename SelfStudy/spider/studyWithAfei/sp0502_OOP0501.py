# 面向对象写法

import requests
from bs4 import BeautifulSoup
import time
import os


class NovelSpider:

    def __init__(self, url):
        self.url = url
        self.headers = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36 Edg/139.0.0.0"
        }
        self.novel_title = None

    # 爬取所有的章节url
    def get_hrefs(self):
        r = requests.get(self.url, headers=self.headers)
        sp = BeautifulSoup(r.text, "lxml")

        # 小说名的获取,并创建相对应的文件夹
        self.novel_title = sp.select("h1")[0].text
        os.makedirs(self.novel_title, exist_ok=True)

        # 章节链接的获取
        all_chaps = sp.select(".info > li > a")
        chap_links = ["https://www.biquge365.net" + el["href"] for el in all_chaps]
        return chap_links

    # 单章节的标题和内容的爬取
    def get_chapter(self, href):
        response = requests.get(url=href, headers=self.headers)
        sp1 = BeautifulSoup(response.text, "lxml")
        chap_title = sp1.select("#neirong > h1")[0].text
        content = sp1.select("#txt")[0].get_text("\n", strip=True)

        self.save_text(chap_title, content)

    # 保存.txt文件
    def save_text(self, chap_title, content):
        file_name = f"{self.novel_title}/{chap_title}.txt"
        with open(file_name, "w", encoding="utf-8") as f:
            f.write(content)
            print(chap_title + "保存完成")

    def run(self):
        hrefs = self.get_hrefs()
        for href in hrefs:
            self.get_chapter(href)


if __name__ == "__main__":
    spider = NovelSpider("https://www.biquge365.net/newbook/652411/")
    spider.run()
