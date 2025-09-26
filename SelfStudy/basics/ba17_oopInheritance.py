# # 继承
# # 子类（派生类）： 可以继承父类（基类）的所有非私有属性和方法

# # class 类名("父类")：
# # # # 传承可以传递
# # 单传承


# class animal:
#     def __init__(self, name, age):
#         self.name = name
#         self.age = age

#     def eating(self):
#         print(f"{self.name} is eating....")

#     def sleeping(self):
#         print(f"{self.name} is sleeping..")


# class Dog(animal):
#     def bark(self):
#         print(f'{self.name} : "汪汪汪"')


# # dog = Dog("inu", 2)
# # dog.sleeping()
# # dog.eating()
# # dog.bark()


# class keji(Dog):
#     def playing(self):
#         print(f"{self.name} is playing...")


# kejiquan = keji("dahuang", 5)
# kejiquan.sleeping()
# kejiquan.playing()


# 和父类同名的函数会被覆盖掉
class Animal:
    def make_sound(self):
        print(" some animal is saying something ")


class Dog(Animal):
    def make_sound(self):  # 同名函数，子类会覆盖父类
        print(f" dog is barking ")
        # Animal.make_sound(self)
        # 该方法不推荐，因为一旦父类名发生修改，这里也要修改
        super().make_sound()


dog = Animal()
dog = Dog()
dog.make_sound()


# # 所有类都默认继承（object）
