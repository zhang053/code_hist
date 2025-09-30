# # # 数据去重
# # 界定去重的标准
# 年龄，姓名，什么的可以重复
# 通过身份证号，id，用户名（该用户名已存在）之类的来判断是否重复

# # 去重的时机
# 即将存储到数据库前
# 爬虫：数据获取的阶段(比如新闻的标题，时间等)

from pymongo import MongoClient

client = MongoClient("localhost", 27017)
SPIDER_DB = client["spider"]
studentDB = SPIDER_DB["student"]

# # 模拟数据
# studentDB.insert_many(
#     [
#         {"name": "张三", "age": 18, "id": 125422},
#         {"name": "李四", "age": 19, "id": 122342},
#         {"name": "王五", "age": 20, "id": 125233},
#         {"name": "赵六", "age": 21, "id": 143125},
#     ]
# )

# 录入信息
d = {"name": "zhang", "age": 18, "id": 153231}
if studentDB.find_one({"id": d["id"]}) == None:
    studentDB.insert_one(d)
    print("录入成功")
else:
    print("该学生已存在")
