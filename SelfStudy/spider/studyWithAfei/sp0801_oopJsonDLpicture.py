import requests
import os
from datetime import datetime
import time


class DLImage:

    def __init__(self):
        self.cookies = {
            "BAIDUID": "48E3DE22FA1321E55C136CBB9CB85853:FG=1",
            "newlogin": "1",
            "PSTM": "1756477320",
            "BIDUPSID": "69E5D72C5201B08F2D08B986BC3D835D",
            "BDUSS": "ldISmtOdDlMOVIzflowdEZIMDZ6TWVoekJjdndDclF4Y1dTM2E5bjBrd3FzZWRvRVFBQUFBJCQAAAAAAQAAAAEAAAA0YFSTAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACokwGgqJMBob",
            "BDUSS_BFESS": "ldISmtOdDlMOVIzflowdEZIMDZ6TWVoekJjdndDclF4Y1dTM2E5bjBrd3FzZWRvRVFBQUFBJCQAAAAAAQAAAAEAAAA0YFSTAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACokwGgqJMBob",
            "BAIDUID_BFESS": "48E3DE22FA1321E55C136CBB9CB85853:FG=1",
            "H_PS_PSSID": "63142_63327_64660_64748_64701_64815_64834_64911_64923_64980_65076_65083_65116_65141_65140_65137_65188_65204_65219_65250_65256_65143_65274_65281_65321_65346_65373_65384",
            "BA_HECTOR": "84a104a5a4240l252h0g00a40ka4ag1kcqgm024",
            "ZFY": "XWFlRw1wcYlt:A775Ad5aCT:AGWI:BuWG:BzKb4aehmWLm4:C",
            "BDRCVFR[feWj1Vr5u3D]": "I67x6TjHwwYf0",
            "PSINO": "7",
            "delPer": "0",
            "BDORZ": "B490B5EBF6F3CD402E515D22BCDA1598",
            "H_WISE_SIDS": "64660_64748_64815_64834_64911_64923_64980_65076_65083_65116_65141_65140_65137_65188_65204_65219_65250_65256_65143_65274_65281_65373_65384",
            "arialoadData": "false",
            "ab_sr": "1.0.1_YmFhZTU3ODA5YzgwYjRlNTg0MDlmZmI4ZmM2MTM1NmEyODNkMjA3MzdjODgyZDM2OGNlMzQxZmZjMGE3MzJiZWNmYjJjNjMyODE1OWVlY2NlMTEyNzRlMDI5ZjAzZGZhYmNjNzliNDEyZjI1OWVjZjIxMzlkMjNiZWNhMGI0ZjQyNjVhOGNiYTcwMjVhODY5MDU5MGY3OGEyODM3NmUxZQ==",
        }
        self.headers = {
            "Accept": "application/json, text/plain, */*",
            "Accept-Language": "ja,en;q=0.9,en-GB;q=0.8,en-US;q=0.7,zh-CN;q=0.6,zh;q=0.5",
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "Pragma": "no-cache",
            "Referer": "https://image.baidu.com/search/index?tn=baiduimage&ps=1&ct=201326592&lm=-1&cl=2&nc=1&ie=utf-8&lid=e25e4ff20036b55f&dyTabStr=MCwxMiwzLDEsMiwxMyw3LDYsNSw5&word=%E6%98%94%E6%B6%9F",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36 Edg/140.0.0.0",
            "sec-ch-ua": '"Chromium";v="140", "Not=A?Brand";v="24", "Microsoft Edge";v="140"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            # 'Cookie': 'BAIDUID=48E3DE22FA1321E55C136CBB9CB85853:FG=1; newlogin=1; PSTM=1756477320; BIDUPSID=69E5D72C5201B08F2D08B986BC3D835D; BDUSS=ldISmtOdDlMOVIzflowdEZIMDZ6TWVoekJjdndDclF4Y1dTM2E5bjBrd3FzZWRvRVFBQUFBJCQAAAAAAQAAAAEAAAA0YFSTAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACokwGgqJMBob; BDUSS_BFESS=ldISmtOdDlMOVIzflowdEZIMDZ6TWVoekJjdndDclF4Y1dTM2E5bjBrd3FzZWRvRVFBQUFBJCQAAAAAAQAAAAEAAAA0YFSTAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACokwGgqJMBob; BAIDUID_BFESS=48E3DE22FA1321E55C136CBB9CB85853:FG=1; H_PS_PSSID=63142_63327_64660_64748_64701_64815_64834_64911_64923_64980_65076_65083_65116_65141_65140_65137_65188_65204_65219_65250_65256_65143_65274_65281_65321_65346_65373_65384; BA_HECTOR=84a104a5a4240l252h0g00a40ka4ag1kcqgm024; ZFY=XWFlRw1wcYlt:A775Ad5aCT:AGWI:BuWG:BzKb4aehmWLm4:C; BDRCVFR[feWj1Vr5u3D]=I67x6TjHwwYf0; PSINO=7; delPer=0; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; H_WISE_SIDS=64660_64748_64815_64834_64911_64923_64980_65076_65083_65116_65141_65140_65137_65188_65204_65219_65250_65256_65143_65274_65281_65373_65384; arialoadData=false; ab_sr=1.0.1_YmFhZTU3ODA5YzgwYjRlNTg0MDlmZmI4ZmM2MTM1NmEyODNkMjA3MzdjODgyZDM2OGNlMzQxZmZjMGE3MzJiZWNmYjJjNjMyODE1OWVlY2NlMTEyNzRlMDI5ZjAzZGZhYmNjNzliNDEyZjI1OWVjZjIxMzlkMjNiZWNhMGI0ZjQyNjVhOGNiYTcwMjVhODY5MDU5MGY3OGEyODM3NmUxZQ==',
        }
        self.params = {
            "tn": "resultjson_com",
            # "word": "昔涟",  # 通过run的地方的代码进行控制
            "ie": "utf-8",
            "fp": "result",
            "fr": "",
            "ala": "0",
            "applid": "10980898559100920535",
            # "pn": "0",
            # "rn": "60",
            "nojc": "0",
            "gsm": "1e",
            "newReq": "1",
        }
        self.pic_cookies = {
            "BAIDUID": "48E3DE22FA1321E55C136CBB9CB85853:FG=1",
            "newlogin": "1",
            "PSTM": "1756477320",
            "BIDUPSID": "69E5D72C5201B08F2D08B986BC3D835D",
            "BDUSS": "ldISmtOdDlMOVIzflowdEZIMDZ6TWVoekJjdndDclF4Y1dTM2E5bjBrd3FzZWRvRVFBQUFBJCQAAAAAAQAAAAEAAAA0YFSTAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACokwGgqJMBob",
            "BDUSS_BFESS": "ldISmtOdDlMOVIzflowdEZIMDZ6TWVoekJjdndDclF4Y1dTM2E5bjBrd3FzZWRvRVFBQUFBJCQAAAAAAQAAAAEAAAA0YFSTAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACokwGgqJMBob",
            "BAIDUID_BFESS": "48E3DE22FA1321E55C136CBB9CB85853:FG=1",
            "H_PS_PSSID": "63142_63327_64660_64748_64701_64815_64834_64911_64923_64980_65076_65083_65116_65141_65140_65137_65188_65204_65219_65250_65256_65143_65274_65281_65321_65346_65373_65384",
            "BA_HECTOR": "84a104a5a4240l252h0g00a40ka4ag1kcqgm024",
            "ZFY": "XWFlRw1wcYlt:A775Ad5aCT:AGWI:BuWG:BzKb4aehmWLm4:C",
            "BDRCVFR[feWj1Vr5u3D]": "I67x6TjHwwYf0",
            "PSINO": "7",
            "delPer": "0",
            "BDORZ": "B490B5EBF6F3CD402E515D22BCDA1598",
            "H_WISE_SIDS": "64660_64748_64815_64834_64911_64923_64980_65076_65083_65116_65141_65140_65137_65188_65204_65219_65250_65256_65143_65274_65281_65373_65384",
            "arialoadData": "false",
            "ab_sr": "1.0.1_YmFhZTU3ODA5YzgwYjRlNTg0MDlmZmI4ZmM2MTM1NmEyODNkMjA3MzdjODgyZDM2OGNlMzQxZmZjMGE3MzJiZWNmYjJjNjMyODE1OWVlY2NlMTEyNzRlMDI5ZjAzZGZhYmNjNzliNDEyZjI1OWVjZjIxMzlkMjNiZWNhMGI0ZjQyNjVhOGNiYTcwMjVhODY5MDU5MGY3OGEyODM3NmUxZQ==",
        }
        self.pic_headers = {
            "accept": "image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8",
            "accept-language": "ja,en;q=0.9,en-GB;q=0.8,en-US;q=0.7,zh-CN;q=0.6,zh;q=0.5",
            "cache-control": "no-cache",
            "pragma": "no-cache",
            "priority": "i",
            "referer": "https://image.baidu.com/",
            "sec-ch-ua": '"Chromium";v="140", "Not=A?Brand";v="24", "Microsoft Edge";v="140"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "sec-fetch-dest": "image",
            "sec-fetch-mode": "no-cors",
            "sec-fetch-site": "same-site",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36 Edg/140.0.0.0",
            # 'cookie': 'BAIDUID=48E3DE22FA1321E55C136CBB9CB85853:FG=1; newlogin=1; PSTM=1756477320; BIDUPSID=69E5D72C5201B08F2D08B986BC3D835D; BDUSS=ldISmtOdDlMOVIzflowdEZIMDZ6TWVoekJjdndDclF4Y1dTM2E5bjBrd3FzZWRvRVFBQUFBJCQAAAAAAQAAAAEAAAA0YFSTAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACokwGgqJMBob; BDUSS_BFESS=ldISmtOdDlMOVIzflowdEZIMDZ6TWVoekJjdndDclF4Y1dTM2E5bjBrd3FzZWRvRVFBQUFBJCQAAAAAAQAAAAEAAAA0YFSTAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACokwGgqJMBob; BAIDUID_BFESS=48E3DE22FA1321E55C136CBB9CB85853:FG=1; H_PS_PSSID=63142_63327_64660_64748_64701_64815_64834_64911_64923_64980_65076_65083_65116_65141_65140_65137_65188_65204_65219_65250_65256_65143_65274_65281_65321_65346_65373_65384; BA_HECTOR=84a104a5a4240l252h0g00a40ka4ag1kcqgm024; ZFY=XWFlRw1wcYlt:A775Ad5aCT:AGWI:BuWG:BzKb4aehmWLm4:C; BDRCVFR[feWj1Vr5u3D]=I67x6TjHwwYf0; PSINO=7; delPer=0; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; H_WISE_SIDS=64660_64748_64815_64834_64911_64923_64980_65076_65083_65116_65141_65140_65137_65188_65204_65219_65250_65256_65143_65274_65281_65373_65384; arialoadData=false; ab_sr=1.0.1_YmFhZTU3ODA5YzgwYjRlNTg0MDlmZmI4ZmM2MTM1NmEyODNkMjA3MzdjODgyZDM2OGNlMzQxZmZjMGE3MzJiZWNmYjJjNjMyODE1OWVlY2NlMTEyNzRlMDI5ZjAzZGZhYmNjNzliNDEyZjI1OWVjZjIxMzlkMjNiZWNhMGI0ZjQyNjVhOGNiYTcwMjVhODY5MDU5MGY3OGEyODM3NmUxZQ==',
        }
        self.search = None

    # 获取json数据  ; 参数: 1, pn : 请求起始数量  2, rn: 图片数量
    def ReqJson(self, pn, rn):
        self.params["pn"] = pn
        self.params["rn"] = rn
        response = requests.get(
            "https://image.baidu.com/search/acjson",
            params=self.params,
            cookies=self.cookies,
            headers=self.headers,
        )
        print(response)
        return response.json()["data"]["images"]

    # 下载图片 参数: data 中存储的图片信息的列表
    def DLimg(self, data):
        for img in data:
            url = img["thumburl"]

            # 链接超时，等报错时候的处理，防止程序直接卡死
            try:
                response = requests.get(
                    url,
                    headers=self.pic_headers,
                    cookies=self.pic_cookies,
                    timeout=(5, 20),
                )
            except requests.exceptions.ConnectTimeout:
                print("连接超时，已跳过：", url)
                continue
            except requests.exceptions.RequestException as e:
                print("下载失败：", url, "→", e)
                continue

            # 时间是绝对不会重复的，使用时间戳来命名
            # 精确到毫秒的时间戳
            d = int(datetime.now().timestamp() * 1000)
            # 图片后缀有很多种可能(.png/.jpg/.gif)
            # 百度自己也需要图片格式，所以json数据里一定会有
            # images里的imageFormat
            suffix = img["imageFormat"]  # 后缀的英文单词 suffix
            with open(f"{self.search}/{d}.{suffix}", "wb") as f:
                f.write(response.content)
            #  间隔1秒钟
            time.sleep(1)

    # 启动函数 参数: 1, 搜索的关键词, search  2, 要下载的数量
    def run(self, serach, total):
        self.params["word"] = serach
        self.search = serach
        # 创建文件夹
        os.makedirs(self.search, exist_ok=True)
        # 请求json数据
        #  一次最多请求60, 需要根据要下载的总数量, 来规划请求数量
        for i in range(0, total, 60):
            pn = i
            rn = min(total - i, 60)  # 每次取 60，最后一次取剩下的
            # 发起请求
            data = self.ReqJson(pn, rn)
            print(len(data))
            # 得到数据，传递给下载函数
            self.DLimg(data)


if __name__ == "__main__":
    bdimgDL = DLImage()
    bdimgDL.run("缇里西庇俄丝", 189)  # 获取189张关于昔涟的图片
