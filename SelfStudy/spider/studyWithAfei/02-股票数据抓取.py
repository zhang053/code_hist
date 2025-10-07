import time
import json
import re
import requests
from pymongo import MongoClient


class Stock:
    def __init__(self):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36"
        }
        self.params = {
            "np": "1",
            "fltt": "1",
            "invt": "2",
            "cb": "jQuery37105874559435026122_1758542812428",
            "fs": "m:0+t:6,m:0+t:80,m:1+t:2,m:1+t:23,m:0+t:81+s:2048",
            "fields": "f12,f13,f14,f1,f2,f4,f3,f152,f5,f6,f7,f15,f18,f16,f17,f10,f8,f9,f23",
            "fid": "f3",
            "pn": "1",
            "pz": "100",
            "po": "1",
            "dect": "1",
            "ut": "fa5fd1943c7b386f172d6893dbfba10b",
            "wbp2u": "|0|0|0|web",
            "_": str(int(time.time() * 1000)),
        }
        self.dataDB = None

    def connect_mongodb(self):
        client = MongoClient("localhost", 27017)
        db = client["stock"]
        self.dataDB = db["data"]

    def start_request(self):
        pn = 1
        while True:
            data = self.get_data(pn)
            pn += 1
            if not data:
                break
            self.save(data)

    def get_data(self, pn):
        """
        获取某一页的数据
        :param: pn:int
        :return:
            - data:list
            - False:bool
        """
        self.params["pn"] = str(pn)
        self.params["_"] = str(int(time.time() * 1000))
        r = requests.get(
            "https://push2.eastmoney.com/api/qt/clist/get",
            params=self.params,
            headers=self.headers,
        )
        result = re.findall(r"\((.*)\)", r.text)[0]
        result = json.loads(result)["data"]
        if result is None:
            print("没有更多数据啦")
            return False
        else:
            data = result["diff"]
            return data

    def save(self, data):
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

    def run(self):
        self.connect_mongodb()  # 连接数据库
        self.start_request()


if __name__ == "__main__":
    stock = Stock()
    stock.run()

# headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36'}
# params = {
#     'np': '1',
#     'fltt': '1',
#     'invt': '2',
#     'cb': 'jQuery37105874559435026122_1758542812428',
#     'fs': 'm:0+t:6,m:0+t:80,m:1+t:2,m:1+t:23,m:0+t:81+s:2048',
#     'fields': 'f12,f13,f14,f1,f2,f4,f3,f152,f5,f6,f7,f15,f18,f16,f17,f10,f8,f9,f23',
#     'fid': 'f3',
#     'pn': '1',
#     'pz': '100',
#     'po': '1',
#     'dect': '1',
#     'ut': 'fa5fd1943c7b386f172d6893dbfba10b',
#     'wbp2u': '|0|0|0|web',
#     '_': str(int(time.time()*1000)),
# }
#
# def get_data(pn):
#     params['pn'] = str(pn)
#     response = requests.get('https://push2.eastmoney.com/api/qt/clist/get', params=params, headers=headers)
#     # 两种方式来处理jsonp内容
#     # 1. 最常见最好用的 -- 使用正则
#     result = re.findall(r'\((.*)\)', response.text)[0]
#     result = json.loads(result)['data']
#     if result is None:
#         print("没有更多数据啦")
#         return False
#     else:
#         data = result['diff']
#         return data
#
# def save(data):
#
#
# pn = 1
# while True:
#     data = get_data(pn)
#     pn += 1
#     if not data:
#         break
#     save(data)
