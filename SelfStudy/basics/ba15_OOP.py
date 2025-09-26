# ================== 面向过程 vs 面向对象 ==================
#
# 【1. 面向过程（Procedural）】
# - 核心思想：以“过程（函数）”为中心，把问题分解为步骤。
# - 特点：
#   * 程序 = 数据 + 函数
#   * 强调“怎么做”
#   * 常见语言：C、早期 BASIC、Pascal
# - 优点：
#   * 简单直观，逻辑清晰
#   * 性能高（无对象封装的开销）
# - 缺点：
#   * 数据与操作分离，容易被任意修改，缺乏安全性
#   * 项目规模大时，维护困难，复用性差
#
# ---------------------------------------------------------
#
# 【2. 面向对象（OOP, Object-Oriented Programming）】
# - 核心思想：以“对象”为中心，对象 = 数据(属性) + 操作(方法)
# - 三大特性：
#   * 封装：数据和方法绑定在对象内部
#   * 继承：可以复用和扩展已有类
#   * 多态：不同对象对同一消息有不同的响应
# - 优点：
#   * 更贴近人类思维（对象集合、交互）
#   * 可复用性高，维护性好，适合大型软件
# - 缺点：
#   * 学习成本高
#   * 性能略低于面向过程（对象创建/调度有开销）
# ---------------------------------------------------
#
# 【面向过程（手洗）】
# 在实现一个功能时，注重的是具体的执行步骤。
# 将整个任务拆解成多个独立的步骤，并为每个步骤定义一个函数，
# 然后通过依次调用这些函数来完成整个任务。
# 在这种方式下，每一步都需要我们亲自去定义和实现，
# 如同手洗衣物，每一步都需要我们亲自动手操作。
#
# ---------------------------------------------------
#
# 【面向对象（机洗）】
# 在实现一个功能时，更侧重于“谁”来执行这些任务。
# 通过定义对象及其行为（方法），可以让对象来为我们完成任务，
# 而不需要我们亲自执行每一个细节。
#
# 这种方式就像使用洗衣机洗衣服，
# 我们只需设定好洗衣机的工作模式和放入衣物，
# 洗衣机就会自动完成洗涤、漂洗、甩干等一系列操作。
# 我们无需亲自动手，从而实现了“偷懒、找别人帮我做”的效果。
#
# ---------------------------------------------------------
#
# 【4. 总结对比】
#
# 面向过程：
# - 按步骤解决问题（过程）
# - 数据与函数分离
# - 适合小型程序、对性能敏感场景
#
# 面向对象：
# - 按对象及其交互解决问题
# - 数据与操作封装在对象中
# - 适合大型复杂系统、需要复用和扩展
#
# =========================================================

# 类
# 对一系列具有相同属性和行为的事务的统称
# 属性： 特征，用来描述什么样子
# 行为： 执行的动作

# 万物皆为对象，包括函数等


# def func():
#     print(12)


# print(type(func))

import random

# print(type(random))

# 注意
#  面向对象编程中，现有类，后有对象，必须先定义 类作为模板，才能根据类创建对象

# 建议使用首字母大写的形式命名,后面可以不要括号


# 以汽车为例，声明一个类
# class Car:
#     """汽车类"""

#     pass  # 使用pass，可以暂时先不定义内容，跳过，占位符


# 占位符 pass 表示空语句，当语法上需要语句，但又不想执行任何操作时使用

# 只是定义声明，不会有任何操作

# 实例化对象（创建对象）
# 变量名=类名()来使用
# print(Car())
# car = Car()
# print(car, id(car), type(car), sep="\n")  # id:2582682233088

# # 第二次实例化
# car2 = Car()
# print(car2)
# print(id(car2))  # id:2582684504528
# # 内存地址不同，说明car和car2时两个不同的对象 --> 一个类可以创建多个对象


# # # 类中定义方法 （方法既是函数）
# 实例方法：定义在类中的函数，必须由对象调用，至少包含一个self参数
# self参数会自动绑定到调用该方法的对象，通过self可以在方法内部访问对象的属性或其他方法
# class Car:
#     def run(self):  # 带有self参数的方法，self代表对象本身 等于claa的名字
#         # 可以改成其他的名字，但是不推荐
#         print("汽车启动")
#         print("self: ", self)


