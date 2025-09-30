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
# 在名为spider的数据库中创建user的集合

# # # 数据库的增删改查


# 增
# 存储数据
# userDB.insert_one({"name": "zhang", "age": 18})
# # --再运行会再增加一条一样的，但是id不一样

# userDB.insert_many(
#     [{"name": "cho", "age": 20}, {"name": "zhang san", "age": 20, "sex": "male"}]
# )
# # 数据库中的数据以列表形式存在


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
# # # 找符合条件的第一个
# data = userDB.find({"age": 20})
# data = userDB.find_one({"age": 20})
# print(data)

# 针对数字字段的写法
# data = userDB.find({"age": {"$gt": 18}})  # gt：大于，固定写法
# data = userDB.find({"age": {"$lt": 20}})  # lt：小于
# for item in data:
#     print(item)


# # # 改
# # .updata(要选谁，要怎么改)
# userDB.update_one({"name": "zhang"}, {"$set": {"age": 30}})
userDB.update_many({"name": "cho"}, {"$set": {"age": 30}})
# userDB.update_many({"age": {"$lt": 25}}, {"$set": {"age": 10}})
# # 只能通过 $ 命令
# for item in userDB.find({"name": "zhang"}):
#     print(item)


# # # 删除
# .delete_one
# userDB.delete_one({"name": "zhang"})
# userDB.delete_many({"name": "zhang"})
# userDB.delete_many({"age": {"$gt": 20}})

# # 删除集合
# userDB02 = SPIDER_DB["user02"]
# # 因为新创建的数据库要存储最少一条数据，才能显示出来
# userDB.drop()
# userDB02.insert_one({"na ma e": "shuhao"})

# # 删数据库
# client.drop_database("spider")

# 删除数据的某个字段
userDB.update_one({"name": "zhang san"}, {"$unset": {"sex": ""}})
# unset 是删除的意思
