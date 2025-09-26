# 可变类型和不可变类型

# li = [1, 2, 3]
# print(id(li))
# li.append(4)
# print(id(li))  # id没有变，说明li是可变类型
# # 内容变化，内存地址不变 --> 可变类型

# dic = {"a": 1, "b": 2}
# print(id(dic))
# dic["b"] = 3
# print(id(dic))  # 内容变化，内存地址不变 --> 可变类型

# 可变类型通常是可哈希(hashable)的

# n = 1
# print(n, id(n))
# n += 1
# print(n, id(n))  # 内容变化，内存地址同样发生变化 --> 不可变类型

s = "hello"
print(s, id(s))
s = s.replace("o", "1")
print(s, id(s))  # 内容变化，内存地址同样发生变化 --> 不可变类型

tuple = (1, 2, 3)
print(tuple, id(tuple))
tuple = tuple + (4,)
print(tuple, id(tuple))  # 元组没有添加操作，只能重新赋值， --> 不可变类型

# 重新赋值会重新开辟新的空间，所以内存地址会发生变化

# 不可变类型的深浅拷贝没有意义，因为内容不会变化
