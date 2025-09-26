# 包
# 包的含义
# 本质上，包是一个带有"__init__.py"文件的目录（文件夹）

# 创建包
# 新建文件夹，然后在其中创建文件取名 __init__.py

# __init__.py是包的标志文件， 功能是
# 1，标识目录为包
# 2，控制导入内容
# 3，执行轻量级操作，导入包的时候自动执行init中的代码

# 导入包
# import 包名.模块名
import ba14_packageFolder

# 为了保持包的清晰和高效，避免在init文件中写过多代码
import ba14_packageFolder.test01 as paTest

# print(py_package.test01.name) # 不使用别名的话需要写全
# print(paTest.name)

# 或者使用 from包名 import 模块名
# from py_package import test01
from ba14_packageFolder.test01 import name  # 导入模块中指定的功能

# print(name)

from ba14_packageFolder import *  # 导入包内的所有模块

# # ！！！当使用这种批量导入方式时，如果__init.py__文件中没有定义__all__变量
# 或者没有显示的导入包内的任何模块或者子包，那么他只会导入__init__.py中直接定义的内容
# 而不会导入包内的其他模块或者子包
# init的作用，控制导入的内容

# # # 使用__all__控制导入内容
# 这是一个列表，用于控制from import* 的导入范围
# 在模块中定义__all__时。from模块名import* 只会导入__all__列表中指定的功能
# 在包下的init.py中定义__all__，from 包名 import* 只会导入__all__列表中指定的模块或init.py文件中直接定义的功能

from ba14_packageFolder import *  # 在init.py中定义了__all__

print(test01.name)
