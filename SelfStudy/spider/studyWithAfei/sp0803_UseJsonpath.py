import requests
from pprint import pprint
from jsonpath import jsonpath

cookies = {
    "BAIDUID": "48E3DE22FA1321E55C136CBB9CB85853:FG=1",
    "newlogin": "1",
    "PSTM": "1756477320",
    "BIDUPSID": "69E5D72C5201B08F2D08B986BC3D835D",
    "BDUSS": "ldISmtOdDlMOVIzflowdEZIMDZ6TWVoekJjdndDclF4Y1dTM2E5bjBrd3FzZWRvRVFBQUFBJCQAAAAAAQAAAAEAAAA0YFSTAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACokwGgqJMBob",
    "BDUSS_BFESS": "ldISmtOdDlMOVIzflowdEZIMDZ6TWVoekJjdndDclF4Y1dTM2E5bjBrd3FzZWRvRVFBQUFBJCQAAAAAAQAAAAEAAAA0YFSTAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACokwGgqJMBob",
    "BAIDUID_BFESS": "48E3DE22FA1321E55C136CBB9CB85853:FG=1",
    "ZFY": "XWFlRw1wcYlt:A775Ad5aCT:AGWI:BuWG:BzKb4aehmWLm4:C",
    "PSINO": "7",
    "delPer": "0",
    "H_WISE_SIDS": "64660_64748_64815_64834_64911_64923_64980_65116_65141_65140_65137_65188_65204_65219_65250_65256_65143_65274_65281_65373_65384",
    "BDRCVFR[feWj1Vr5u3D]": "mbxnW11j9Dfmh7GuZR8mvqV",
    "H_PS_PSSID": "63142_63327_64660_64748_64701_64815_64834_64911_64923_64980_65116_65141_65140_65137_65188_65204_65219_65250_65256_65143_65274_65281_65321_65346_65373_65384",
}

headers = {
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
    # 'Cookie': 'BAIDUID=48E3DE22FA1321E55C136CBB9CB85853:FG=1; newlogin=1; PSTM=1756477320; BIDUPSID=69E5D72C5201B08F2D08B986BC3D835D; BDUSS=ldISmtOdDlMOVIzflowdEZIMDZ6TWVoekJjdndDclF4Y1dTM2E5bjBrd3FzZWRvRVFBQUFBJCQAAAAAAQAAAAEAAAA0YFSTAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACokwGgqJMBob; BDUSS_BFESS=ldISmtOdDlMOVIzflowdEZIMDZ6TWVoekJjdndDclF4Y1dTM2E5bjBrd3FzZWRvRVFBQUFBJCQAAAAAAQAAAAEAAAA0YFSTAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACokwGgqJMBob; BAIDUID_BFESS=48E3DE22FA1321E55C136CBB9CB85853:FG=1; ZFY=XWFlRw1wcYlt:A775Ad5aCT:AGWI:BuWG:BzKb4aehmWLm4:C; PSINO=7; delPer=0; H_WISE_SIDS=64660_64748_64815_64834_64911_64923_64980_65116_65141_65140_65137_65188_65204_65219_65250_65256_65143_65274_65281_65373_65384; BDRCVFR[feWj1Vr5u3D]=mbxnW11j9Dfmh7GuZR8mvqV; H_PS_PSSID=63142_63327_64660_64748_64701_64815_64834_64911_64923_64980_65116_65141_65140_65137_65188_65204_65219_65250_65256_65143_65274_65281_65321_65346_65373_65384',
}

params = {
    "tn": "resultjson_com",
    "word": "昔涟",
    "ie": "utf-8",
    "fp": "result",
    "fr": "",
    "ala": "0",
    "applid": "10992671519962248405",
    "pn": "70",
    "rn": "60",
    "nojc": "0",
    "gsm": "3c",
    "newReq": "1",
}

response = requests.get(
    "https://image.baidu.com/search/acjson",
    params=params,
    cookies=cookies,
    headers=headers,
)

print(response)

data = response.json()
# pprint(data)

print(jsonpath(data, "$..images..thumburl"))
