# # # 文件读写
# 代码执行中的列表之类的数据，在每次结束时都会删除
# 把结果保存到文件

# 保存的文件，可以分成2大类
# 1,文本文件 ： 把字符信息通过编码（ASCII， UTF-）等，转换成二进制后，存储在文件中，通常扩展名为.txt  .py ， 通常对人类来说可读
# 2,二进制文件 ： 图片，视频等 。 通常不是为人类阅读而设计的

# # # 操作文件的基础操作
# 路径可以右键文件名，copy path 获取绝对路径
# 其他盘的文件，点击那个文件，プロパティ　、上面的 セキュリティ　最上边的那行就是绝对路径

# 绝对路径优点，不受当前工作的位置影响
# 缺点： 如果移动文件，会导致路径失效，找不到，可维护性差
# f = open(r"D:\StudyPy\py_practice\SelfStudy\basics\ba20_2_targetFile.txt")
# # 直接复制会导致转义，前面加个 r ，取消转义，避免发生这种情况
# print(f)
# print(f.read())
# f.close()

# 相对路径 当前文件所在的根目录开始获取
# # SelfStudy\basics\ba20_1_SaveFile.py
# f = open(r".\ba20_2_targetFile.txt")  # 当前目录下的ba20文件
# # ..\ba20_2_  # 上一级目录下的ba20 文件
# # ..\..\ba20   # 上一级的上一级的ba20文件

# # 相对路径优点 ： 即使名字发生更改也没事
# # 缺点： 依赖当前工作目录，如果改变了工作目录就会导致路径失效
# # 应用场景，访问内部文件时
# print(f.read())
# # 打开文件必须要关闭文件，否则会导致因为文件被打开占用，导致报错
# f.close()

# # # 文件对象的常用属性
# file.name : 返回文件对象的名称(相对路径/绝对路径)
# file.mode ： 返回文件的访问状态

# f = open(r".\ba20_2_targetFile.txt")
# print(f.name)
# print(f.mode)  # r: 只能读，访问模式
# print(f.closed)  # 检测文件的关闭状态  打开中：false
# print(f.encoding)
# f.close()
# print(f.closed)  # 检测文件的关闭状态  打开中：false 已关闭： true

# # # 文件的读写操作
# # 文件的读取操作

# f = open(r".\ba20_2_targetFile.txt")
# print(f.read(-1))  # 括号内可以指定读取的字符的数量，负数也是读取全部
# # 使用read方法读取文件时，会将文件所有内容全部加载到内存中，非常大的文件的读取会给内存带来压力，处理大文件时使用readline 方法
# print(f.readline())  # 一次读取一行，超过会返回空值，不会报错
# print(f.readline())
# print(f.readline())

# # 通常不会使用for循环来数代码的行数，使用死循环，如果返回的值是空值则结束循环
# while 1:
#     text = f.readline()
#     if text == "":  # 如果text是空字符
#         break
#     print(text, end="")
# f.close()

# f.readlines() 把逐行获取到的字符串，保存成列表
# 如果文件很大的话，也会消耗很多内存，因为他需要将整个文件内容都加载到内存中
# f = open(r".\ba20_2_targetFile.txt")
# for i in f.readlines():
#     print(i, end="")
# print(f.readlines())
# f.close()

# # 文件的写入操作
# f = open(r".\ba20_2_targetFile.txt") # 文件默认 "r" ，只读模式，文件必须存在，否则报错，只能读，不能写
# f = open(r".\ba20_2_targetFile.txt", "w")  # "w" 如果文件不存在则新建，存在则覆盖，只能写，不能读
# # fmt: off
# f = open( r".\ba20_2_targetFile.txt", "a")  # "a" , 如果文件不存在则新建，存在则追加到文件末尾,只能写，不能读
# # fmt: on
# print(f.mode)
# try:
#     f.write("123")
# finally:
#     f.close()
#     print(f.closed)

# # 在 r，w，a 后面添加 "+" , 读写模式。使用加号会影响文件的读写效率，开发中通常只读，只写
f = open(r".\ba20_2_targetFile.txt", "a+")
# print(f.read())
# 读取到的内容为空 --> 因为文件的指针在内容最末尾，从最末尾读取文件，所以为空。a表示从文件末尾添加，所以指针在末尾
# 文件定位操作
# print(f.tell())  # tell（） 返回指针的当前位置
# seek(offset, whence)  # 移动指针到指定位置，offset是偏移量，表示要移动的字节数。
#   whence ， 用于指定offset的其实位置，默认是0，文件的起始位置。 1 表示当前位置为参考位置。 2 表示文件末尾作为参考位置
# f.seek(0, 0)  # 移动到最开头，读取全部内容
# f.seek(0)  # 移动到最开头，读取全部内容, 后面的默认值为0，简写
# f.seek(6, 0)  # 偏移6，从第7开始读
# print(f.read())
# f.close()

# 简化方法，自动关闭
# with语句
# with open(r".\ba20_2_targetFile.txt") as f:
#     print(f.read())

# 处理图片，视频等文件时  ， 必须要加 "b" 来声明，比如 "rb" , "wb"
# # 备份图片，--> 先读取文件，然后写入别的文件
# with open(
#     "D:\StudyPy\py_practice\SelfStudy\spider\studyWithHarry\picture.png", "rb"
# ) as f:
#     img_data = f.read()
#     print(img_data)

# with open("img_copy.png", "wb") as f:
#     f.write(img_data)

# # python进行文件操作，重命名 删除 ， 需要借助 import os
import os

# # 使用rename，可以重命名，还可以移动文件，括号中放入路径
# os.rename("img_copy.png", "img01.jpg")
# os.rename(r".\basics", "basics_new")  # 输入路径来更换位置
# 文件目录必须存在，不然报错
# 不支持跨盘操作，C盘到D盘之类的
# 操作不可逆
# 通过代码删除的，无法通过回收站回复

# os.mkdir("create")
# # 创建的文件夹必须不存在，否则报错
# print("文件已创建")
# os.rmdir("create")
# # os.rmdir("create") # 如果要删除的目录不存在，会报错
# print("文件已删除")
# # 删除目录只能删除空文件夹。如果文件夹中有文件会报错，需要先删除文件夹中的文件
# # 删除不可逆

# 获取当前文件的路径
# print(os.getcwd())  # 绝对路径

# # 获取目录列表
# print(os.listdir())  # 获取当前文件所在的文件夹的所有项目
# print(len(os.listdir()))
# print(os.listdir(r"D:\StudyPy\py_practice\SelfStudy"))  # 获取selfstudy之下的所有项目

# 检验路径是否存在 os.path.exists(要检查的路径)
print(os.path.exists("D:\StudyPy\py_practice"))
# true 表示存在， false 表示不存在

# 检验路径是否存在并且是文件
print(os.path.isfile("D:\StudyPy\py_practice"))  # 路径存在，但不是文件，返回false
print(
    os.path.isfile(r"D:\StudyPy\py_practice\SelfStudy\basics/ba20_1_SaveFile.py")
)  # 路径存在，并且是文件，返回true

# 检验是否存在并且是文件夹 os.path.isdir()
