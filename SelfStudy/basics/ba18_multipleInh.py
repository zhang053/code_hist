# 多继承
# 从多个父类中继承

import time


class Watch:
    def show_time(self):
        print("使用 Watch 类")
        print(f"NOW: {time.asctime()}")  # 显示当前时间

    def set_alarm(self):
        print("设置闹钟")


class HealthDevice:
    def check_heart_rate(self):
        print("测试心率")

    def count_steps(self):
        print("测试步数")

    def show_time(self):
        print("使用 HealthDevice 类")
        print(f"{time.asctime()}")


# 在自身没有同名函数，但多继承的父类的函数中有同名时，使用先继承到的函数，也就是使用括号左边的类中的同名函数
class SmartWatch(HealthDevice, Watch):
    pass


sw = SmartWatch()
sw.check_heart_rate()
sw.show_time()

# 使用属性 __mro__ 来确认，子类调用方法时的查找路径，也就是告诉你python按什么顺序去各个类里找这个方法
# 返回元组
# 查看路径
print(SmartWatch.__mro__, type(SmartWatch.__mro__))
# 先找括号左边的，如果左边的类中有函数，则直接调用，不会继续往下寻找，所以，有同名函数时调用左边的
# 左右都没有时，调用父类的父类，往更上层搜索

# 不建议使用多继承，因为可能修改一个父类，就会影响一连串子类 ， 且容易混淆，复杂
# 建议使用单继承加组合的方式
# 在单继承中实例化
# class HD(Watch):
#     h = HealthDevice()
