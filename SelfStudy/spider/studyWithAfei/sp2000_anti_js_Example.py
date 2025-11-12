"""
逆向获得的代码通常是js，所以一般使用js发请求，但是不熟悉，需要使用python发请求

另类方法
    通过python控制nodejs执行js代码，从而获取数据
    1.需要把参数传入js代码 , 使用argv
    2.python调用js代码，获取返回值 , 增加subprocess的参数，使用r.stdout
"""

import subprocess

# subprocess.run(
#     [
#         "node",
#         "D:\StudyPy\py_practice\SelfStudy\spider\studyWithAfei\sp2001_js.js",
#         "123",
#     ]
# )
# 可以在js文件中通过process.argv获取参数，现在传进去的用process.argv[2]获取，可以传递参数

py_x = 100
# r = subprocess.run(["node", "sp2001_js.js", str(py_x)])
# 命令行只有文字，所以需要类型转换
# print(r)  # CompletedProcess(args=['node', 'sp2001_js.js', '100'], returncode=0)
# 返回的是看不懂的内容

# # # 如何获取js代码的返回值
r = subprocess.run(
    ["node", "sp2001_js.js", str(py_x)],
    capture_output=True,  # 捕获输出, js文件中的console.log的内容不会打印
    text=True,  # 把输出转换为字符串
    encoding="utf-8",  # 指定输出编码
)
print(r.stdout)  # 获取console.log的内容
