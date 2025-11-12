"""
playwright 相关知识补充
    多个中选一个子元素的方法
    获取元素位置的方法
        html中元素的位置
            xy坐标, 浏览器左上角, 网址还有收藏栏的下方的位置是原点
            原点往右是 x+
            原点往下是 y+
    ---> 用处，获取位置后进行截图

"""

from playwright.sync_api import sync_playwright


with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    # page.set_viewport_size({"width": 1080, "height": 500})
    page.goto("https://www.baidu.com")

    # # 选择想要获取的元素的方法
    # # titles = page.locator(".title-content-title").first # 第一个
    # titles = page.locator(".title-content-title").last  # 最后一个
    # titles = page.locator(".title-content-title").nth(3)  # 从0开始计数
    # print(titles.inner_text())

    # 获得元素在页面中的坐标
    hotsearch = page.locator("#s-hotsearch-wrapper")
    print("元素位置: ", hotsearch.bounding_box())
    # {'x': 226, 'y': 370, 'width': 798, 'height': 258}
    # 获得位置后进行截图
    # page.screenshot(path="sp2501_temp_ScShot.png")  # 整页截图

    from playwright.sync_api import FloatRect

    # page.screenshot(
    #     path="sp2501_temp_ScShot.png", clip=FloatRect(x=0, y=0, width=500, height=300)
    # )
    page.screenshot(
        path="sp2501_temp_ScShot.png",
        clip={"x": 226, "y": 370, "width": 798, "height": 258},
    )
    page.wait_for_timeout(500000)
