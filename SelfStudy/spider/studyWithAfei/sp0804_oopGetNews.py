import requests
from jsonpath import jsonpath
from itertools import zip_longest


class GetNews:
    def __init__(self):
        self.cookies = {
            "csrftoken": "FlQbWnSE3iqWkY33mXENKmCCiaoVHhsN",
            "Hm_lvt_d8ac74031a6495039421daa89265b01d": "1758430277",
            "HMACCOUNT": "42F592952044B1A2",
            "Hm_lpvt_d8ac74031a6495039421daa89265b01d": "1758430303",
        }
        self.headers = {
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "Accept-Language": "ja,en;q=0.9,en-GB;q=0.8,en-US;q=0.7,zh-CN;q=0.6,zh;q=0.5",
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "Pragma": "no-cache",
            "Referer": "https://www.xfz.cn/",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36 Edg/140.0.0.0",
            "X-Requested-With": "XMLHttpRequest",
            "sec-ch-ua": '"Chromium";v="140", "Not=A?Brand";v="24", "Microsoft Edge";v="140"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
        }
        self.params = {
            "p": "1",
            "n": "10",
            # "type": "",
        }

    def RequestJson(self):
        response = requests.get(
            "https://www.xfz.cn/api/website/articles/",
            params=self.params,
            cookies=self.cookies,
            headers=self.headers,
        )
        print(response)
        data = response.json()
        print(len(data["data"]))
        self.news_title = jsonpath(data, "$..title")
        self.news_intros = jsonpath(data, "$..intro")
        self.news_times = jsonpath(data, "$..time")
        self.news_photos = jsonpath(data, "$.data[*].photo")
        self.news_authors = jsonpath(data, "$..author.authors[0].name")

    def Output(self):
        """
        方法1 循环获取内容，然后添加
        弊端：在for循环中使用with open 每次循环都要打开关闭文件
            I/O操作相对耗费时间
        for i in range(len(self.titles)):
            title = self.titles[i]
            time = self.times[i]
            author = self.authors[i]
            txt = f"标题：{title},时间：{time},编辑：{author}"
            with open("News.txt", "a", encoding="utf-8") as f:
                f.write(txt)
                f.write("\n")
                # "a"是追加操作
        """
        """
        # 方法2 外层打开文件，然后循环逐行写入
        # 只打开一次，执行速度相对更快
        with open("News2.txt", "w", encoding="utf-8") as f:
            for i in range(len(self.news_title)):
                title = self.news_title[i]
                time = self.news_times[i]
                author = self.news_authors[i]
                txt2 = f"标题：{title},时间：{time},编辑：{author}"
                f.write(txt2)
                f.write("\n")
        """

        # 方式3 先构建所有内容然后再写入
        # 好处：只要一次i/o打开，打开写入。其他的在代码中实现
        # 弊端：如果在代码中用result变量接的话，如果数据量很庞大的话，因为变量使用未被删除前在内存中，如果数据量很多，然后
        # 如果有这种情况，可以把循环分割成几次，来分段读写
        result = ""
        for i in range(len(self.news_title)):
            title = self.news_title[i]
            time = self.news_times[i]
            author = self.news_authors[i]
            txt3 = f"标题：{title},时间：{time},编辑：{author}"
            result += txt3 + "\n"
        with open("News3.txt", "w", encoding="utf-8") as f:
            f.write(result)

    def run(self):
        self.RequestJson()
        self.Output()


if __name__ == "__main__":
    get_news = GetNews()
    get_news.run()
