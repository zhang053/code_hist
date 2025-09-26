# encode
# st = "hello"
# st_en = st.encode()
# print(st_en, type(st_en))

st2 = "こんにちは"
st2_en = st2.encode()
# print(st2_en, type(st2_en))

# decode
# print(b"\xe3\x81\x93\xe3\x82\x93\xe3\x81\xab\xe3\x81\xa1\xe3\x81\xaf".decode())

# string[index]的正数时为从左往右，负数时从右往左。0是最开始第一个
# string = "asdfjlhdgsajk"
# print(string[4])
# # seq[start:stop:step]
# 省略start默认从开头，start包含最开始的值
# 省略stop默认到结尾,stop不包含指定的最后一个值
# 省略step默认步长为1，负数时从右往左切取

# print(string[2::2])
# print(string[:100:3])

# str3 = "いらっしゃいませ"
# print(str3[0:1])
# print(str3[:4])
# print(str3[:100:2])
# print(str3[::-2])

# # 步长和切取的方向需要一致
# print(str3[-2:-8:-1])

# 寻找 .find .index
# 区别是，find没找到返回-1，index没找到会报错
# find(index)["找寻目标",start,end]
str4 = input("text:")
# print(str4.find("f"))

# 统计目标字符串出现的次数 .count
# 没出现过，不存在的返回0
# print(str4.count("f"))
print(str4.count("f", 3))

# 修改元素
# replace(old,new,count修改次数)如果没有设置count的话，会进行到底
# if str4.find("1", 1):
#     print(str4.replace("1", "i", 1))
# else:
#     print("is no '1'")

# 分隔符 .split(sep,{maxsplit}) 分割几个
# str5 = "he\nllo wor ld"
# print(str5.split())  # 如果什么都不指定，默认以空格或者\n,\t等空白字符来分隔
# print(str5.split("\n"))  # 指定\n为分割符

# 去除左右两边的字符 .strip
# str5 = "xxyyxxhello x worl xy dxxxxxyyxyxyx"
# print(str5.strip("x"))  # 默认去除空格，只去除首尾，不管中间的内容
# print(str5.strip("xy"))  # 去除首尾的x和y

# 将字符串中的所有大写换层小写 .lower 小写换成大写upper
str6 = "HEllO WoRLd,你好"  # 非字母不受影响
# print(str6.upper())

# 判断是否为开头 .starswith() 是否为结尾 .endswith()
# print(str6.startswith("HE"))
# print(str6.endswith("好"))
# print(str6.endswith("D"))
# print(str6.startswith("l", 2, 5))  # 判断下标2的位置是否为是以目标字符开始

# 判断字符串中是否全部都是大写 .isupper 判断是否全部小写 .islower
# str7 = "ni hAo"  # 没有字母字符返回false
# print(str7.isupper())
# print(str7.islower())

# if str7.islower():
#     print(str7.upper())
# else:
#     print(str7.lower())

# # 对齐
# print(f'{"python":^<10} hello')  # 向左对齐，<,中间用^来填充
# print(f'{"js":+>10}')  # 向右对齐  >  ，中间用 + 填充，
# print(f'{"c#":+^12}')  # 居中对齐  ^  ，中间用 + 填充