# run()  # NameError: name 'run' is not defined  # 不可以直接调用
# Car.run()  # TypeError: Car.run() missing 1 required positional argument: 'self' #
# 通过Car 类调用，必须要给self传参数

# Car().run()  # 但是通过Car() 对象调用，则不用传参数

# car1 = Car()
# print(car1)
# car1.run()

# car2 = Car()
# print(car2)
# car2.run()

# 哪一个对象调用的实例方法，那么实例方法中的self参数就是哪一个对象

# 意思
# 意思是self变量里带入的是本身，带入点前面的对象

# 比如，isupper，"aaa".isupper()  这个括号内不需要传参的原因是，这个函数定义时括号内是self
# 就是self="aaa"的意思，isupper("aaa")

# # 类中定义属性
# 1，类属性
# 定义在类中，方法体外的变量，属于类本身，呗该类的所有实例共享


class Car:
    wheels = 4  # 类属性： 不管什么样的类型，都共同的属性，变量

    def run(self):
        print("starting Engine...")

    # def display_info(self, brand):
    #     # 显示汽车的品牌
    #     print(f"this car's brand is: {brand}")  # self.属性名/对象名.属性名 --> 实例属性

    def display_info(self):
        # 显示汽车的品牌
        print(
            f"this car's brand is: {self.brand}"
        )  # self.属性名/对象名.属性名 --> 实例属性


# # 访问类属性
# print(Car.wheels)
# # 当每个对象的属性值都相同是，将该属性定义为类属性

# 当对象的属性值不同时，将该属性定义为实例属性
# 2，实例属性
# 实例属性时每个对象独有的属性，通过self在实例方法中定义，每个对象的实例属性可以有不同的值
# car3 = Car()
# car4 = Car()
# # 给car3的实例属性赋值
# # car3.display_info("SUBARU")  # 该方法对应上面的display_info函数
# # 给car4的实例属性赋值
# car4.brand = "BENZ"  #  # 该方法对应下面的display_info函数
# car4.display_info()

# # car4.color = "red"
# # print(car4.color)
# # print(car3.color) # 因为没有给car3定义color，所以没有这个属性，会报错

# # # 构造函数  __init__
# __xx__时python中的魔术方法/属性


# class Car:
#     def __init__(self):
#         print("__init__ is called")


# car = Car()
# car2 = Car()  # 每次Car实例化的时候都会调用自动__init__,无需手动调用


# class Cars:
#     def __init__(self, brand, color):  # 因为每次实例化时都会自动执行，所以在这里可以
#         self.brand = brand
#         self.color = color

#     def display_info(self):
#         print(f"car's brand: {self.brand}, car's color:  {self.color}")


# car1 = Cars("SUBARU", "WHITE")
# car1.display_info()

# car2 = Cars("BENZ", "BLACK")  # 此时self 表示car2 。 self.brand = car2.brand
# car2.display_info()


# 一般情况下，实例属性在构造函数中定义


# 析构函数 __del__
# 当对象被销毁（内存被回收）前，python的垃圾回收机制会自动调用该方法


# class Car:
#     def __del__(self):
#         print(f"{self} is deleted")


# car = Car()

# # del car  # 在del函数中，直接触发__del__程序，触发垃圾回收机制

# print("程序执行中1。。")
# print("程序执行中2.。")
# print("程序执行中3。。")  # 在程序结束时，__del__被自动执行

# car2 = Car()
# car2 = car
# print("befor delete car")
# del car  # 虽然在这里删除了，但是因为car还赋值给了car2，所以不会被删除
# print("after delete car")
# print("car2 will be deleted")
# del car2
# print("car2 is be deleted")

# python 有自动回收机制，所以大部分情况下都不需要定义

# 但是其他语言，会需要用到，比如java

# __str__
# 用于定义对象的字符串表示形式，当使用print函数输出对象或需要字符串表示时， 会自动调用该方法


class Car:
    def __str__(self):
        return f"car's brand: {self.brand}, car's color:  {self.color}"
        # 默认情况下，直接打印对象会输出其类型和内存地址，不够直观
        # 可通过该方法自定义输出格式
        # ！__str__必须有返回值，必须是字符串类型

    def __init__(self, brand, color):
        self.brand = brand
        self.color = color


car = Car("BMW", "White")
print(car)

# # # 应用场景
# 1，提供对象的可读性好的字符串表示
# 2，方便调试和日志输出
# 3，在格式化字符串中使用对象
