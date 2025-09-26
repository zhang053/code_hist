# # #  1.总和
sum = 0
for i in range(2, 101, 2):
    sum += i
print(f"总和：{sum}")
print("\n")

# # #  2.倒序99乘法表
for m in range(9, 1, -1):
    for n in range(m, 0, -1):
        print(f"{m}*{n}={m*n}", end=" ")
    print("")
print("\n")

# # #  3.替换
s = "hello world , hello python"
ind = s.find("hello")
s = s.replace("hello", "hi")
print(f"hello第一次出现在下标为 {ind} 的位置,替换后的字符串为：{s}")
print("\n")

# # #  4.找最长单词
string1 = "python is a powerful programming language"
string1_sp = string1.split()  # 把句子分割成一个一个的单词
length = len(string1_sp)  # length 表示有多少个单词
longest = len(string1_sp[0])
for i in string1_sp:  # i= python , is , .....
    if len(i) > longest:
        # 如果当前这个单词长度大于一开始假定的longest的话，当前单词长度则为longest
        longest = len(i)
        longest_word = i  # 保存最长的单词
print(f"输出：{longest_word} 长度：{longest}")
print("\n")

# # #  5.列表操作
fruits = ["apple", "banana", "cherry", "date", "elderberry", "fig", "grape"]
# 5.1 切片2到5
print(fruits[2:5])
# 5.2 切片最后三个元素
print(fruits[-3::1])
# 5.3 遍历列表，打印长度
for i in fruits:
    print(f"元素：{i} 的长度为 {len(i)}")
# 5.4 转为大写后存入新列表
new_fruits = []
for i in range(len(fruits)):
    new_fruits.append(fruits[i].upper())
print(new_fruits)

# # #  6.推导式
# 6.1 1~20偶数
print([i for i in range(0, 21, 2)])

# 6.2 每个元素首字母
words = ["apple", "banana", "cherry", "date"]
print([i[0] for i in words])

# 6.3 整除3的数字
nums = [12, 35, 87, 26, 9, 42, 56]
print([i for i in nums if i % 3 == 0])

# # #  7.计算二维元组
matrix = ((1, 2, 3), (4, 5, 6), (7, 8, 9))
sum = 0
for i in range(len(matrix)):
    sub_sum = 0
    for m in range(len(matrix[i])):
        sub_sum += matrix[i][m]
    sum += sub_sum
print(f"该二维元组的总和是：{sum}")

# # #  7.找出所有a
t = ("a", "b", "c", "a", "d", "a", "e")
for i in range(len(t)):
    if t[i] == "a":
        print(i)
