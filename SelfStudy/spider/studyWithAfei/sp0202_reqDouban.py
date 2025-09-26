import requests
import re

url = "https://movie.douban.com/top250"

headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36 Edg/139.0.0.0"
}
# fmt:off
req = requests.get(url, headers = headers)  # 如果直接打印这个的话，显示 418 ，服务器拒绝，因为携带信息太少，判定为爬虫，被拒绝
# fmt: on

with open("douban.html", "w", encoding="utf-8") as f:
    f.write(req.text)  # 通过text获取的文件一定是string类型的文字

# <span class="title">星际穿越</span>  # 前面的固定，后面的固定，中间的电影名不是固定的
# <span class="title">(.+)</span>     #

### 正则表达式  re

html = req.text
pattern = re.compile(r'<span class="title">(?!&nbsp)(.+?)</span>')

titles = pattern.findall(html)
# print(titles)  # 会出现 &nbsp ，这个通常在前端表示空格的意思

# for ti in titles:
#     if not ti.startswith("&"):
#         print(ti)

# print(titles)
# print(len(titles))

#  获取导演名字
# 规律： 导演: 克里斯托弗·诺兰 Christopher Nolan  主演: 莱昂纳多·迪卡普里奥  （导演名字和前后有空格）
director_pattern = re.compile(r"导演: (.+?) ")
directors = director_pattern.findall(html)

# print(directors)
# print(len(directors))

# 获得评分数据
# 规律： <span class="rating_num" property="v:average">9.5</span>
rating_pattern = re.compile(
    r'<span class="rating_num" property="v:average">(.+?)</span>'
)
ratings = rating_pattern.findall(html)

# print(ratings)
# print(len(ratings))

# 总结整理
# result = []
# for i in range(len(titles)):
#     result.append([titles[i], directors[i], ratings[i]])
# print(result)

# dic_result = list()
# for i in range(len(titles)):
#     dic_result[i] = {}
#     dic_result[titles[i]] = [directors[i], ratings[i]]

# print(dic_result)

# from pprint import pprint
