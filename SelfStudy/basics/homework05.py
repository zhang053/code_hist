# 1
def Quotient(num1, num2):
    return num1 / num2


try:
    num1 = int(input("enter the dividend "))
    num2 = int(input("enter 2nd divisor: "))
    result = Quotient(num1, num2)
except ValueError:
    print("catched ValueError")
except ZeroDivisionError:
    print("catched ZeroDivisionError")
else:
    print("result = ", result)


# # 2
def Root(num3):
    if num3 < 0:
        raise Exception("num3 < 0")
    else:
        result = num3**0.5
        return result


num = 9
print(f"{num}的平方根是： {Root(num)}")


# 3
class Student:
    def __init__(self, name, age, sex, eng_score, math_score, chn_score):
        self.name = name
        self.sex = sex
        self.age = age
        self.escore = eng_score
        self.mscore = math_score
        self.cscore = chn_score

    def total_score(self):
        return self.escore + self.mscore + self.cscore

    def average_score(self):
        ave = self.total_score() / 3
        return ave

    def show_info(self):
        print(self.name)
        print(self.age)
        print(self.sex)
        print(self.escore)
        print(self.mscore)
        print(self.cscore)


# fmt: off
st1 = Student("zhang" , 20 , "male" , 100 , 99 , 98)
# fmt: on
print(st1.total_score())
print(st1.average_score())
st1.show_info()


# # # 4
class Person:
    def __init__(self, name, age, sex):
        self.name = name
        self.age = age
        self.sex = sex

    def printInfo(self):
        print(f"name: {self.name}")
        print(f"age: {self.age}")
        print(f"sex: {self.sex}")


class Student(Person):
    def __init__(self, name, age, sex, college, class_):
        super().__init__(name, age, sex)
        self.college = college
        self.class_ = class_

    def printInfo(self):
        super().printInfo()
        print(f"college: {self.college}")
        print(f"class: {self.class_}")


st2 = Person("zhang", 20, "male")
st2.printInfo()
st2 = Student("zhang", 20, "male", "computer", "d")
st2.printInfo()


# # 5
class BankAccount:
    def __init__(self, balance):
        self.__balance = balance

    def deposit(self, money):
        print(f"存款：{money}")
        self.__balance += money
        return self.__balance

    def withdraw(self, money):
        if money < self.__balance:
            self.__balance -= money
            print(f"成功取款 {money}元")
            return self.__balance
        else:
            print("取款失败")
            return None

    def get_balance(self):
        print(f"当前余额为 {self.__balance}")
        return


ba = BankAccount(1000)
ba.deposit(100)
ba.withdraw(1000)
ba.withdraw(1000)
ba.get_balance()


# # 6
def Data(age, sex):
    if age not in range(0, 121):
        raise Exception("年龄不符合预期")

    if sex not in ("female", "male"):
        raise Exception("性别不符合")

    print("年龄和性别符合预期")


age = int(input("age: "))
sex = input("sex: ")
Data(age, sex)

# # 7
import random


def guess_num():
    target = random.randint(0, 99)
    while 1:
        enter_num = int(input("enter a number: "))
        if enter_num == target:
            print("你猜中了！！")
            break
        elif enter_num < target:
            print("猜错了，再大一些")
        elif enter_num > target:
            print("猜错了，再小一些")


guess_num()


# # 8
def rps():
    choices = ["r", "p", "s"]  # rock , paper , scissors

    p_choice = input("玩家出拳: ")
    if p_choice not in choices:
        print("请出石头/剪刀/布，r/p/s")
        return

    c_choice = random.choice(choices)
    print("电脑出拳:", c_choice)

    if p_choice == c_choice:
        print("平局！")
    elif (
        (p_choice == "r" and c_choice == "s")
        or (p_choice == "s" and c_choice == "p")
        or (p_choice == "p" and c_choice == "r")
    ):
        print("玩家赢！")
    else:
        print("电脑赢!")


# count = 1
# while 1:
#     print(f"round {count}")
#     rps()
#     count += 1
#     print("\n")
