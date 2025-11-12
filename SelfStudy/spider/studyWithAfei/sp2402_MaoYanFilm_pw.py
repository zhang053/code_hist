"""
https://mt-m.maoyan.com/asgard/board/4
获取猫眼电影的 猫眼经典top100


"""

from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    page.goto("https://mt-m.maoyan.com/asgard/board/4")
    page.set_viewport_size({"width": 1080, "height": 500})

    # 有时候获取的顺序不同可能导致内容还没渲染完成就开始寻找，导致找不到
    # 等待元素渲染成功后，再去获取
    page.wait_for_selector(".board-card")

    # 获取所有父级
    ele_borads = page.locator(".board-card")
    for board in ele_borads.all():
        # 获取电影标题
        ele_name = board.locator("h3.title")
        print("电影名：", ele_name.text_content())
        # 获取电影主演
        ele_actor = board.locator(".actors")
        print("主演：", ele_actor.text_content())
        # 获取上映时间
        ele_date = board.locator(".date")
        print("上映时间：", ele_date.text_content())
        # 获取评分
        ele_num = board.locator(".number")
        print("评分：", ele_num.text_content())
        # 获取猫眼地址
        ele_link = board.locator("a.link-holder")
        print("猫眼地址：", ele_link.get_attribute("href"))

        print("=" * 50)

    page.wait_for_timeout(5000000)
