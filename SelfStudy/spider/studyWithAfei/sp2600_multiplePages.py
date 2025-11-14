"""
访问多个页面的方法

"""

from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    # page = browser.new_page()
    # page.goto("https://www.baidu.com")
    # page1 = browser.new_page()
    # page1.goto("https://www.sina.com.cn")
    # # 可以发现两个page是独立的，在不同的窗口

    # 在同一个浏览器窗口中，打开多个标签页 # 创建一个浏览器上下文，通过上下文创建页面，可以实现多标签页的管理
    context = browser.new_context()
    # page1 = context.new_page()
    # page1.goto("https://www.baidu.com")

    # page1.wait_for_timeout(3000)

    # page2 = context.new_page()
    # page2.goto("https://mt-m.maoyan.com/asgard/board/4")

    # 切换页面 ，创建新页面后自动跳转到第二页，切换回原来页面的方法
    # page1.bring_to_front()  # 切换，激活到前台

    # 点击链接打开的新页面
    page1 = context.new_page()
    page1.goto("https://www.baidu.com")
    page1.wait_for_timeout(2000)
    a = page1.locator("#s-top-left >a:nth-child(1)")
    a.click()
    page1.wait_for_timeout(1000)
    # # 新打开的页面没有设定不叫page2,无法通过该方法切换回来
    page1.bring_to_front()
    page1.wait_for_timeout(5000)

    # 获取context创建的所有page页
    pages = context.pages
    print(pages)
    pages[1].bring_to_front()

    page1.wait_for_timeout(30323400)
