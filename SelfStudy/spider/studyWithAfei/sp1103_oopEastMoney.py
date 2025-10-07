# 使用面向对象写法，保存数据使用mongodb
import requests
import re
import time
import json
from pymongo import MongoClient


class Stock:
    def __init__(self):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36 Edg/141.0.0.0",
        }
        self.params = {
            "np": "1",
            "fltt": "1",
            "invt": "2",
            "cb": "jQuery37109155425940039459_1759754393521",  # 这里是可以自定义的
            "fs": "m:0+t:6,m:0+t:80,m:1+t:2,m:1+t:23,m:0+t:81+s:2048",
            "fields": "f12,f13,f14,f1,f2,f4,f3,f152,f5,f6,f7,f15,f18,f16,f17,f10,f8,f9,f23",
            "fid": "f3",
            # "pn": "57",
            "pz": "100",
            "po": "1",
            "dect": "1",
            "ut": "fa5fd1943c7b386f172d6893dbfba10b",
            "wbp2u": "|0|0|0|web",
            # "_": str(int(time.time() * 1000)),  # 时间戳，time.time 乘以一千，取整
        }

    def connect_mongodb(self):
        client = MongoClient("localhost", 27017)
        db = client["stock"]
        self.dataDB = db["data"]

    def get_data(self, pn):
        """
        获取某一页的数据
        params : pn : 页数 int
        return :
            -data:list
            -False:bool
        """
        self.params["pn"] = str(pn)
        self.params["_"] = str(int(time.time() * 1000))
        response = requests.get(
            "https://push2.eastmoney.com/api/qt/clist/get",
            # cookies=self.cookies,
            params=self.params,
            headers=self.headers,
        )
        print(response)

        result = re.findall(r"\((.*)\)", response.text, re.S)[0]
        result = json.loads(result)["data"]
        if result is None:
            print("没有更多数据了")
            return False
        else:
            data = result["diff"]
            return data

    def request(self):
        pn = 1
        while 1:
            data = self.get_data(pn)
            pn += 1
            if not data:
                break
            # print(len(data))
            self.save(data)
            print(f"成功获取{pn*100}条数据")
            time.sleep(1)

    def save(self, data):
        # 在这里写链接mongodb，不合适，因为save写在了循环里，所以会被执行很多次
        # 只需要链接一次
        for item in data:
            result = {
                "名称": item["f14"],
                "代码": item["f12"],
                "最新价": item["f2"],
                "涨跌幅": item["f3"],
                "涨跌额": item["f4"],
                "最高": item["f15"],
                "最低": item["f16"],
                "今开": item["f17"],
                "昨收": item["f18"],
            }
            self.dataDB.insert_one(result)
        print(len(data))

    def run(self):
        self.connect_mongodb()
        self.request()


if __name__ == "__main__":
    stock = Stock()
    stock.run()
