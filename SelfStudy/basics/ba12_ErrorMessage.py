# 异常会导致程序中断
# 1. NameError: 使用一个还未赋值的变量
# 2. SyntaxError: 代码不符合 Python 语法规定
# 3. IndexError: 下标/索引超出范围
# 4. ZeroDivisionError: 除数为 0
# 5. KeyError: 字典里不存在这个键
# 6. IOError（OSError）: 输入/输出失败；多见于文件不存在或无法打开
# 7. AttributeError: 对象没有这个属性
# 8. ValueError: 传入的值不合法/不符合要求
# 9. TypeError: 类型错误；传入的类型与期望不匹配
# 10. ImportError（ModuleNotFoundError）: 无法导入模块/包；多为路径或名称错误
# 11. IndentationError: 缩进错误；代码没有正确对齐

# # # 异常处理 try - except 语句来处理异常
# try:
#     尝试执行的代码  # 这个代码可能会报错，可能不会，所以需要try，常试
# except 异常类型 as 变量:
#     print("变量 num 未定义")
#     检测到异常要执行代码块 # 这个代码块是可选的，如果try中的代码没有报错，那么这个代码块不会执行
# else:
#     没有检测到异常要执行的代码块
# finally:
#     无论是否检测到异常都要执行的代码块

# # # 防止程序因异常而中断

# try:
#     num = int(input("请输入:"))
#     print(num)
# except:
#     print("输入错误")

# # 捕获指定异常类型
# # 1）单一异常
# try:
#     num = int(input("请输入:"))
#     print(num)
# except ValueError:
#     print("输入错误")

# # 2）多个异常
# try:
#     num = int(input("请输入:"))
#     print(num)
# except (ValueError, NameError):  # 使用元组的形式，来捕获多种异常
#     print("输入错误")

# # 对多种异常使用不同处理方式
# try:
#     num = int(input("请输入:"))
#     print(num)
# except ValueError:  # 可以对不同异常使用不同的处理方式
#     print("输入错误")
# except NameError:
#     print("变量 num 未定义")

# # 捕获所有异常
# try:
#     # num = int(input("请输入:"))
#     print(num)
#     # print(num / 0)
#     # print(1 > "3")
# except Exception as text:  # 可以捕获到所有非语法错误异常,比如缩进错误无法捕获，中文括号等
#     # 不加exception 同样可以捕获所有异常，但是无法获取异常信息，无法使用as变量
#     print(text)

# # else语句
# try:  # try下面最好只放一行代码，规范性写法
#     num = int(input("请输入:"))
#     print(num)
# except ValueError:
#     print("输入错误")
# else:
#     print("输入正确")  # try中的代码没有报错，那么这个代码块会执行
#     # 就是正常逻辑下的代码，链接try中没有报错情况下的代码

# # finally语句
# # 无论是否检测到异常都要执行的代码块
# # 比如关闭文件，因为如果文件及时关闭，不仅占用资源，还可能造成数据丢失。还可能导致后续对该文件的操作失效
# try:
#     # num = int(input("请输入:"))
#     print(num)
# except Exception as text:
#     print("输入错误", text)
# else:
#     print("输入正确")
# finally:
#     print("无论是否检测到异常都要执行的代码块")
#     # 通常与exception一起使用

# # 自定义异常
# # 自定义异常作用
# 实现业务错误的处理
# 附加丰富的错误信息

# 实现步骤
# 1, 创建自定义异常类
# 异常类型（异常具体描述信息）
# 2，使用raise语句抛出自定义异常
# raise会中断当前程序流程

# e = Exception("这是一个异常")
# raise e  # 让程序主动报错
# # raise Exception("这是一个异常")  # 也可以这样写

# # 实例: 编写函数，实现取款功能，当取款金额大于账户余额时，抛出异常
# balance = 1000  # 账户余额

# def withdraw(amount):
#     global balance
#     if amount > balance:
#         raise Exception(f"余额不足,当前余额为{balance}元")
#     else:
#         balance -= amount
#         print(f"取款成功,余额为{balance}")
#         return balance

# try:
#     withdraw(12)
# except Exception as text:
#     print(text)


# 以下是为了学习模块制作的函数

name = "this is ba12"


def print_func(text):
    print("you inputed:", text)


def sayHello_func():
    print("hello model")


if __name__ == "__main__":
    # 不想被其他模块执行的代码
    sayHello_func()
    print("__name__的值：", __name__)
