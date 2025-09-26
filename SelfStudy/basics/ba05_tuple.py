# ## tuple 元祖  定义不允许被修改的数据集合
# 语法格式：变量名 = （元素，元素，元素，元素，元素）

tup = ("nihao", "hello", "zaijian", "byebye", 1, 2, [12, 35], (31, 32, 2))
tup_ex = "ohou"  # 如果只有一个数据，必须要在末尾加逗号，否则会变成string类型
# print(tup_ex, type(tup_ex))
tup_ex = ("ohou",)
# print(tup_ex, type(tup_ex))

# 元祖同样支持切片（截取）
# print(tup)
# print(tup[1])
# print(tup[0::2])
print(tup[len(tup) - 1 :: -1])
# print(tup[::-1])

# for name in tup[len(tup) - 1 :: -1]:
#     print(f"tup = {name}")

# 元组不支持删除，添加
# 只支持.index  .count 还有 in
# print(tup.index(1))
# print(2 in tup)
# 但是可以重新赋值
# tup += tup_ex
# print(tup)
