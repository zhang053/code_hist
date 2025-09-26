# 内存地址相同， -> 是同一个文件 （对象） ->   操作共享
# 内存地址不同， -> 是两个文件  ->   操作不共享

# 当前文件的地址 （パスのコピー, copy path）
# D:\py\py_practice\SelfStudy\basics\09_Copy.py
# D:\py\py_practice\SelfStudy\basics\09_Copy.py  <--这个是在vsCode里打开的，地址相同，所以操作可以共享

# ### 赋值
# li = [1, 2, 3, 4, 5]
# li2 = li
# print("li:", li)
# print("li2:", li2)
# # id()() 用来查看内存地址

# li2.append(6)  # 修改li2，li也会被修改 ,因为li和li2指向同一个内存地址
# print("li:", li)
# print("li2:", li2)
# # print("id(li):", id(li))
# # print("id(li2):", id(li2))  # 两个的内存地址相同
# # print(li == li2)  # 返回True

# 通常不会改写原来的值，而是创建一个新的变量，使用copy()方法
# 需要导入模块 import copy

import copy

# # 深拷贝deepcopy，浅拷贝copy
# # 浅拷贝copy，只拷贝一层，深层次的对象不拷贝，嵌套层共享，最外层不共享
# li = [1, 2, 3, 4, 5, [1, 23, 4]]
# li2 = copy.copy(li)  # copy模块里的copy函数

# li2.append(6)
# # print("li:", li)  # 修改l2，li不会改变
# # print("l2:", l2)
# # print(id(li) == id(l2))  # 两个的内存地址不同

# li2[5].append(6)
# print("li:", li)  # 外层未发生变化，内层发生变化
# print("l2:", li2)  # 外层未发生变化，内层发生变化
# print(id(li[5]) == id(li2[5]))
# print(id(li) == id(li2))

# # 深拷贝deepcopy，拷贝所有层，深层次的对象也拷贝
li1 = [1, 2, [3, 4]]
li2 = copy.deepcopy(li1)
print("li1:", li1)
print("li2:", li2)

li2[2].append(5)
print("li1:", li1)
print("li2:", li2)  # 操作没有共享
print(id(li1[2]) == id(li2[2]))  # 内存地址不同

# 深拷贝更占用空间，所以平时浅拷贝更常用，并且一般不会列表嵌套列表
