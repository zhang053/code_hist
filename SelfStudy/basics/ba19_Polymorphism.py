# # 多态
# # 同一个方法名，在不同的类里可以有不一样的实现。
# # 好处：用起来更灵活，不用关心对象的具体类型，只要调用同样的方法就行。

# # 比如 支付
# # 使用微信支付，钱从微信里扣
# # 使用支付宝，钱从支付宝里扣


# class WechatPay:
#     def pay(self, money):
#         print(f"微信支付 {money} 元")


# class AliPay:
#     def pay(self, money):
#         print(f"支付宝支付 {money} 元")


# class CreCardPay:
#     def pay(self, money):
#         print(f"银行卡支付 {money} 元")


# # 统一支付接口，不关心具体的支付类型，只要有pay方法即可
# def pay_order(pay_method, amount):
#     pay_method.pay(amount)  # WechatPay().pay(amout)  # 执行方式


# # 同一种调用方式，能够根据传入对象的不同产生不同的结果 --> 多态
# pay_order(WechatPay(), 400)
# pay_order(AliPay(), 100)


# # # # 多态与继承
# # 想要增加功能时，不需要重写代码，只需要添加，并使用对应方法调用即可


# class Animal:
#     def eat(self, animal):
#         print(f"eating...", end="")
#         animal.eat()


# class Cat(Animal):
#     def eat(self):
#         print("fish")


# class Sheep(Animal):
#     def eat(self):
#         print("glass")


# ani = Animal()
# ani.eat(Cat())
# ani.eat(Sheep())


# # # # 静态方法
# class Person:
#     def study(self):
#         print("person can study")
#         # 弊端1：需要专门创建对象来调用该实例方法
#         # 弊端2：方法内部没有使用到实例

#     # 使用 定义 静态方法
#     @staticmethod
#     def study_static():
#         print("use static method to apply this function")

#     @staticmethod
#     def study_subject(subject):
#         print(f"study {subject}")


# person = Person()
# person.study()
# # 弊端1 ： 需要专门创建对象来调用

# Person.study_static()
# # # 应用场景
# # 实现工具类功能
# # 方法里不需要用到类的属性，也不需要用到实例的属性，没有self属性
# # 需在类中放一个独立的函数，即使单独拿出来也可以使用

# Person.study_subject("python")


# #
# def study_subject(subject):
#     print(f"study {subject}")


# Person.study_subject("python")
# # 单独拿出来也可以的独立函数


# # # 类方法


class Person:
    age = 20

    def set_age(self):
        # global age  # 该函数并非全局变量，所以无法通过该方法子秀发i
        # self.age = 18  # 需要调用set_age 才可以改变,仅作用与当前对象
        Person.age = 10  # 修改类属性 弊端：可维护性差

    @classmethod
    def set_age2(cls, age):
        # print("cls: ", cls)
        # cls:  <class '__main__.Person'>
        # cls自动带入该类的类名 ， 和打印 print（Person）一样
        # cls.age = 12  # Person.age = 12
        cls.age = age


# person = Person()
# person2 = Person()
# # person.set_age()
# print(person2.age)  # 如果不调用set_age 函数就不会发生改变

# print(Person.age)
# Person.set_age2()

print(Person.age)
Person.set_age2(15)  # 不需要给cls传参，只需要给属性传参
print(Person.age)
