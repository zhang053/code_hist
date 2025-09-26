# 用于提取HTML数据的方案：bs4
# 1，安装 pip install beautifulsoup4

from bs4 import BeautifulSoup
import re

# 解析HTML文件 / 解析HTML文本
soup = BeautifulSoup(open("0202-1_douban.html", encoding="utf-8"), "lxml")
# python 有默认的解析器 html.parser
# 通常会使用 lxml，因为解析效果更好（需要安装lxml包)

# 获取标签内容
# print(soup.title.string)
# print(soup.h1)  # 当有多个时，只返回第一个，通常只用在标签为title或h1时
# 或者能百分百确定，这个html文件，只有这一个标签时

# 获取多个匹配结果
# print(soup.find_all("a"))  # 返回一个列表，列表中每个元素是标签对象,没找到返回空列表

# 添加条件 通过标签属性来筛选
# print(soup.find_all(name="div", id="doubanapp-tip"))
# 通过class筛选
# fmt: off
# print(soup.find_all("p", class_="qrcode"))  # class是python的保留字，所以用class_来表示class
# 只要标签中包含class属性，都会被筛选出来
# fmt: on
# print(soup.find_all("a", href="https://www.douban.com"))

# # 通过正则表达式进行筛选
# print(soup.find_all("a", href=re.compile(r"^http")))
# ^表示以什么开头，$表示以什么结尾

# 通过css选择器进行筛选
# print(soup.select("#top-nav-appintro"))  # 井号# 表示id=，点号是 . 表示class=
# # fmt: off
# print(soup.select(".qrcode a.link"))  # 可以用空格表示层级关系 class="qrcode" 下的 a 标签
# # fmt: on

# d = soup.find("div", class_="more-items")
# print(d.string)  # None 因为div标签中，很多内容隔开了，所以获取不到
# print(d.get_text("\n", strip=True))  # 获取标签中的所有文本内容
# strip=True 表示去掉首尾的空格, 前面的""表示用双引号之内的字符来隔开

# 获取标签属性
a = soup.find("a")  # 只返回第一个匹配的标签
print(a["href"])
