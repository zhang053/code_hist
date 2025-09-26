# 起点虽然没法爬，但是可以爬取类似于笔趣阁的东西
# 1，确定要爬哪一本
# （https://www.69shuba.com/book/51592.htm）
# 2，获取章节列表（各个章节的url）
# 3，利用循环，向上述url发起请求，获取内容
# 4，将内容写入文件，保存


import requests
from bs4 import BeautifulSoup
import time

url = "https://www.69shuba.com/book/51592.htm"
cookies = {
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
    "jieqiHistory": "51592-35389639-%25u7B2C1073%25u7AE0%2520%25u5927%25u7ED3%25u5C40%25uFF08%25u4E0B%25uFF09-1757427233%7C58425-40302491-%25u7B2C491%25u7AE0%2520%25u75BE%25u901F%25u8FFD%25u8E2A-1757398771%7C43484-40592015-1259.%25u7B2C1254%25u7AE0%2520%25u7B49%25u4EE5%25u540E%25u6211%25u4EEC%25u518D%25u5BF9%25u6218%25u4E00%25u573A%25uFF01-1757344506%7C57909-39377756-%25u7B2C370%25u7AE0%2520%25u756A%25u5916%25uFF1A%25u5361%25u8299%25u5361-1755495112",
    "PHPSESSID": "rh2he8iusnk42t6jfjvb1i6fd5",
    "jieqiUserInfo": "jieqiUserId%3D1694798%2CjieqiUserUname%3Dshohiro5531%2CjieqiUserName%3Dshohiro5531%2CjieqiUserGroup%3D3%2CjieqiUserGroupName%3D%26%23x666E%3B%26%23x901A%3B%26%23x4F1A%3B%26%23x5458%3B%2CjieqiUserVip%3D0%2CjieqiUserHonorId%3D%2CjieqiUserHonor%3D%26%23x65B0%3B%26%23x624B%3B%26%23x4E0A%3B%26%23x8DEF%3B%2CjieqiUserToken%3Da2bec4ceb582b357fcc93e52332666f3%2CjieqiCodeLogin%3D0%2CjieqiCodePost%3D0%2CjieqiNewMessage%3D0%2CjieqiUserPassword%3Dc927d3e096e7385d2053e5f72d7b6ddf%2CjieqiUserLogin%3D1757428067",
    "jieqiVisitInfo": "jieqiUserLogin%3D1757428067%2CjieqiUserId%3D1694798",
    "cf_clearance": "YDo7GAYvIdChAmlB5dW1mS4SQ7Rci.b1_a93egjCwVw-1757428072-1.2.1.1-p6VPr4r0RbZ20n7rAyGolFo_y5HhOKz4QvMxg4oJormBfPO3u9a1wyrICtDwoCjjCvZWwcSre86zJUDbymPDKv7owj2ztw_a6nkNbrn39Xx.Qa1DxHaup_5Ptt9wCws4AJ7SAHmK_y21hHwg0suQLGLdfmptKyX.EN3AC0ULOMy8vFYKxPh1Yzwy3K38liWU9YprHegKycx._2PsAH5uGSSp_YbrhPciO_iLbFp6HIs",
    "shuba_userverfiy": "1757428072@4886b79744578c6f8f41f69b04875a2e",
    "jieqiVisitTime": "jieqiArticlesearchTime%3D1757428102",
    "shuba": "6831-4354-19118-1544",
    "_ga_04LTEL5PWY": "GS2.1.s1757427234$o53$g1$t1757428106$j37$l0$h0",
}
headers = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "accept-language": "ja,en;q=0.9,en-GB;q=0.8,en-US;q=0.7,zh-CN;q=0.6,zh;q=0.5",
    "cache-control": "no-cache",
    "pragma": "no-cache",
    "priority": "u=0, i",
    "referer": "https://www.69shuba.com/modules/article/search.php",
    "sec-ch-ua": '"Not;A=Brand";v="99", "Microsoft Edge";v="139", "Chromium";v="139"',
    "sec-ch-ua-arch": '"x86"',
    "sec-ch-ua-bitness": '"64"',
    "sec-ch-ua-full-version": '"139.0.3405.125"',
    "sec-ch-ua-full-version-list": '"Not;A=Brand";v="99.0.0.0", "Microsoft Edge";v="139.0.3405.125", "Chromium";v="139.0.7258.155"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-model": '""',
    "sec-ch-ua-platform": '"Windows"',
    "sec-ch-ua-platform-version": '"15.0.0"',
    "sec-fetch-dest": "document",
    "sec-fetch-mode": "navigate",
    "sec-fetch-site": "same-origin",
    "sec-fetch-user": "?1",
    "upgrade-insecure-requests": "1",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36 Edg/139.0.0.0",
    # 'cookie': 'zh_choose=s; _ga=GA1.1.513912616.1754138004; _ym_uid=175431646499432818; _lr_env_src_ats=false; _sharedID=64154fc2-22c5-4b2d-af0a-f55e359b9b8f; _sharedID_cst=zix7LPQsHA%3D%3D; sharedid=74fa1d2d-c84f-44b6-adaa-32a838fff58a; sharedid_cst=kaULaw%3D%3D; cto_bundle=fOxyo19RZkh0Z1glMkZ2SndwZzdrV1BiZEUxSzglMkZCWWVoMnl0SnAwZ3pwdjROTG5oQnBqbW9La0tLZTluOTBYdUs4RWVyME0zZGpyZllpTmo2N3hwWTBDOWdKJTJCalJ1cVZxaWhvQW1jMkIyeEZhTWVMbHZQZ3VRMW1XOGlKRUZLQUNjN0xKYkc2MDdnYXd1ZE1CUkNjQzQ1SXBENHclM0QlM0Q; cto_bidid=8mYetV9DRSUyRkFOdENSQiUyQk1jRENReXB1SlpyWmNsVWtrNEVSRGhJdGdYMnRFUzNJV0lySkNTMkxMVmtZbTRVQUxBMXlhTEowbG15dlFldCUyQmJEWFhQMyUyRnFySHdiN2Z5ZmZtNVBKNCUyRnF3WWwxd2VYMWslM0Q; cto_dna_bundle=bHuT1F9Tdzc2bnlwUFpCZjNLb21uM092VzVjd2x6QlRrMFJsRkNCaDFORVlEZHc5WjdOZThzanN2RTZ6SkVORDh6TGd0R1g0c1N2WEFzb01xQTk4c3FLJTJGQkt3JTNEJTNE; pbjs-id5id=%7B%22signature%22%3A%22ID5_As27vNz947cXo-oC2WQOBmktq54ViVUG2kIB-ykPaMOoDa9hQ3IG5ct1wPeZExS9tErk61sbJnn49mrRzroqKr5HEMP0YwHfAcoON0qut2N2V0bSvqjkO3r5ENedVPkFb1aUGFW0hDCrXKkq83FTjs_WjABnOrobkCEFMpdo4KvbFInYGj8%22%2C%22created_at%22%3A%222025-08-08T04%3A28%3A01Z%22%2C%22id5_consent%22%3Atrue%2C%22original_uid%22%3A%22ID5*IUqn7Xu9obCQbCK4UlDUd-xP4d-NL3dH4SLxeEFLq3067b01x9cRaXpNyOFPNcig%22%2C%22universal_uid%22%3A%22ID5*AOM2GtW1C5RjpatBVhKlFY6oqmcHCx3M581qwxYyoJo67UflKdSw6LCCBUjS3RWe%22%2C%22link_type%22%3A1%2C%22cascade_needed%22%3Atrue%2C%22privacy%22%3A%7B%22jurisdiction%22%3A%22other%22%2C%22id5_consent%22%3Atrue%7D%2C%22ext%22%3A%7B%22linkType%22%3A1%2C%22pba%22%3A%22zdid%2FBooWl%2FM%2B0XzZX5iwijps2mKM1WffAZ2QQKO8vNIOqmlV8o1ndQNo7XZ%2B6kn%22%7D%2C%22cache_control%22%3A%7B%22max_age_sec%22%3A7200%7D%2C%22ids%22%3A%7B%22id5id%22%3A%7B%22eid%22%3A%7B%22source%22%3A%22id5-sync.com%22%2C%22uids%22%3A%5B%7B%22id%22%3A%22ID5*AOM2GtW1C5RjpatBVhKlFY6oqmcHCx3M581qwxYyoJo67UflKdSw6LCCBUjS3RWe%22%2C%22atype%22%3A1%2C%22ext%22%3A%7B%22linkType%22%3A1%2C%22pba%22%3A%22zdid%2FBooWl%2FM%2B0XzZX5iwijps2mKM1WffAZ2QQKO8vNIOqmlV8o1ndQNo7XZ%2B6kn%22%7D%7D%5D%7D%7D%7D%7D; pbjs-id5id_cst=kaULaw%3D%3D; pbjs-id5id_last=Fri%2C%2008%20Aug%202025%2007%3A45%3A27%20GMT; _ym_uid_cst=znv0HA%3D%3D; jieqiHistory=51592-35389639-%25u7B2C1073%25u7AE0%2520%25u5927%25u7ED3%25u5C40%25uFF08%25u4E0B%25uFF09-1757427233%7C58425-40302491-%25u7B2C491%25u7AE0%2520%25u75BE%25u901F%25u8FFD%25u8E2A-1757398771%7C43484-40592015-1259.%25u7B2C1254%25u7AE0%2520%25u7B49%25u4EE5%25u540E%25u6211%25u4EEC%25u518D%25u5BF9%25u6218%25u4E00%25u573A%25uFF01-1757344506%7C57909-39377756-%25u7B2C370%25u7AE0%2520%25u756A%25u5916%25uFF1A%25u5361%25u8299%25u5361-1755495112; PHPSESSID=rh2he8iusnk42t6jfjvb1i6fd5; jieqiUserInfo=jieqiUserId%3D1694798%2CjieqiUserUname%3Dshohiro5531%2CjieqiUserName%3Dshohiro5531%2CjieqiUserGroup%3D3%2CjieqiUserGroupName%3D%26%23x666E%3B%26%23x901A%3B%26%23x4F1A%3B%26%23x5458%3B%2CjieqiUserVip%3D0%2CjieqiUserHonorId%3D%2CjieqiUserHonor%3D%26%23x65B0%3B%26%23x624B%3B%26%23x4E0A%3B%26%23x8DEF%3B%2CjieqiUserToken%3Da2bec4ceb582b357fcc93e52332666f3%2CjieqiCodeLogin%3D0%2CjieqiCodePost%3D0%2CjieqiNewMessage%3D0%2CjieqiUserPassword%3Dc927d3e096e7385d2053e5f72d7b6ddf%2CjieqiUserLogin%3D1757428067; jieqiVisitInfo=jieqiUserLogin%3D1757428067%2CjieqiUserId%3D1694798; cf_clearance=YDo7GAYvIdChAmlB5dW1mS4SQ7Rci.b1_a93egjCwVw-1757428072-1.2.1.1-p6VPr4r0RbZ20n7rAyGolFo_y5HhOKz4QvMxg4oJormBfPO3u9a1wyrICtDwoCjjCvZWwcSre86zJUDbymPDKv7owj2ztw_a6nkNbrn39Xx.Qa1DxHaup_5Ptt9wCws4AJ7SAHmK_y21hHwg0suQLGLdfmptKyX.EN3AC0ULOMy8vFYKxPh1Yzwy3K38liWU9YprHegKycx._2PsAH5uGSSp_YbrhPciO_iLbFp6HIs; shuba_userverfiy=1757428072@4886b79744578c6f8f41f69b04875a2e; jieqiVisitTime=jieqiArticlesearchTime%3D1757428102; shuba=6831-4354-19118-1544; _ga_04LTEL5PWY=GS2.1.s1757427234$o53$g1$t1757428106$j37$l0$h0',
}

