# # # 模块
# import time  用ctrl键按住点击，可以看到这个库可以实现的功能，这些是python自带的库
# print(time.asctime())

# 通过社区提供的第三方库 pip install

# 3)自定义模块，每一个代码都是一个模块
# import 导入

import ba12_ErrorMessage as m

# as 设置别名

# 使用功能 模块名.功能名
# print(ba12_ErrorMessage.name)
# ba12_ErrorMessage.print_func("correct")
# ba12_ErrorMessage.sayHello_func()

# # 如果导入的模块名太长，可以后面加上as ， 自己起一个短的别名使用
# print(m.name)
# m.sayHello_func()
# m.print_func("Um ~ ?")

# 如果只想要导入部分功能，from 模块名 import 功能名
# from ba12_ErrorMessage import print_func, sayHello_func

# # 如果想导入全部功能
# from ba12_ErrorMessage import *  # 星号导入全部功能

# # 这个s是name的别名，如果想挨个起别名，需要每一个后面写as 别名

# # 可以使用逗号来导入多个，并且函数不需要后面的括号
# sayHello_func()
# # 前面不需要加模块名称

# # 在本模块中使用和引入的同名的话，(使用from方式),后定义的会覆盖掉前面的


# # # 以主程序的形式执行
# 每一个模块内都有一个变量__name__，前后两个下划线，用于区分模块的运行方式
# 当模块直接运行时，__name__的值为"__main__"
# 当模块被导入时，__name__的值为"模块名"
# 作用：在模块中编写测试代码，确保导入时不执行测试逻辑

import ba12_ErrorMessage

# 在导入的瞬间，什么都不用做，所有的被导入的模块中的所有代码都会执行
# 如果在被导入的模块中加入判断则不会被执行
# if __name__ == "__main__"
