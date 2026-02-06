# https://www.spolicy.com/
from playwright.sync_api import sync_playwright
from openpyxl import Workbook


class BigData:
    def __init__(self):
        self.url = "https://www.spolicy.com/"
        self.page = None

    # 清理特殊空白符
    def clean(self, text: str) -> str:
        if not text:
            return ""
        return (
            text.replace("\u2003", " ")
            .replace("\u2002", " ")
            .replace("\u2001", " ")
            .strip()
        )

    # 搜索
    def search(self, search_content: str):
        # 搜索框
        input_button = self.page.locator("input.q-field__native").first
        input_button.fill(search_content)

        # 搜索按钮
        search_button = self.page.locator(
            "#app > div > div > main > div.relative-position.h-650px > "
            "div.absolute.absolute-full.custom-header.custom-header > div > "
            "div.flex.items-center.h-70px.input-wrapper > "
            "div.flex.items-center.h-full.bg-white.flex-1.pl-7.py-5px.pr-5px > "
            "button > span.q-btn__content.text-center.col.items-center.q-anchor--skip.justify-center.row"
        )
        search_button.click()

        # 等搜索结果出来
        self.page.wait_for_timeout(3000)

        # 点击加载更多
        load_btn = self.page.wait_for_selector(
            "div.q-page-container > main > div.items-start > div.pt-1 > button"
        )
        load_btn.click()

        # 等“加载更多”
        self.page.wait_for_load_state("networkidle")
        self.page.wait_for_timeout(3000)
        print("第一页加载完成")

    # 解析当前页的所有结果
    def parse_current_page(self):
        data = []

        results_panel = self.page.locator("main div.bg-white.card-shadow.pb-10").first
        items = results_panel.locator("a.policy-item.mb-5.block")

        count = items.count()
        print("本页实际条目数:", count)

        for i in range(count):
            a = items.nth(i)

            # 标题
            title = self.clean(a.locator(".policy-title").inner_text())

            # 内容
            content = self.clean(a.locator(".policy-content").inner_text())

            # 同一条记录的“发布网站 / 技术领域 / 发布时间”
            row = a.locator("xpath=..")  # 父级 py-5 容器
            info_div = row.locator("div.text-xs.leading-15px").first
            spans = info_div.locator("span")

            site = self.clean(spans.nth(0).inner_text())
            field = self.clean(spans.nth(1).inner_text())
            pub_time = self.clean(spans.nth(2).inner_text())

            item = {
                "title": title,
                "content": content,
                "site": site,
                "field": field,
                "pub_time": pub_time,
            }
            data.append(item)

            print(f"=== 本页第 {i + 1} 条 ===")
            # print(item)

        return data

    # 通过分页输入框跳转到指定页
    def goto_page(self, page_num: int):
        # 页码输入框点击并输入
        input_box = self.page.locator("input.q-field__native.text-center").first
        input_box.click()
        input_box.fill(str(page_num))
        self.page.keyboard.press("Enter")

        # 等待加载
        results_panel = self.page.locator("main div.bg-white.card-shadow.pb-10").first
        items = results_panel.locator("a.policy-item.mb-5.block")

        # 等至少出现一条内容
        items.first.wait_for(state="visible", timeout=15000)

        # 等待网络加载
        self.page.wait_for_load_state("networkidle")

        print(f"已跳转第 {page_num} 页")

    # 翻页 收集数据 保存成 xlsx
    def run(self, search_content: str, max_pages: int = 10):
        with sync_playwright() as p:
            # 浏览器位置
            browser = p.chromium.launch_persistent_context(
                executable_path=r"C:\Program Files\Google\Chrome\Application\chrome.exe",
                user_data_dir=r"4.3_userData",
                headless=False,
            )
            self.page = browser.new_page()
            self.page.goto(self.url)
            self.page.wait_for_timeout(6000)

            print("开始搜索")
            # 先搜索并加载第一页
            self.search(search_content)

            all_data = []

            for page_num in range(1, max_pages + 1):
                print("\n" + "=" * 25 + f" 第 {page_num} 页 " + "=" * 25)

                if page_num > 1:
                    self.goto_page(page_num)

                page_data = self.parse_current_page()
                all_data.extend(page_data)

            # 保存到 xlsx
            filename = f"4.3_BigData_result.xlsx"
            self.save_to_xlsx(all_data, filename)
            print(f"已保存 {len(all_data)} 条数据到: {filename}")

            self.page.wait_for_timeout(10000)

    # 保存为 xlsx
    def save_to_xlsx(self, data, filename: str):
        wb = Workbook()
        ws = wb.active
        ws.title = "data"

        # 表头
        ws.append(["标题", "内容", "发布网站", "技术领域", "发布时间"])

        for item in data:
            ws.append(
                [
                    item["title"],
                    item["content"],
                    item["site"],
                    item["field"],
                    item["pub_time"],
                ]
            )

        wb.save(filename)


if __name__ == "__main__":
    bd = BigData()
    # 抓“区块链”相关的前 10 页
    bd.run("区块链", max_pages=10)
