"""
# json 有特定的格式规则
# 1，最外层必须是个字典
# {
    花括号
    },
    [
    方括号
    ]
最外层只能是这两种括号

# 2，值允许的格式
    数字10，12
    字符串"afsojl"
    null
    true/false  ....之类的

# 3，属性和字符串的值必须是双引号， 区分双引号和单引号，只能是用双引号
"""

# json 最经常用于前后端数据传输，因为大部分语言都能很好的解析json
import json

s = """{
    "name": "hao",
    "age": 20,
    "height": "45",
    "weight": "40"
}"""

# json转字典
data = json.loads(s)
print(data)
print(data["age"])

# 字典转json
dic = {
    "name": "hao",
    "age": 20,
    "height": "45",
    "weight": "40",
    "male": False,
    "hobby": ["eating", "sleeping"],
}
sd = json.dumps(dic)
print(sd)
