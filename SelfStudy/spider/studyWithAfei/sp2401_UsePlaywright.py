# 第一个playwright案例
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    page.set_viewport_size({"width": 1080, "height": 500})
    page.goto("https://www.baidu.com")

    # # 获得页面的标题
    # print(page.title())
    # # 获取页面的url
    # print(page.url)
    # # 获取页面的源代码
    # print(page.content())

    # # 获取页面的元素 -- xpath
    # ele_input = page.locator('//textarea[@id="chat-textarea"]')
    # # 给input输入框 输入内容
    # ele_input.fill("叶瞬光")  # 一次性输入内容
    # # 输入内容 # 模拟键盘一个一个字敲
    # # ele_input.type("ye shun guang")

    # # 搜索框输入内容，间隔三秒，点击
    # page.wait_for_timeout(3000)

    # # 获取搜索按钮 -- css 选择器
    # ele_button = page.locator("#chat-submit-button")
    # # 点击按钮
    # ele_button.click()

    ### 获取百度热搜的内容
    # 获取元素
    # element = page.locator(".title-content-title")
    # print(element.count())  # 获取元素个数
    # print(element.all_text_contents())  # 打印获取到的全部内容，放入列表
    # print(element.all_inner_texts())  # 获取可见元素的文本，有些元素可能是 隐藏的

    # 获取单个元素
    # div = page.locator('//*[@id="chat-input-extension"]/div/div/div[1]/a/div[1]')
    # print(div.text_content())

    # 获取标签属性 href
    ele_news = page.locator('//ul[@id="hotsearch-content-wrapper"]/li/a')
    print(ele_news.count())
    # 需要遍历获取多个值
    for a in ele_news.all():
        print(a.get_attribute("href"))  # 获取标签属性

    page.wait_for_timeout(5000000)
