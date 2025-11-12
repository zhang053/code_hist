"""
如何通过playwright进行鼠标操作
    支持鼠标案件: 左键 滚轮 右键
"""

from playwright.sync_api import sync_playwright


with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    # page.set_viewport_size({"width": 1080, "height": 500})
    page.goto("https://baidu.com")

    # 使用鼠标的场景
    # 鼠标左键点击 xxxx.click() 获取某个元素后进行左键点击
    # 指定位置点击
    # page.mouse.click(100, 31)
    # page.mouse.click(160, 31, button="right")  # 右键点击，默认左键
    # page.mouse.click(100, 31, button="middle")  # 按下滚轮
    # page.mouse.dblclick(100,31) # 双击

    # # 鼠标 按下 移动 抬起  --> .down()  .move()  .up()  拖拽功能
    # # 移动鼠标到指定位置，然后按下，然后移动，然后抬起
    # page.mouse.move(100, 100)
    # page.mouse.down()
    # page.mouse.move(x=1100, y=700)
    # page.mouse.up()
    # page.wait_for_timeout(2000)
    # page.mouse.down()

    # # 鼠标滚动操作
    # 用处： 请求瀑布流的时候
    # page.mouse.wheel(0, 100)
    # page.wait_for_timeout(1000)
    # page.mouse.wheel(0, 200)
    # page.wait_for_timeout(1000)
    # page.mouse.wheel(0, 300)
    # page.wait_for_timeout(1000)
    # page.mouse.wheel(0, 400)
    # page.wait_for_timeout(1000)
    # # 有过程的滚动,匀速
    # top = 0
    # while 1:
    #     top += 10
    #     # wheel 的参数控制的是单次的滚动距离，不是页面的距离
    #     page.mouse.wheel(0, 10)
    #     page.wait_for_timeout(30)
    #     if top >= 1000:
    #         break

    # playwright可以执行js代码，
    # js代码可以获取整个页面的高度 # document.body.scrollHeight
    # max_height = page.evaluate("()=>document.body.scrollHeight")  # js代码执行方法
    # print(max_height)  # 获取整个页面的高度后，匀速滑动到底部
    # top = 0
    # while 1:
    #     top += 30
    #     # wheel 的参数控制的是单次的滚动距离，不是页面的距离
    #     page.mouse.wheel(0, 30)
    #     page.wait_for_timeout(30)
    #     print("页面总高度：", max_height)
    #     print("当前高度：", page.evaluate("()=>window.scrollY"))
    #     if top >= max_height:
    #         break

    # 键盘输入
    # page.keyboard.type("abc mart")
    # page.wait_for_timeout(1000)
    # # 按键输入内容
    # page.keyboard.press(" ")
    # page.keyboard.press("a")
    # page.keyboard.press("b")
    # page.keyboard.press("Enter")  # press是瞬间的行为，只点击一次
    # # 按下抬起
    page.keyboard.down("w")
    page.wait_for_timeout(1000)
    page.keyboard.up("w")  # 长按一秒后抬起

    page.wait_for_timeout(659989)
