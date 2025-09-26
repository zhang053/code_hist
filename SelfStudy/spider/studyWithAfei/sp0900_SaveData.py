# 保存数据的几种方法

# 1，保存成文本文档 .txt
# 格式：标题：xxx ，时间：xxx ，作者：xxx
# 指路地址 sp0804_oopGetNews.py 的 def Output()

# 2，保存json文件
# 如果本身就是json文件的话。把名字命名为.json 直接存成json格式。 response.text  -->   saveFile.json
# 会被转换成Unicode编码

# 本身不是json的，需要进行处理，提取某些内容的，然后制作成json格式
"""
示范：
result = []
for i in range(len(self.news_title)):
    title = self.news_title[i]
    time = self.news_times[i]
    author = self.news_authors[i]
    result.append{"title":title,"time":time,"author":author}
# print(result)
import json

# 转换成json格式
with open("News.json","w",encoding="utf-8") as f:
    json.dump(result,f,ensure_ascii=False,indent=4)
    # indent = 4  自动缩进，但是会占用更多的空间，如果只是保存，不查看不需要加indent
    # ensure_ascii = False  -->  不让自动编码,不进行Unicode编码
"""

# # # 保存csv文件
# 使用逗号隔开
import sp0804_oopGetNews as d
import csv

g = d.GetNews()
g.run()
title = g.news_title
author = g.news_authors
intro = g.news_intros
time = g.news_times

# print(title, author, intro, time)

r = ""
for i in range(len(title)):
    tit = title[i]
    aut = author[i]
    intr = intro[i]
    tim = time[i]
    r += f"{tit},{aut},{intr},{tim}\n"

# 写入csv方法1，扩展名写.csv
# with open("News4.csv", "w", encoding="utf-8-sig") as f:
#     f.write(r)

"""
# #  方法2
# 首先import csv  自带
# with open("News5.csv", "w", encoding="utf-8-sig", newline="") as f:
#     # csv文件写入时自动会中间多出来空行，newline="" 空，可以取消自动空行
#     # 步骤1 设置csv文件的写入起
#     writer = csv.writer(f)
#     # 写入内容
#     writer.writerow([11123, 22, 223, 432]) # 第一行
#     writer.writerow([11, 22, 223, 432]) # 第二行
#     # 写入的内容要以列表的形式，row，横着写

# 实例：
with open("News5.csv", "w", encoding="utf-8-sig", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["title", "author", "time", "introduction"])
    for tit, aut, tim, introdution in zip(title, author, time, intro):
        writer.writerow([tit, aut, tim, introdution])
"""
