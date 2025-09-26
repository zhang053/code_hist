# name = input("what's your name:")
# print("hi,", name)

num = 56
print(num + 100)

x = 1 - 1

# score = int(input("tell me your score:"))
if num >= 90:
    print("excellent!")
elif num >= 60:
    print("good")
else:
    print("need fighting")

i = 1
while i < 6:
    if i == 1:
        print("1 st")
    elif i == 2:
        print("2 nd")
    elif i == 3:
        print("3 rd")
    else:
        print(i, "th", sep="")
        print("i=", i, sep="1")
    i += 1
print("end")

for i in range(3, 19, 4):
    print("i =", i)
