"""
多进程，适合计算密集型任务
"""

# 使用多进程，求阶乘

import random
import time
from multiprocessing import Pool
import os

# 随机生成一个数组
nums = [random.randint(1, 1000) for i in range(100000)]
# print(nums)


def factorial(n):
    result = 1
    for i in range(1, n + 1):
        result *= i
    return result


if __name__ == "__main__":
    # # 普通的单进程版本
    t0 = time.time()
    for n in nums:
        factorial(n)
    t1 = time.time()
    print(f"普通版本耗时：{t1 - t0:.2f}秒")

    # 多进程版本
    # cpu_count = os.cpu_count()
    # print(f"CPU核心数：{cpu_count}")
    t0 = time.time()
    with Pool(8) as p:
        p.map(factorial, nums)
    t1 = time.time()
    print(f"多进程版本耗时：{t1 - t0:.2f}秒")
