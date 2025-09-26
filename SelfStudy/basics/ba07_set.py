# 和字典相同，使用中括号，元素之间用逗号分割
stt = {"1", "2", 3, 4, "aaa"}
# print(stt)  # 集合是无序的，打印出来的顺序随机,，没有下标，所以不可以切片,没有查询操作，修改

ds = {}  # 空的中括号，是字典类型
# print(type(ds))  # <class 'dict'>

# 定义一个空集合
# s = set()
# print(s, type(s))

# 唯一性，如果集合中有重复元素，会自动去重。可以实现高效率去重
stt = {"1", "2", 3, 4, "aaa", "1", "aaa"}
# print(stt)

# 集合中的元素/字典中的键名必须是可哈希的  哈希： hash ，把数据映射为唯一整数，像身份证号。用途 ： 快速查找、去重、校验、安全
# print(hash(123))
# print(hash("hello"))
# # print(hash([1, 2, 3]))   # unhashable type: 'list'
# # print(hash({[1, 2, 3]: 23}))  # unhashable type: 'list'
# # print(hash({"aa": 34}))  # unhashable type: 'dict'
# print(hash((1, 2, "hello", "ohou")))

### 集合常见操作  添加 删除
# 添加元素，如果集合中已经存在，则不进行任何操作，因为集合有自动去重的功能
stt.add("bbb")
stt.add("aaa")  # 不执行操作
# stt.add(["a", "b"])  # unhashable type: 'list' 列表不可作为集合中的元素
# print(stt)

# # .update(可迭代对象)  可迭代对象 ： iterable ， 因为要将可迭代对象进行拆分
# plus = [11, 22, 33, 44]
# stt.update(plus)
# stt.update("gadsho")  # 将这个拆分成了一个个字母
# stt.update([23, 42], (234, 231), "adsfgd")  # 可以添加多个
# print(stt)

### 删除元素
# .remove()
# stt.remove("aaa")
# stt.remove("aafs")  #  删除不存在的元素会报错
# print(stt)

# .discard() 如果删除的元素不存在，不会报错，不执行任何操作
stt.discard("fadso")
stt.discard("bbb")

# del stt("aaa")  # del 根据下标删除，remove根据值来删除
# print(stt)


### 集合的数学操作
# 交集
s1 = {1, 2, 3, 4, 5}
s2 = {2, 6, 8}
s3 = {2, 6, 4, 3}
# print(s1 & s2 & s3)  # and s1和s2两个集合 相交的部分
# print(s1.intersection(s2))  # 这个也是相交部分，不用符号的写法  # 如果没有，会返回空集合
# print(s1.intersection(s2).intersection(s3))  # s1和s2 的 交集也会返回一个集合

# 并集
# print(s1 | s2)  # or
# print(s1.union(s2))

# in / not in / len 公共操作
# print("aaa" in stt)
# print("ccc" not in stt)
# print(len(stt))

# 集合是可迭代对象
for i in stt:
    print(i)