response = requests.get(url, cookies=cookies, headers=headers)

print(response)

# with open("0501_69shuba.html", "w", encoding="utf-8") as f:
#     f.write(resp.text)

# 解析返回的html文本
soup = BeautifulSoup(response.text, "lxml")

novel_title = soup.select("h1 > a")[0].text

import os

os.makedirs(novel_title, exist_ok=True)
# 完成创建文件夹

index_urls = soup.select(".mybox > a")
# print(index_urls[0]["href"])
# 成功获得完整目录的链接

response2 = requests.get(url=index_urls[0]["href"], headers=headers, cookies=cookies)
soup2 = BeautifulSoup(response2.text, "lxml")

# # # 查找数据  --> 返回的值是列表

# # 方法1
# div = soup.find("div", id="catalog")
# li = div.find_all("li")


# # 方法2
# css选择器 。 快捷方法，在想要寻找的标签右键，复制，复制selector （copy selector）

ele_titles = soup2.select("#catalog > ul > li >a")
# >后面是下一级，必须要一层一层的写
print(response2)
for ele in ele_titles:
    # examp = ele_titles[0]
    response3 = requests.get(url=ele["href"], headers=headers, cookies=cookies)

    soup3 = BeautifulSoup(response3.text, "lxml")
    # 以获取每一张的内容，接下来找标题和内容
    title = soup3.select("h1")[0].text
    content = soup3.select(".txtnav")[0].get_text("\n", strip=True)
    file_name = f"{novel_title}/{title}.txt"
    with open(file_name, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"完成爬取{title}")
    time.sleep(2)
