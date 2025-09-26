# list 列表
programing_name = [
    "python",
    "c",
    "c#",
    "c++",
    1,
    2,
    [1, 2, "HELLO"],
]  # 列表里的值没有限制，可以是数值，文字列表，truefalse
# print(programing_name[6], type(programing_name))
# print(programing_name[-2])  # -2:列表中倒数第二个元素
# print(programing_name[-1:-4:-1])  # 切片操作也管用

# for pn in programing_name[:2]:
#     print(f"{pn},hello")

## 列表常见操作
# .append() 在列表最后面添加，括号里可以是任何类型
# programing_name.append("js")
# programing_name.append(123)
# programing_name.append(["a", "b"])
# print(f"{programing_name}")

## .extend() 会把括号里的元素逐个拆分成一个一个的元素，然后依次添加到列表末尾
# programing_name.extend([1, 2, 3])  # 把这个列表拆分成一个一个元素，逐一添加
# programing_name.extend("hello")  # 把这个列表拆分成一个一个字母，逐一添加

# ## .insert() 把元素插入到指定的位置(index)
# programing_name.insert(0, "hello")
# programing_name.insert(2, "hello")  # 插入到下标2，列表中第三个的位置
# programing_name.insert(
#     1000, "ohou"
# )  # 如果指定的位置超过列表的范围，会添加到最末尾，但是推荐使用append

# ## 修改元素，list[inden] = xxx, 指定下标位置，代入新的值
# programing_name[0] = "nihao"  # 如果超过范围会报错
# # print(programing_name)

# ## in 检查一个元素是否存在于列表中，如果存在返回 true ，不存在时 false
# print("python" in programing_name)  # in 前面加个not 判断不在，如果在则为false，不在就说明这句话是对的则返回true
# print("js" not in programing_name)
# # 与字符串的in 不同， 列表的in判断的是一个元素的整体，不是一部分
# print("py" in programing_name)

# ## 创建昵称是判断昵称是否重复
# names = ["1", "12", "123"]
# while 1:
#     new_name = input("create a name: ")
#     if new_name in names:
#         print("该昵称已被使用")
#     else:
#         print("账号创建成功")
#         names.append(new_name)
#         print(names)
#         break
# # 局限：该代码无法永久化保存，因为没有保存到数据库或文件里

# index(value,start,stop)  查找列表中某一个元素第一次出现的值，如果不存在则会报错
# search = input("I want to find: ")
# print(
#     f"想要寻找的元素在第{programing_name.index(search) + 1}个"
# )  # 下标加1，去除从0开始的影响

# list.count(value) 统计括号里的元素在列表里出现过几次，如果没出现过返回0
programing_name.append("c#")
programing_name.append("c#")
# print(f'该元素出现过 {programing_name.count("c#")} 次')
# print(f'该元素出现过 {programing_name.count("js")} 次')

## 删除元素
# del 这个是公共操作，不光在列表可以用
# print(programing_name)
# del programing_name[0]
# del programing_name[0::2]
# print(programing_name)

# remove 根据元素的值进行删除，指定元素删除
# print(programing_name)
# programing_name.remove("c#")  # 会删除找到的第一个指定元素
# print(programing_name)
# programing_name.append("0")

# for i in programing_name:
#     if i == "c#":
#         programing_name.remove(i)
# print(programing_name)
## 无法通过该方式删除所有重复的指定删除元素，因为for循环的次数不会影响，但是删除其中元素会影响下标数字，倒是for循环操作的列表每次都不一样
# 可以通过从后往前删除，这样删除后面的元素，前面的元素的下标不会影响
# fmt: off
# for i in range(len(programing_name) - 1, -1, -1):  # len() 获取括号内列表的长度，列表如果哟5个元素，则返回5，但是下标长度到4，所以需要减1
#     print(programing_name)
#     if programing_name[i] == "c#":
#         programing_name.remove(programing_name[i])
# print(programing_name)


### 可迭代对象 = 可以用for循环遍历的

# fmt: on

# 排序
# li = [23, 12, 4, 5, 24, 432, 3]
# # li.sort()  # 默认为 reverse = false，从小到大排序
# # li.sort(reverse=True)
# print(li)

# li.reverse()  # 把原来的列表变成从后往前 相当于 li[::-1]
# print(li)

# # 列表推导式
# 笨方法 生成1到10
li = []
# for i in range(1, 11):
#     li.append(i)
# print(li)

## 推导式  [表达式(expression) for 变量 in 可迭代对象]  表达式：列表中的元素
# x = 1 * 2
# print([x for i in range(1, 11, 1)])

# 列表中的元素乘以6
lst = [i for i in range(1, 11, 2)]
lst2 = []
# print(lst)
# for i in lst:
#     lst2.append(i * 6)
#     print(lst2)

# 简化：推导式
# fmt:off
print([i * 6 for i in lst])  # 这个和上面的for的笨方法一一对应，最开始的表达式对应的是想要添加的变量
# fmt:on

# 推导式后面还可以添加条件  [表达式(expression) for 变量 in 可迭代对象 if  ]
print(
    [i * 6 for i in lst if i * 6 <= 30]  # 这个if判断是选取的变量，不是列表的元素
)  # 这个和上面的for的笨方法一一对应，最开始的表达式对应的是想要添加的变量

# 列表嵌套
list1 = [[[[1, 23, 4]], 1], 23]
print(list1[0][0][0][1])
