"""
playwright 相关课件存放位置
"D:\StudyPy\py_practice\SelfStudy\playwright课件"

# # # 安装playwright
pip install playwright

# 检查是否安装成功  playwright --version

## 安装浏览器依赖  playwright install

# playwright的优势
    有些request发的请求会被拦住

# 有加密内容时
    通过request发送的,只能获取源码就是加密前的,需要js逆向,pw不需要
    正常拿不到渲染之后的内容, pw是浏览器所以可以拿到



"""

import time

# 第一个playwright案例
from playwright.sync_api import sync_playwright

# fmt: off
# 使用with创建playwright -- 不需要手动关闭
with sync_playwright() as p:
    # 创建浏览器对象
    browser = p.chromium.launch(headless=False)  # headless 默认时true ； false：代码运行, 不显示浏览器， true：显示浏览器
    # fmt: on
    # 创建标签页
    page = browser.new_page()
    # 修改页面大小
    page.set_viewport_size({"width":1080,"height":720})
    # 访问网址
    page.goto("https://www.baidu.com")
    
    # with 会自动管理p对象, 没有需要运行的逻辑后进行关闭
    # time.sleep(500)
    # playwright中专门的等待方法
    page.wait_for_timeout(5000)
