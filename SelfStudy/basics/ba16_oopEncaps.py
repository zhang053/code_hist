# 封装

# 面向对象三大特征
# 封装：隐藏对象的属性和实现细节，仅对外公开接口
# 继承：实现代码重用和扩展
# 多态：接口重用

# # 封装
# 将复杂信息隐藏在内部，只对外提供简洁的接口
# 类本质上就是封装


# class Bank:
#     def __init__(self, name, balance):
#         self.name = name
#         self.balance = balance

#     def chack_balance(self):
#         print(f"{self.name} ' balance is : {self.balance}")


# bank = Bank("zhang", 100)
# bank.chack_balance()

# bank.balance = 10000
# bank.chack_balance()

# 直接通过外部调整，不安全

# # 类中定义私有


# class Bank:
#     def __init__(self, name, balance):
#         self.name = name
#         self.__balance = balance  # 私有属性（不允许类外直接访问或修改）

#     def check_balance(self):
#         print(f"{self.name} ' balance is : {self.__balance}")

#     # 存款
#     def deposit(self, amount):
#         if amount > 0:
#             self.__balance += amount
#             print("存款成功")
#         else:
#             print("存款金额必须是正数")


# # 直接访问私有属性，会报错
# bank = Bank("zhang", 1000)

# # 通过公开的方法访问私有属性（正确方式）
# # 在类的内部添加公开的访问方式
# bank.check_balance()
# bank.deposit(100)
# bank.check_balance()

# # 使用property 简化访问（方法伪装成属性）
# property(fget=None, fset=None, fdel=None, doc=None)
# 1,fget:获取属性值的方法
# 2,fset:设置属性值的方法
# 3,fdel:删除属性值的方法
# 4,doc:属性的描述信息，如果省略，会把fget的doc作为属性的doc，说明文档的形式是前后三个双引号围起来的文章


# class Bank:
#     def __init__(self, name, balance):
#         self.name = name
#         self.__balance = balance

#     def getBalance(self):
#         # 获取余额 井号
#         """获取余额 三个双引号"""
#         return self.__balance

#     def addBalance(self, new_balance):
#         # 存款
#         if new_balance > 0:
#             self.__balance += new_balance
#             print("success to add balance")

#     balance = property(fget=getBalance, fset=addBalance, doc="this is balance")


# bank_account = Bank("zhang", 1000)

# # bank_account.balance = 5000
# # AttributeError: property 'balance' of 'Bank' object has no setter
# # 这里balance只允许被获取，无法修改
# print(bank_account.balance)

# bank_account.addBalance(100)
# print(bank_account.getBalance())
# print(Bank.balance.__doc__)

# 弊端：每个功能都要有一个函数，臃肿

# 解决方法
# @property 装饰器


# class Bank:
#     def __init__(self, name, balance):
#         self.name = name
#         self.__balance = balance

#     # 标记为读取属性的方法，必须要同名
#     @property
#     def balance(self):
#         # 获取余额 井号
#         """获取余额 三个双引号"""
#         return self.__balance

#     # 标记为修改属性的方法，需要与属性名一致,三个属性，必须要同名
#     @balance.setter
#     def balance(self, new_balance):
#         # 存款
#         if new_balance > 0:
#             self.__balance += new_balance
#             print("success to add balance")

#     # 标记为删除属性的方法，必须要同名
#     @balance.deleter
#     def balance(self):
#         del self.__balance


# bankAccount = Bank("hao", 1000)
# print(bankAccount.balance)

# bankAccount.balance = 500
# print(bankAccount.balance)

# # del bankAccount.balance
# print(bankAccount.balance)

# # # 不推荐的访问方式
# 名称改写


class BankAccount:
    def __init__(self, name, balance):
        self.name = name
        self.__balance = balance

    def __private(self):
        print("this is private area, donot request")


account = BankAccount("shu", 100)

# # # dir(对象): 查看对象的所有属性和方法
# print(dir(account))
# print(account._BankAccount__balance)
# account._BankAccount__balance = 500
# print(account._BankAccount__balance)  # 成功被修改，但是该方法违背了封装的原则

# account.__private()  # 通过该方法无法获取私有函数
account._BankAccount__private()  # 但是可以这样获取私有函数，但是不推荐
