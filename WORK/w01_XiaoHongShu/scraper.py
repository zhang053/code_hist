from playwright.sync_api import sync_playwright
import re


class XiaoHongShu:
    def __init__(self):
        self.url = "https://www.xiaohongshu.com/search_result/?keyword=%25E8%258B%25B1%25E8%25AF%25AD%25E5%25AD%25A6%25E4%25B9%25A0%25E6%259C%25BA&source=web_search_result_notes&type=51"

        self.ITEM_SEL = "section.note-item"
        self.END_SEL = "div.search-layout__main div.end-container"

    # ---------- 标题容错提取 ----------
    def pick_title(self, item):
        candidates = [
            ":scope div.footer a.title > span",
            ":scope a.title span",
            ":scope > div > div > a > span",
            ":scope a span",
        ]
        for sel in candidates:
            loc = item.locator(sel)
            if loc.count() > 0:
                t = (loc.first.text_content() or "").strip()
                if t:
                    return t
        return ""

    # ---------- 采集当前已加载卡片 ----------

    def collect_by_index(self, page, seen_index: set[int], rows: dict[int, dict]):
        items = page.locator("section.note-item")
        for i in range(items.count()):
            it = items.nth(i)

            idx_str = it.get_attribute("data-index")
            if not idx_str or not idx_str.isdigit():
                continue
            idx = int(idx_str)

            if idx in seen_index:
                continue

            # 1) href：优先隐藏 explore（最稳）
            href = ""
            explore = it.locator('a[href^="/explore/"]').first
            if explore.count() > 0:
                h = explore.get_attribute("href") or ""
                if h.startswith("/"):
                    href = "https://www.xiaohongshu.com" + h

            # 2) 备胎：cover.mask（有些卡只有这个）
            if not href:
                cover = it.locator("a.cover.mask").first
                if cover.count() > 0:
                    h = cover.get_attribute("href") or ""
                    if h.startswith("/"):
                        href = "https://www.xiaohongshu.com" + h
                    else:
                        href = h

            # 3) title：按你截图结构优先
            title = ""
            tloc = it.locator(":scope div.footer a.title > span")
            if tloc.count() > 0:
                title = (tloc.first.text_content() or "").strip()

            # 4) 记录（即使 title/href 为空也记录，避免漏 index）
            rows[idx] = {"index": idx, "href": href, "title": title}
            seen_index.add(idx)

    # ---------- 平滑滚动 ----------
    def smooth_scroll(self, page):
        for _ in range(2):
            page.mouse.wheel(0, 600)
            page.wait_for_timeout(300)

    # ---------- 主逻辑 ----------
    def run(self):
        with sync_playwright() as p:
            context = p.chromium.launch_persistent_context(
                executable_path=r"C:\Program Files\Google\Chrome\Application\chrome.exe",
                user_data_dir=r"./userData",
                headless=False,
                slow_mo=30,
            )

            page = context.new_page()
            page.goto(self.url, wait_until="domcontentloaded")

            # 登录处理
            try:
                page.wait_for_selector(self.ITEM_SEL, timeout=10000)
            except:
                input("请先登录，然后按回车继续...")
                page.wait_for_selector(self.ITEM_SEL, timeout=30000)

            seen_href = set()
            all_rows = []
            idle = 0

            seen_index = set()
            rows = {}  # idx -> {index, href, title}

            idle = 0
            MAX_IDLE = 12  # 可以略大一点

            while True:
                end_visible = (
                    page.locator(self.END_SEL).count() > 0
                    and page.locator(self.END_SEL).is_visible()
                )
                if end_visible:
                    page.wait_for_timeout(1200)  # 尾部缓冲

                before = len(seen_index)
                self.collect_by_index(page, seen_index, rows)
                after = len(seen_index)

                if after > before:
                    idle = 0
                    print("新增", after - before, "累计", after)
                else:
                    idle += 1
                    print("无新增 idle=", idle)

                # 到底 + 多轮无新增才停
                if end_visible and idle >= 4:
                    print("THE END + 稳定无新增，结束")
                    break
                if idle >= MAX_IDLE:
                    print("兜底结束")
                    break

                # 小步滚动更稳
                for _ in range(2):
                    page.mouse.wheel(0, 600)
                    page.wait_for_timeout(300)
                page.wait_for_timeout(800)
            max_idx = max(rows.keys()) if rows else -1
            missing = [i for i in range(max_idx + 1) if i not in rows]

            print("\n==== 抓取结果 ====")

            print("max_idx =", max_idx)
            print("抓到 =", len(rows))
            print("缺失 index 数 =", len(missing))
            print("缺失 index 列表 =", missing[:50], "..." if len(missing) > 50 else "")
            for i, (_, title) in enumerate(all_rows, 1):
                print(i, title)
            print("\n==== 标题列表（按 index 顺序）====")
            for idx in sorted(rows.keys()):
                title = rows[idx]["title"]
                print(idx, title)

            input("\n浏览器保持开启用于调试，按回车退出程序...\n")


if __name__ == "__main__":
    XiaoHongShu().run()
