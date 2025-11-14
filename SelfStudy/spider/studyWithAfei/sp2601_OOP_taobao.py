"""
淘宝搜索内容需要登录

# 如果有相对复杂的登录场景，需要手动介入

playwright 两次运行间, 没有保存cookie的概念

    维持登录状态, 需要手动输入
    登录有cookie, 复制下来后
"""

from playwright.sync_api import sync_playwright
import os


class Taobao:
    def __init__(self):
        self.page = None
        self.browser = None
        self.context = None
        self.login_file = "sp2602_temp_login.json"

    # 对手动登录和自动登录进行处理
    def login(self):
        # 如果有"sp2602_temp_login.json"，则使用保存的文件 --> 自动登录 , 没有就手动登录
        if os.path.exists(self.login_file):
            print("运行 自动 登录")
            self.auto_login()
        else:
            print("运行 手动 登录")
            self.context = self.browser.new_context()
            self.page = self.context.new_page()
            self.page.goto("https://www.taobao.com")
            self.manual_login()
        # 登录信息进行存储, 自动登录也使用这段代码，用于更新cookie
        self.page.context.storage_state(path=self.login_file)
        print("登录信息保存成功")

    # 手动登录 获取登录状态的信息
    def manual_login(self):
        # 获取html的标签进行登录
        # fmt: off
        login_button = self.page.locator("#J_SiteNavLogin > div.site-nav-menu-hd > div.site-nav-sign > a.h")
        # fmt: on
        login_button.click()
        # 手动介入
        input("登录完成后输入回车 继续...")

    # 自动登录
    def auto_login(self):
        # 调用保存的登录信息的json文件
        self.context = self.browser.new_context(storage_state=self.login_file)
        self.page = self.context.new_page()
        self.page.goto("https://www.taobao.com")

        # 检测是否真的登录成功
        # 检测条件: 登录的标签的class会发生改变
        try:
            self.page.wait_for_selector(
                "#J_SiteNavLogin > div.site-nav-menu-hd > div.site-nav-user > a",
                timeout=6000,
            )
            print("登录成功")
        except:
            print("登录失败，请手动登录")
            self.manual_login()

    def search(self, search):
        ele_input = self.page.locator("#q")
        ele_input.fill(search)
        self.page.keyboard.press("Enter")
        self.page.wait_for_timeout(3000)  # 搜索延迟

    def get_goods_info(self):
        # 搜索后会开新页，找到新标签页
        page2 = self.context.pages[1]
        # print(page2)
        # 获取所有商品的父级
        page2.wait_for_load_state("load")
        goods_list = page2.locator("#content_items_wrapper > div > a")
        # print(goods_list.count())
        # 遍历，获取需要的商品信息
        for good in goods_list.all():
            title = good.locator("div.title--ASSt27UY").get_attribute("title")
            print("标题:", title)
            price = good.locator("div.priceInt--yqqZMJ5a").text_content()
            print("价格：", price)
            # 如果有销量，就获取
            try:
                sales = good.locator("span.realSales--XZJiepmt")
                sales.wait_for(timeout=2000)
                sales = sales.text_content()
            except:
                sales = "暂无信息"
            print("销量：", sales)
            shopName = good.locator("span.shopNameText--DmtlsDKm").text_content()
            print("店铺：", shopName)
            print("-" * 50)

    def run(self, search):
        with sync_playwright() as p:
            self.browser = p.chromium.launch(headless=False)
            # context = browser.new_context()
            # self.page = context.new_page()
            # self.page.goto("https://www.taobao.com")
            # self.page.wait_for_timeout(1000)
            # # 手动登录获取登录信息后，自动登录
            self.login()
            # 登录后进行搜索
            self.search(search)
            self.get_goods_info()

            self.page.wait_for_timeout(3402873)


if __name__ == "__main__":
    tb = Taobao()
    tb.run("头戴式耳机")
