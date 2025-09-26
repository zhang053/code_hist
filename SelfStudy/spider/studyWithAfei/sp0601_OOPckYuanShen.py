import requests
from bs4 import BeautifulSoup
import time
import os
import time

"""
爬取小说需要的功能
1. 访问初始的所有章节页面
   - 提取所有章节的url
2. 访问章节的url
   - 提取标题，提取文字内容
3. 保存内容成.txt

"""


class NovelSpider:
    # 访问初始页面
    # url 创建类的参数/可以在写死，但是如果要换书的时候，得修改内部代码，所以定义初始
    # headers 后续还有请求，headers可以共用
    def __init__(self, url):
        self.url = url
        self.headers = {
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "accept-language": "ja,en;q=0.9,en-GB;q=0.8,en-US;q=0.7,zh-CN;q=0.6,zh;q=0.5",
            "cache-control": "no-cache",
            "pragma": "no-cache",
            "priority": "u=0, i",
            "referer": "https://www.69shuba.com/modules/article/search.php",
            "sec-ch-ua": '"Chromium";v="140", "Not=A?Brand";v="24", "Microsoft Edge";v="140"',
            "sec-ch-ua-arch": '"x86"',
            "sec-ch-ua-bitness": '"64"',
            "sec-ch-ua-full-version": '"140.0.3485.66"',
            "sec-ch-ua-full-version-list": '"Chromium";v="140.0.7339.133", "Not=A?Brand";v="24.0.0.0", "Microsoft Edge";v="140.0.3485.66"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-model": '""',
            "sec-ch-ua-platform": '"Windows"',
            "sec-ch-ua-platform-version": '"15.0.0"',
            "sec-fetch-dest": "document",
            "sec-fetch-mode": "navigate",
            "sec-fetch-site": "same-origin",
            "sec-fetch-user": "?1",
            "upgrade-insecure-requests": "1",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36 Edg/140.0.0.0",
            # 'cookie': 'zh_choose=s; _ga=GA1.1.513912616.1754138004; _ym_uid=175431646499432818; _lr_env_src_ats=false; _sharedID=64154fc2-22c5-4b2d-af0a-f55e359b9b8f; _sharedID_cst=zix7LPQsHA%3D%3D; sharedid=74fa1d2d-c84f-44b6-adaa-32a838fff58a; sharedid_cst=kaULaw%3D%3D; cto_bundle=fOxyo19RZkh0Z1glMkZ2SndwZzdrV1BiZEUxSzglMkZCWWVoMnl0SnAwZ3pwdjROTG5oQnBqbW9La0tLZTluOTBYdUs4RWVyME0zZGpyZllpTmo2N3hwWTBDOWdKJTJCalJ1cVZxaWhvQW1jMkIyeEZhTWVMbHZQZ3VRMW1XOGlKRUZLQUNjN0xKYkc2MDdnYXd1ZE1CUkNjQzQ1SXBENHclM0QlM0Q; cto_bidid=8mYetV9DRSUyRkFOdENSQiUyQk1jRENReXB1SlpyWmNsVWtrNEVSRGhJdGdYMnRFUzNJV0lySkNTMkxMVmtZbTRVQUxBMXlhTEowbG15dlFldCUyQmJEWFhQMyUyRnFySHdiN2Z5ZmZtNVBKNCUyRnF3WWwxd2VYMWslM0Q; cto_dna_bundle=bHuT1F9Tdzc2bnlwUFpCZjNLb21uM092VzVjd2x6QlRrMFJsRkNCaDFORVlEZHc5WjdOZThzanN2RTZ6SkVORDh6TGd0R1g0c1N2WEFzb01xQTk4c3FLJTJGQkt3JTNEJTNE; pbjs-id5id=%7B%22signature%22%3A%22ID5_As27vNz947cXo-oC2WQOBmktq54ViVUG2kIB-ykPaMOoDa9hQ3IG5ct1wPeZExS9tErk61sbJnn49mrRzroqKr5HEMP0YwHfAcoON0qut2N2V0bSvqjkO3r5ENedVPkFb1aUGFW0hDCrXKkq83FTjs_WjABnOrobkCEFMpdo4KvbFInYGj8%22%2C%22created_at%22%3A%222025-08-08T04%3A28%3A01Z%22%2C%22id5_consent%22%3Atrue%2C%22original_uid%22%3A%22ID5*IUqn7Xu9obCQbCK4UlDUd-xP4d-NL3dH4SLxeEFLq3067b01x9cRaXpNyOFPNcig%22%2C%22universal_uid%22%3A%22ID5*AOM2GtW1C5RjpatBVhKlFY6oqmcHCx3M581qwxYyoJo67UflKdSw6LCCBUjS3RWe%22%2C%22link_type%22%3A1%2C%22cascade_needed%22%3Atrue%2C%22privacy%22%3A%7B%22jurisdiction%22%3A%22other%22%2C%22id5_consent%22%3Atrue%7D%2C%22ext%22%3A%7B%22linkType%22%3A1%2C%22pba%22%3A%22zdid%2FBooWl%2FM%2B0XzZX5iwijps2mKM1WffAZ2QQKO8vNIOqmlV8o1ndQNo7XZ%2B6kn%22%7D%2C%22cache_control%22%3A%7B%22max_age_sec%22%3A7200%7D%2C%22ids%22%3A%7B%22id5id%22%3A%7B%22eid%22%3A%7B%22source%22%3A%22id5-sync.com%22%2C%22uids%22%3A%5B%7B%22id%22%3A%22ID5*AOM2GtW1C5RjpatBVhKlFY6oqmcHCx3M581qwxYyoJo67UflKdSw6LCCBUjS3RWe%22%2C%22atype%22%3A1%2C%22ext%22%3A%7B%22linkType%22%3A1%2C%22pba%22%3A%22zdid%2FBooWl%2FM%2B0XzZX5iwijps2mKM1WffAZ2QQKO8vNIOqmlV8o1ndQNo7XZ%2B6kn%22%7D%7D%5D%7D%7D%7D%7D; pbjs-id5id_cst=kaULaw%3D%3D; pbjs-id5id_last=Fri%2C%2008%20Aug%202025%2007%3A45%3A27%20GMT; _ym_uid_cst=znv0HA%3D%3D; jieqiHistory=37740-35228958-%25u7B2C403%25u7AE0%2520%25u6700%25u7EC8-1757777057%7C90072-40621179-%25u7B2C96%25u7AE0%2520%25u90A3%25u5C31%25u7EA6%25u4F1A%25u5427-1757776868%7C51592-37594019-%25u65B0%25u4E66%25u300A%25u65E7%25u795E%25u4E4B%25u5DC5%25u300B%25u5DF2%25u4E0A%25u4F20-1757431879%7C58425-40302491-%25u7B2C491%25u7AE0%2520%25u75BE%25u901F%25u8FFD%25u8E2A-1757398771%7C43484-40592015-1259.%25u7B2C1254%25u7AE0%2520%25u7B49%25u4EE5%25u540E%25u6211%25u4EEC%25u518D%25u5BF9%25u6218%25u4E00%25u573A%25uFF01-1757344506%7C57909-39377756-%25u7B2C370%25u7AE0%2520%25u756A%25u5916%25uFF1A%25u5361%25u8299%25u5361-1755495112; PHPSESSID=7amn261lasc5qetdg6k1bcvg20; jieqiUserInfo=jieqiUserId%3D1694798%2CjieqiUserUname%3Dshohiro5531%2CjieqiUserName%3Dshohiro5531%2CjieqiUserGroup%3D3%2CjieqiUserGroupName%3D%26%23x666E%3B%26%23x901A%3B%26%23x4F1A%3B%26%23x5458%3B%2CjieqiUserVip%3D0%2CjieqiUserHonorId%3D%2CjieqiUserHonor%3D%26%23x65B0%3B%26%23x624B%3B%26%23x4E0A%3B%26%23x8DEF%3B%2CjieqiUserToken%3D232d7d8793e7a5115d781e4ac44420a2%2CjieqiCodeLogin%3D0%2CjieqiCodePost%3D0%2CjieqiNewMessage%3D0%2CjieqiUserPassword%3Dc927d3e096e7385d2053e5f72d7b6ddf%2CjieqiUserLogin%3D1757900157; jieqiVisitInfo=jieqiUserLogin%3D1757900157%2CjieqiUserId%3D1694798; cf_clearance=LuQ4nqDjcciYm3MbHIpOScLQLVZcJBUztyYugTorMic-1757900162-1.2.1.1-tt2NLQYy4y4cRKHYvA0Pk4ZNhGUljd0yZK8bRibJys8OQDhJzzkVCfMXonIx9Z85GPNzursPxWtYP3subC.9EZv7x1Bq3hgSp484UGmDx0z1WfJ4Cq9OdSIxtFf8RszDe3WSMabcS7hkLCOyutcZSQGmzYE7IytYLi1hff.TdHtczhorb49mJ7wR.d6FL_CI8UvLKNryAJtixHlGSYbAXsIkIdobsRbs9WSHytEcygM; shuba_userverfiy=1757900162@aa405edf3ca1bce990ae917f67204433; jieqiVisitTime=jieqiArticlesearchTime%3D1757900163; shuba=6164-1363-18926-1347; _ga_04LTEL5PWY=GS2.1.s1757900164$o58$g1$t1757900166$j58$l0$h0',
        }
        self.cookies = {
            "zh_choose": "s",
            "_ga": "GA1.1.513912616.1754138004",
            "_ym_uid": "175431646499432818",
            "_lr_env_src_ats": "false",
            "_sharedID": "64154fc2-22c5-4b2d-af0a-f55e359b9b8f",
            "_sharedID_cst": "zix7LPQsHA%3D%3D",
            "sharedid": "74fa1d2d-c84f-44b6-adaa-32a838fff58a",
            "sharedid_cst": "kaULaw%3D%3D",
            "cto_bundle": "fOxyo19RZkh0Z1glMkZ2SndwZzdrV1BiZEUxSzglMkZCWWVoMnl0SnAwZ3pwdjROTG5oQnBqbW9La0tLZTluOTBYdUs4RWVyME0zZGpyZllpTmo2N3hwWTBDOWdKJTJCalJ1cVZxaWhvQW1jMkIyeEZhTWVMbHZQZ3VRMW1XOGlKRUZLQUNjN0xKYkc2MDdnYXd1ZE1CUkNjQzQ1SXBENHclM0QlM0Q",
            "cto_bidid": "8mYetV9DRSUyRkFOdENSQiUyQk1jRENReXB1SlpyWmNsVWtrNEVSRGhJdGdYMnRFUzNJV0lySkNTMkxMVmtZbTRVQUxBMXlhTEowbG15dlFldCUyQmJEWFhQMyUyRnFySHdiN2Z5ZmZtNVBKNCUyRnF3WWwxd2VYMWslM0Q",
            "cto_dna_bundle": "bHuT1F9Tdzc2bnlwUFpCZjNLb21uM092VzVjd2x6QlRrMFJsRkNCaDFORVlEZHc5WjdOZThzanN2RTZ6SkVORDh6TGd0R1g0c1N2WEFzb01xQTk4c3FLJTJGQkt3JTNEJTNE",
            "pbjs-id5id": "%7B%22signature%22%3A%22ID5_As27vNz947cXo-oC2WQOBmktq54ViVUG2kIB-ykPaMOoDa9hQ3IG5ct1wPeZExS9tErk61sbJnn49mrRzroqKr5HEMP0YwHfAcoON0qut2N2V0bSvqjkO3r5ENedVPkFb1aUGFW0hDCrXKkq83FTjs_WjABnOrobkCEFMpdo4KvbFInYGj8%22%2C%22created_at%22%3A%222025-08-08T04%3A28%3A01Z%22%2C%22id5_consent%22%3Atrue%2C%22original_uid%22%3A%22ID5*IUqn7Xu9obCQbCK4UlDUd-xP4d-NL3dH4SLxeEFLq3067b01x9cRaXpNyOFPNcig%22%2C%22universal_uid%22%3A%22ID5*AOM2GtW1C5RjpatBVhKlFY6oqmcHCx3M581qwxYyoJo67UflKdSw6LCCBUjS3RWe%22%2C%22link_type%22%3A1%2C%22cascade_needed%22%3Atrue%2C%22privacy%22%3A%7B%22jurisdiction%22%3A%22other%22%2C%22id5_consent%22%3Atrue%7D%2C%22ext%22%3A%7B%22linkType%22%3A1%2C%22pba%22%3A%22zdid%2FBooWl%2FM%2B0XzZX5iwijps2mKM1WffAZ2QQKO8vNIOqmlV8o1ndQNo7XZ%2B6kn%22%7D%2C%22cache_control%22%3A%7B%22max_age_sec%22%3A7200%7D%2C%22ids%22%3A%7B%22id5id%22%3A%7B%22eid%22%3A%7B%22source%22%3A%22id5-sync.com%22%2C%22uids%22%3A%5B%7B%22id%22%3A%22ID5*AOM2GtW1C5RjpatBVhKlFY6oqmcHCx3M581qwxYyoJo67UflKdSw6LCCBUjS3RWe%22%2C%22atype%22%3A1%2C%22ext%22%3A%7B%22linkType%22%3A1%2C%22pba%22%3A%22zdid%2FBooWl%2FM%2B0XzZX5iwijps2mKM1WffAZ2QQKO8vNIOqmlV8o1ndQNo7XZ%2B6kn%22%7D%7D%5D%7D%7D%7D%7D",
            "pbjs-id5id_cst": "kaULaw%3D%3D",
            "pbjs-id5id_last": "Fri%2C%2008%20Aug%202025%2007%3A45%3A27%20GMT",
            "_ym_uid_cst": "znv0HA%3D%3D",
            "jieqiHistory": "37740-35228958-%25u7B2C403%25u7AE0%2520%25u6700%25u7EC8-1757777057%7C90072-40621179-%25u7B2C96%25u7AE0%2520%25u90A3%25u5C31%25u7EA6%25u4F1A%25u5427-1757776868%7C51592-37594019-%25u65B0%25u4E66%25u300A%25u65E7%25u795E%25u4E4B%25u5DC5%25u300B%25u5DF2%25u4E0A%25u4F20-1757431879%7C58425-40302491-%25u7B2C491%25u7AE0%2520%25u75BE%25u901F%25u8FFD%25u8E2A-1757398771%7C43484-40592015-1259.%25u7B2C1254%25u7AE0%2520%25u7B49%25u4EE5%25u540E%25u6211%25u4EEC%25u518D%25u5BF9%25u6218%25u4E00%25u573A%25uFF01-1757344506%7C57909-39377756-%25u7B2C370%25u7AE0%2520%25u756A%25u5916%25uFF1A%25u5361%25u8299%25u5361-1755495112",
            "PHPSESSID": "7amn261lasc5qetdg6k1bcvg20",
            "jieqiUserInfo": "jieqiUserId%3D1694798%2CjieqiUserUname%3Dshohiro5531%2CjieqiUserName%3Dshohiro5531%2CjieqiUserGroup%3D3%2CjieqiUserGroupName%3D%26%23x666E%3B%26%23x901A%3B%26%23x4F1A%3B%26%23x5458%3B%2CjieqiUserVip%3D0%2CjieqiUserHonorId%3D%2CjieqiUserHonor%3D%26%23x65B0%3B%26%23x624B%3B%26%23x4E0A%3B%26%23x8DEF%3B%2CjieqiUserToken%3D232d7d8793e7a5115d781e4ac44420a2%2CjieqiCodeLogin%3D0%2CjieqiCodePost%3D0%2CjieqiNewMessage%3D0%2CjieqiUserPassword%3Dc927d3e096e7385d2053e5f72d7b6ddf%2CjieqiUserLogin%3D1757900157",
            "jieqiVisitInfo": "jieqiUserLogin%3D1757900157%2CjieqiUserId%3D1694798",
            "cf_clearance": "LuQ4nqDjcciYm3MbHIpOScLQLVZcJBUztyYugTorMic-1757900162-1.2.1.1-tt2NLQYy4y4cRKHYvA0Pk4ZNhGUljd0yZK8bRibJys8OQDhJzzkVCfMXonIx9Z85GPNzursPxWtYP3subC.9EZv7x1Bq3hgSp484UGmDx0z1WfJ4Cq9OdSIxtFf8RszDe3WSMabcS7hkLCOyutcZSQGmzYE7IytYLi1hff.TdHtczhorb49mJ7wR.d6FL_CI8UvLKNryAJtixHlGSYbAXsIkIdobsRbs9WSHytEcygM",
            "shuba_userverfiy": "1757900162@aa405edf3ca1bce990ae917f67204433",
            "jieqiVisitTime": "jieqiArticlesearchTime%3D1757900163",
            "shuba": "6164-1363-18926-1347",
            "_ga_04LTEL5PWY": "GS2.1.s1757900164$o58$g1$t1757900166$j58$l0$h0",
        }
        self.chap_links = []
        self.novel_name = None

    # 获取所有章节的链接
    def get_hrefs(self):
        # 初始页面

        resp = requests.get(self.url, headers=self.headers, cookies=self.cookies)
        print(resp)
        soup1 = BeautifulSoup(resp.text, "lxml")

        # 获取小说标题,并创建以该小说为名的文件夹
        self.novel_name = soup1.select("h1")[0].text
        os.makedirs(self.novel_name, exist_ok=True)

        # 获得有全部章节的页面的链接
        chaps = soup1.select(".mybox > a")[0]
        resp2 = requests.get(chaps["href"], headers=self.headers, cookies=self.cookies)
        soup2 = BeautifulSoup(resp2.text, "lxml")
        # 获取每一个章节的链接
        get_links = soup2.select("#catalog > ul > li >a")
        self.chap_links = [chap["href"] for chap in get_links]

    # 单章节的标题和内容,然后保存成文件夹
    def get_chapter(self, href):
        resp3 = requests.get(href, headers=self.headers, cookies=self.cookies)
        soup3 = BeautifulSoup(resp3.text, "lxml")
        # 获取章节标题
        chap_title = soup3.select(".txtnav > h1")[0].text
        # 获取章节内容
        chap_content = soup3.select("div.txtnav")[0].get_text("\n", strip=True)
        # 保存
        # 最好不要在函数中嵌套另一个函数，会导致可读性降低
        # self.save_chapters(chap_title, chap_content)
        return chap_title, chap_content

    # 保存文件
    def save_chapters(self, chap_title, chap_content):
        # fmt: off
        with open(f"{self.novel_name}/{chap_title}.txt", "w", encoding="utf-8") as f:
        # fmt: on
            f.write(chap_content)
            print(chap_title + "保存完成")

    # 启动
    def run(self):
        self.get_hrefs()
        for c in self.chap_links:
            title, content = self.get_chapter(c)
            self.save_chapters(title, content)
            time.sleep(1.5)


if __name__ == "__main__":
    # 传入初始页面的url，后续如果要换书，只需要修改url
    spider = NovelSpider("https://www.69shuba.com/book/58375.htm")
    spider.run()
