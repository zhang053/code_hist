# # 通过代码操作数据库
# 1， 安装对应的包 pip install pymongo
from pymongo import MongoClient

client = MongoClient("localhost", 27017)

# 简单测试 --获取数据库列表
# print(client.list_database_names())

# 创建 数据库 (新创建的数据库要存储最少一条数据，才能显示出来)
SPIDER_DB = client["spider"]
# 在数据库里要先创建集合
userDB = SPIDER_DB["user"]

# # # 数据库的增删改查


# 增
# 存储数据
# userDB.insert_one({"name": "zhang", "age": 18})
# --再运行会再增加一条一样的，但是id不一样

# userDB.insert_many(
#     [{"name": "cho", "age": 20}, {"name": "zhang san", "age": 20, "sex": "male"}]
# )

# # # 查找

# # 找所有
# data = userDB.find()
# print(data)
# for item in data:
#     print(item)

# 按条件找
# data = userDB.find({"age": 20})
# for item in data:
#     print(item)
# # 找符合条件的第一个
data = userDB.find({"age": 20})
data = userDB.find_one({"age": 20})
print(data)
