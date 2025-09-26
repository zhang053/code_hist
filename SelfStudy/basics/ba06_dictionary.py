# 认识字典
# info = {"name": "zhang", "age": 18, "length": 1.8}  # 键值对，冒号左边是键，右边是值，值可以重复，但是键不可以，必须是唯一
# print(info, type(info))

info = {
    "name": "zhang",
    "age": 18,
    "length": 1.8,
    "sex": "male",
    "tele": [12345678, 45355435],
}  # 如果键重复则后面的键所代表的值会重新赋值，类似于变量重新赋值
# print(info, type(info))


# ## ### 字典常见设置

# 查看元素  in/not in
# print("name" in info)
# print("zhang" in info)  # in 默认检查键名，不会查找值

# print(len(info))  #  统计键值对的数量，统计元素的数量，每个元素用逗号隔开

# dict[key]  通过键来寻找对应的值。不可以反过来，因为键不可以重复，值可以重复，如果通过值搜索，可能会返回多个key
# print(info["name"])  # 返回name对应的值
# print(info["tele"])

# print(info[0])  # 这里会把0 个判断成键。字典没有下标，不可进行切片操作
# []里如果输入没有的键名，会报错，导致代码无法运行

# .get(key,defalt) 根据键来获取对应的值，如果键不存在会返回none（优点：不会报错）, defaule
# ifmt = input("搜索你想要的情报")
# print(info.get(ifmt, "无"))  # 默认返回none，但是可以设置

# 如果一个键对应多个值，那些值可以用列表存储，然后可以通过下标获取对应的元素
# print(info["tele"][1])

# 字典的键名相当于下标
# info["name"] = "shuhao"  # 重新赋值
# print(info)

info["address"] = "Tokyo"  # 如果原来字典里没有，则会添加这个变量

del info["length"]  # 如果删除不存在的键时，会报错
# print(info)

# del info  # 该操作会删除整个字典
# print(info)

info["tele"].remove(info["tele"][0])  # 通过该方式对字典中的列表进行操作

# 清楚字典中所有键值对，将其变为空字典
# info.clear()
# info["name"] = "empty"
# print(info)

# # fmt: off
# print(info.pop("name"))  # 会先找到值，然后将键和值都删除，所以打印出来的会是这个键对应的值
# print(info)

# print(info.pop("weight", "no this information"))  # pop函数里默认是报错，但要是设置了返回值则会返回默认值
# fmt: on

# for i in info:  # 可以遍历，字典是可迭代对象
#     print(i)  # 默认遍历字典的键


# .keys 获取所有键 / .values 获取所有值 / .items 获取所有键值对
# print(info.keys())  # keys之类的括号里不需要变量，什么都不需要
# print(info.values())  # 虽然结果是[],但是不是列表，只支持遍历，不支持访问

# key，value，item 的值会随着字典的变化实时更改，即使没有重新赋值

# fmt: off
# print("male" in info.values())  # 检查字典中的值是否存在，但是找不到字典值中列表中的一个元素
# fmt: on

#### 解包
# for item in info.items():
#     print(item, type(item))  # <class 'tuple'> 以元组的形式去除键值对

# tup = ("hello", "nihao", 1, 2)
# print(tup)
# n1, n2, n3, n4 = ("hello", "nihao", 1, 2)
# print(n1, n2)
# # fmt: off
# n6, *n9 = ("hello", "nihao", 1, 2)    # 在最后一个变量上加 * ,可以让最后一个变量接收剩下的全部
# # fmt: on
# print(n6, n9)

# print(info.items())
# for k, v in info.items():  # 元组解包
#     print("key:", k)
#     print("value:", v)
#     print("")

# ##列表同样可以解包
# list = ["fa", "sfd", "fds", "sd"]
# a, *b = list
# print(a, b)
