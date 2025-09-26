# jsonpath 用于提取json字符串中数据的工具
# 需要先安装 pip install jsonpath
# 然后  from jsonpath import jsonpath

from jsonpath import jsonpath

data = {
    "data": {
        "aigcEditParams": {"ispq": 0, "showEditEntry": 1},
        "applid": "10642317779320561439",
        "disgusting": 0,
        "dyTabData": [
            {
                "ename": "ps",
                "iconcontent": "\\e608",
                "name": "网页",
                "url": "//www.baidu.com/s?wd=_QUERY_",
                "price": 80.3,
            },
            {
                "ename2": "ps",
                "iconcontent2": "\\e608",
                "name2": "网页",
                "url2": "//www.baidu.com/s?wd=_QUERY_",
                "price": 53,
            },
        ],
    },
    "data2": {
        "aigcEditParams": {"ispq": 0, "showEditEntry": 1},
        "applid": "10642317779320561439",
        "disgusting": 0,
        "dyTabData": [
            {"ename": "ps", "iconcontent": "\\e608", "name": "网页", "price": 340},
            {"ename": "ps", "iconcontent": "\\e608", "name": "网页", "price": 3.3},
        ],
    },
}

# $ 根节点
# matches = jsonpath(data, "$")  # False , $根节点不能单独使用
# matches = jsonpath(data, "$.data2.dyTabData")  # . 子代匹配
# matches = jsonpath(data, "$.data2.dyTabData..url")  # .. 匹配子代中所有的url
# matches = jsonpath(data, "$.data.*")  # .* 把data的所有子代都输出出来
# matches = jsonpath(data, "$.data.dyTabData[*]")
# 把dy...中的所有子代的值都拿过来，把子代中所有的值都拿出来放入一个列表，可用来遍历


# 高阶用法
# matches = jsonpath(data, "$.data.dyTabData[1]")  # 列表操作，支持切片
# matches = jsonpath(data, "$.data.dyTabData[0:2]")  # 列表操作，支持切片

# 条件匹配 [?(条件)]
# matches = jsonpath(data, "$.data.dyTabData[?(@.name)]")
# @表示当前位置，在当前位置寻找包含有name的元素

matches = jsonpath(data, "$..[?(@.price<70)]")  # 可以使用判断符

for match in matches:
    print(matches)
