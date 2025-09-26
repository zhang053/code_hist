# 列表 用来存储一系列的元素
# 元组 用来保存不可变的数据
# 字典 用来存储一系列的键值对
# 集合 用来存储一系列的元素，用来去重

# 数据类型：字符串、数字、列表、元组、字典、集合

#     int（） 将值转换为整数数据，如果有字母字符会报错
# print(int(-1.999))  # 转换时去掉小数点，不是四舍五入
# print(int(True))  # True 转换为1，False 转换为0
# print("123")  # 字符串转换为整数
# num = int(input("请输入："))  # input() 输入的值都是字符串类型
# print(num, type(num))  # 如果包含数字字符以外的字符，会报错

# print(int("1.23"))  # 如果字符串包含小数点，会报错
# print(int(float("1.99")))  # 先将字符串转换为浮点数，再转换为整数


#      float（） 将值转换为浮点数
# print(float(1))  # 将整数转换为浮点数,整数x 后面加小数点 x.0
# print(float("1.23"))  # 将字符串转换为浮点数
# print(float(True))  # True 转换为1.0，False 转换为0.0
# print(float("abs"))  # 如果字符串包含字母字符，会报错

# fmt: off
# print(float([1, 2, 3]))  #TypeError: float() argument must be a string or a real number, not 'list'
# fmt: on
# 列表，元组，字典，集合等复合的数据结构，不能直接转换为浮点数


#      bool（） 将值转换为布尔值
# 0和空返回false，其他的都返回true
# print(bool(0))  # False
# print(bool(-19.03))  # True
# print(bool(""))  # 空，False
# print(bool([1, 2, 3]))  # 非空，True
# 任何数据类型中的零（0，0.0，0.0j，""，[]，()，{}，set()）在布尔上下文中都为False，其余都为True
# 其中0j是虚数0，虚数是数学中的概念，虚数是表示形如a+bi的复数，其中a和b都是实数，i是虚数单位，满足i^2 = -1


#      str（） 将值转换为字符串
data = 123
data = True  # True 转换为字符串 "True"
data = (1, 2, 3)  # 元组转换为字符串 "(1, 2, 3)"
data = str(data)
# print(data, type(data))


###       eval（） 将字符串转换为表达式
# print("1" + "1")  # 字符串拼接
# print(eval("1 + 1"))  # 表达式计算,相当于eval把引号给去掉了
# eval("print(1+1)")  # eval执行字符串中的代码
a = 10
b = 12
# print(eval("a*b"))  #
# print("hello"[0])  # 字符串索引
# print(eval('"abc"[0]'))  # 字符串索引,eval把引号给去掉了

# data = eval(input("请输入："))  # 输入任何类型，都会被转换成相对应的类型
# print(data, type(data))  # 如果input里输入字符串，要加上引号，否则会报错
# eval的方法不推荐使用，因为eval会执行字符串中的代码，如果字符串中包含恶意代码，会带来安全风险


#      list(可迭代对象) 将值转换为列表
#      tuple(可迭代对象) 将值转换为元组
#       set(可迭代对象) 将值转换为集合
#      dict(可迭代对象) 将值转换为字典
# 字符串是可迭代对象，所以可以直接转换为列表，元组，字典，会把字符一个一个拆分
# print(list("hello"))  # ['h', 'e', 'l', 'l', 'o']
# range() 生成的数字序列，也是一个可迭代对象
# print(list(range(11, 16)))  # [11, 12, 13, 14, 15]

li = [1, 2, 3]
# print(tuple(li))  # (1, 2, 3)
# print(li, type(li))  # [1, 2, 3] <class 'list'> 没有变化

li = {"a": 2, "fas": 5, "jgs": 32}
# print(list(li))  # ['a', 'fas', 'jgs'] # 字典默认操作键
# print(list(li.values()))  # [2, 5, 32]
# print(set(li.items()))  # [('a', 2), ('fas', 5), ('jgs', 32)]

### 通常使用dict()时，一般是创建新字典
# 创建字典的方式1
dic = {"a": 1, "b": 2, "c": 3}
# print(dic)
# 创建字典的方式2
d = dict(a=1, b=2, c=3)  # 变量名=值 --> {"变量名":值}
# print(d)

# # 列表无法转换为字典，因为字典的键不能重复，而列表可以重复。并且，单一列表无法同时设置键和值
# li = [1, 2, 3]  # print(dict(li))  # 报错，因为列表的值不能同时作为键和值
# li = [(1, 2), (3, 4), (5, 6)]
# # [(1, 2), (3, 4), (5, 6)]  # 列表中的元素是元组，元组中的第一个元素作为键，第二个元素作为值
# print(dict(li))

# 把字符串转换成列表，然后再转换回去，无法转换回字符串
s = "hello"
li = list(s)
# print(li, type(li))  # ['h', 'e', 'l', 'l', 'o']

# li2 = str(li)
# print(li2, type(li2))  # ['h', 'e', 'l', 'l', 'o'] <class 'str'>

# 如果想转换成被分割前的字符串 连接符.join(列表) 连接符表示用什么来连接这个列表
print("_".join(li))  # 如果前面只是"",则表示空白，把列表的各个元素用空白紧密连接起来
# 该方式列表，元组，集合也可以连接，需要注意，只有序列的元素是字符串时，才能使用该方法
l = {"ads", "gfsa", "sadf", "afd", "sfa"}
l = list(l)
print("".join(l[1:4:2]))
