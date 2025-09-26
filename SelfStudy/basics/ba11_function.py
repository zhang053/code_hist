# 函数：封装好的可以重复使用的  需要先定义后调用


# 定义函数 def 函数名(参数1, 参数2, ...):
def print_hello():
    print("hello")
    print("have a nice day")


# 调用 执行函数
# print_hello()

# 形参：定义函数时，函数名后面的变量名
# 实参：调用函数时，函数名后面的变量名


def add(a, b):  # a, b 形参
    print(a + b)


def say_name(name="zhang"):  # 可以设定一个默认值，之后调用时不传参也可以
    print("my name is " + name)


# say_name("hiro")
# say_name(name="hiro")  # 如果有多个参数，但是不想给前面的参数传参，可以指定参数名

# fmt: off
# 设置参数默认值时，必须把有默认值的参数放在后面
def make_tea( tea, sugar = 5 ):  # parameter without a default follows parameter with a default
    print("make tea")
    print("sugar: " + str(sugar))
    print("tea: " + tea)
# fmt: on

# make_tea("wulong", 9)


def print_name(*names):  # *names 表示可以传入任意多个参数，这些参数会被封装成一个元组
    print(f"hello {names}")  # 不传递也可以
    for name in names:
        print(f"hello {name[0:6:2]}")


# print_name()
# print_name("zhang", "cho", "hiro")

# fmt: off

# 该方法多用于有污染的数据，比如填写用户数据时的 必填和选填
# 必填的定义参数名，选填的用双星号来接受
def info(**kwargs):  # **kwargs 表示可以传入任意多个参数，这些参数会被封装成一个字典,任何类型
    for key, value in kwargs.items():
        print(f"{key}: {value}")
        print(f"information: {kwargs}")
        print("="*12)

# info(name="z hang", age=18, gender="male")
# fmt: on


# return 返回值 ，可以让函数立即结束，并且返回一个值
# 如果没有return，函数默认返回None
def add(a, b):
    if a < b:
        return a + b
    return a - b, a + b, "计算结束"  # 返回值有多个时，用一个元组形式接受


# num = add(5, 2)
# print(num, type(num))
# 元组可以解包
a, b, c = add(5, 2)
# print(a, b, c)

# 在局部生成的变量，在函数外部无法访问
# 在局部生成全局变量 global 变量名
# 在函数内部修改全局变量 global 变量名
# global 只能用于修改全局变量，不能用于创建全局变量

a = 2


# def func():
#     # global a
#     a = 3
#     global b
#     b = 4
#     print(a)


# func()
# print(a, b)

a = 9


# nonlocal 只能在嵌套函数中使用，用于修改嵌套函数中的变量
def outter():
    # nonlocal a  # SyntaxError: no binding for nonlocal 'a' found， 无法在表层使用
    a = 3
    print(a)

    #  这个变量是在outter中定义的，所以只能在outter中使用
    def inner():
        nonlocal a  # 声明为外层函数的局部变量，修改上一层变量的值
        a = 4
        print(a)

    inner()  # 在外函数里面，在内函数外面
    print(a)


outter()
print(a)

# nonlocal 如果没有找到外层函数的局部变量，就会继续向上找，直到找到为止，如果都没有找到，就会报错
# nonlocal 只能用于修改外层函数的局部变量，不能用于创建全局变量
# nonlocal 和 global 的区别是，nonlocal 只能用于修改外层函数的局部变量，而 global 可以用于修改全局变量
