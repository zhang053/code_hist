import requests
from bs4 import BeautifulSoup
import time

# 目标url https://www.biquge365.net/book/652411/

url = "https://www.biquge365.net/newbook/652411/"

headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36 Edg/139.0.0.0"
}

response = requests.get(url, headers=headers)
# print(response)

# 解析
sp = BeautifulSoup(response.text, "lxml")

eles = sp.select(".info > li > a")
print(eles)

# ele_links = []
# for el in eles:
#     title = el.text
#     # /chapter/652411/94489267.html
#     # 这个链接是被省略的，因为在当前页面点击的相对链接，会被自动补全协议和域名
#     href = "https://www.biquge365.net" + el["href"]
#     ele_links.append(href)

ele_links = ["https://www.biquge365.net" + el["href"] for el in eles]
# 循环向links发起请求

# 创建文件夹
import os

novel_title = sp.select("h1")[0].text
os.makedirs(novel_title, exist_ok=True)

for href in ele_links:
    response = requests.get(url=href, headers=headers)
    # response = requests.get(url=ele_links[0], headers=headers)
    # print(response)
    # print(response.text)

    # 获取章节的名字
    # #neirong > h1
    sp1 = BeautifulSoup(response.text, "lxml")
    # 因为是新的请求，所以需要去构建一个新的soup解析器
    title = sp1.select("#neirong > h1")[0].text
    # 因为是列表形式，输出会带方括号，所以用[0]来取出这个字符串

    # 获取章节的内容
    # content = sp1.select("#txt")[0].text  # 这样获取的文本没有换行
    content = sp1.select("#txt")[0].get_text("\n", strip=True)
    # print(content)

    # 已经获取小说内容了，接下来是把他们存储起来
    # 创建文件夹，小说名字在第一次获取的时候获取

    file_name = f"{novel_title}/{title}.txt"
    with open(file_name, "w", encoding="utf-8") as f:
        f.write(content)
    print(title + "保存完成")
    time.sleep(2)  # 暂停两秒钟
    # 因为频率太快的话，会被判定爬虫，2:等两秒再爬
