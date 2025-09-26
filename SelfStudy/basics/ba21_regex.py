# # # 正则表达式 Regular Expression　有规律的表达式
# 一种字符串处理工具

import re  # 需要先导入模块，这个是python内置的模块

# re.match(pattern, string, flags)
# pattern 表达式的模式 string 要搜索的字符串 flags 标志位，是否区分大小写，是否多行匹配啥的，0则是默认
# 没找到 返回none

# # pattern 匹配开头的字符
# res = re.match("he", "hello")  # match：从开头开始匹配
# print(res)  # 没搜索到返回none
# print(res.group())  # 没搜索到会报错，因为只有match有group函数，none没有
# # .group() 返回匹配的数据

# # # 匹配单个字符
# " . " 匹配任何字符，除了\n 换行符
# res = re.match(".", "*python")
# print(res)
# print(res.group())

# [] 匹配括号内的单个字符
# res = re.match("[pHk]", "Hello")  # 匹配开头为 p H k中任意一个
# res = re.match("[1234567890]", "253086273") # 匹配任何数字
# res = re.match("[0-9]", "253086273")  # 简写
# res = re.match("[0-46-9]", "3086273")  # 简写,匹配除了5以外的任何数字
# res = re.match("[a-z]", "gasadf73")  # 简写，匹配任何小写字母
# res = re.match("[a-zA-Z]", "gasadf73")  # 简写，匹配任何大写，小写字母
# res = re.match("[a-z]", "Aafdshp", re.I)  # re.I 忽略大小写
# res = re.match("\D", "Aafdshp")  # 因为正则也会进行转义，所以使用反斜杠时前面加个r
# # # 写在pattern中的字符
# # .       匹配任意 1 个字符（除了 \n）
# # [ ]     匹配 [ ] 中列举的字符
# # \d      匹配数字，即 0-9
# # \D      匹配非数字，即不是数字
# # \s      匹配空白，即 空格、tab 键 ， \r \t \n 等也可以匹配到，没有内容显示的字符都可以匹配
# # \S      匹配非空白
# # \w      匹配单词字符，即 a-z、A-Z、0-9、下划线 _
# # \W      匹配非单词字符 比如 * & ， 非文字字符的
# print(res)
# print(res.group())

# import time
# for i in range(10, 0, -1):
#     print(f"\r{i}", end="")  # \r 用后输入的把前面的给覆盖掉，可以当个计时器
#     time.sleep(1)


# # # 匹配多个字符
# *        匹配前一个字符出现 0 次或无限次，即可有可无
# +        匹配前一个字符出现 1 次或无限次，即至少有 1 次
# ?        匹配前一个字符出现 0 次或 1 次，要么有 1 次，要么没有
# {m}      匹配前一个字符出现 m 次
# {m,n}    匹配前一个字符出现从 m 到 n 次

# res = re.match("\d*", "1234sggs124")
# 匹配任意个数字字符 ， 没匹配到也可以，任意包括0个
# res = re.match("\d+", "23hosd342")
# 匹配1个或者多个数字字符，没有则会报错  (最少匹配一个)
# res = re.match("\d?", "hoasjfi")
# 匹配0或者1个数字字符，没匹配到也可以，(最多匹配1个)
# res = re.match("\d{3}", "125hoasjfi")
# 花括号中的数字表示匹配个数，3 --> 匹配3个
# res = re.match("\d{2,4}", "125hoasjfi")
# # 识别 2到4 个字符，如果不满足2，只有1个数字的话，会报错
# print(res)
# print(res.group())

# # #　findall()  在字符串中查找所有(非重叠)匹配的字符串，返回一个列表
# res = re.findall("\d", "123hoah134ag23")
# res = re.findall(r"^\w", "|123hoah134ag23")
# \w 匹配所有单词字符，前面加个 "^" 匹配开头的第一个单词字符,但是开头没找到 会返回空列表

# res = re.match("[^asd]", "|123hoah134ag23")
# 在匹配字符中"^"表示取反，取a s d 以外的字符串

# res = re.findall("\d$", "afdsio123")
# "$" 从后尾开始匹配，匹配结尾的一个数字字符

# "|" 匹配 | 的左右的表达式
# res = re.findall(r"\d|\s", "1 adsf")
# # 使用场景，匹配邮箱
# 邮箱：1234567@qq.com  --> 邮箱格式：xxxx@qq.com
# res = re.match(r"\w+@(qq|gmail|126)\.com", "1234567@gmail.com")
# 匹配至少一个单词字符，然后必须要有@,然后匹配“.com”，前面要加反斜杠，不然就会匹配所有字符. 可以把括号中的看作整体

# res = re.match(r"<(\w+)>.*</\1>", "<body>hello re</body>")
# # \1 表示匹配前面的第一个分类也就是小括号中的内容
# # 中间表示匹配任意数量的任意字符
# res = re.match(r"<(\w+)><(\w+)>.*</\2></\1>", "<body><h1>hello re</h1></body>")
# # 从左往右排序1，2，3...
# print(res.group())  # 列表没有group方法，只有match有

# # # 常见函数
# search(pattern,string,flag) 查找字符串，然后返回第一个匹配的结果，没有返回none
# res = re.match(r"\d", "a123oafdjo")
# match会匹配从头开始匹配第一个,如果开头第一个不符合，会报错
# res = re.search(r"\d", "asadfs34jlso")  # 从头到尾都找一遍，一直没有才会返回none
# print(res)

# # 替换所有匹配部分
# sub(pattern , repl , string , count , flag) pattern 匹配字符串，repl 要替换的字符串 ， count 替换次数 ， flag 标志位
# res = re.sub("zhang", "shuhao", "hello,zhang")
# res = re.sub(r"\d+", "xxx", "afh233ho3a2", count=2)
# # 把所有数字字符替换成xxx , count = 1 替换1次
# print(res)
# "+" 直到无法满足为止

# # # 贪婪匹配  尽可能多的匹配结果
# res = re.match(r"\d*", "3243ofdasoh23")
# print(res.group())

# # 非贪婪匹配   按最少次数匹配
res = re.match(r"\d*?", "3243ofdasoh23")
print(res.group())
# 匹配内容中加的问号? ，表示非贪婪匹配，按照星号* 的最少匹配次数0次进行匹配
# 如果是加号后面跟个问好 +? 加号的最少次数是1，所以只匹配一次
# 如果决定次数了{4,8} 默认贪婪尽可能多的匹配到8个字符，非贪婪模式加个问号匹配到最少次数4次
