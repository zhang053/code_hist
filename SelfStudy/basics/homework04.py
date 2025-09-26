# 1
li = ["a", "b", "c"]
dic = dict()
for i in li:
    dic[i] = i.upper()
print(dic)

# 2
st = "Hello World"
st = st.replace(" ", "")
st = list(st)
dic2 = dict()
for char in st:
    if char in dic2:
        dic2[char] += 1
    else:
        dic2[char] = 1
print(dic2)

# 3
s = set()
s.add("apple")
s.add("banana")
s.add("cherry")
s.remove("banana")
if "apple" in s:
    print(s)

# 4
li2 = [2, 4, 2, 6, 8, 4, 10, 6]
li3 = []
s2 = set()
for i in li2:
    if i % 2 == 0:
        s2.add(i)
    else:
        li3.append(i)
li3.extend(s2)
print(li3)

# 5
dic3 = dict()
# test
# dic3 = dict(a=1, b=1, c=4, d=1)
sum = 0
for i in dic3.values():
    sum += i
print(sum)

# 6
total = 0


def add(num):
    global total
    total += num


def subtract(num):
    global total
    total -= num


def get_total():
    return total


n = 5
add(n)
add(n)
subtract(n)
print(get_total())


# 7
def jiecheng(n):
    result = 1
    print(f"{n}的阶乘: ", end="")
    for i in range(1, n + 1):
        result *= i
        if i < n:
            print(i, end="*")
        else:
            print(i)
    return result


print(jiecheng(3))


# 8
def text_processor(text, option):
    if option == "uppercase":
        return text.upper()
    elif option == "lowercase":
        return text.lower()
    elif option == "word_count":
        return text.count(" ") + 1
    else:
        return text


print(text_processor("hello world daf daf daer", "word_count"))
