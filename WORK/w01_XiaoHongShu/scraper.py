import json
import random
import re
import time
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple

from playwright.sync_api import sync_playwright, TimeoutError as PWTimeoutError


# ===================== 配置 =====================
SEARCH_URL = "https://www.xiaohongshu.com/search_result/?keyword=%25E8%258B%25B1%25E8%25AF%25AD%25E5%25AD%25A6%25E4%25B9%25A0%25E6%259C%25BA&source=web_search_result_notes&type=51"
CHROME_EXE = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
USER_DATA_DIR = r"./userData"

OUT_JSONL = "comments_click_dom.jsonl"

MAX_NOTES = 50  # 先跑小一点验证，OK后再改大
MAX_COMMENTS_PER_NOTE = 300  # 单条笔记最多保存多少条（含回复）
SCROLL_WHEEL = 700  # 搜索页滚动步长
# ==============================================


def rsleep(a: float, b: float, reason: str = ""):
    t = random.uniform(a, b)
    if reason:
        print(f"    [sleep] {t:.2f}s ({reason})")
    time.sleep(t)


def safe_text(x: Optional[str]) -> str:
    return (x or "").strip()


def prefix_url(href: str) -> str:
    href = safe_text(href)
    if not href:
        return ""
    if href.startswith("http"):
        return href
    if href.startswith("/"):
        return "https://www.xiaohongshu.com" + href
    return href


@dataclass
class NoteCard:
    index: int
    title: str


# --------------------- 1) 弹窗/浮层尽量关掉（降低闪动干扰） ---------------------


def try_dismiss_popups(page):
    """
    只尝试点击“明确的关闭按钮”
    不使用 ESC（ESC 会把卡片/详情关掉）
    """
    candidates = [
        "button[aria-label='关闭']",
        "button:has-text('关闭')",
        "button:has-text('我知道了')",
        "button:has-text('知道了')",
        "button:has-text('取消')",
        "div[role='dialog'] button",  # 弹窗里的按钮兜底
    ]

    for sel in candidates:
        try:
            loc = page.locator(sel)
            if loc.count() and loc.first.is_visible():
                loc.first.click(timeout=500)
                rsleep(0.15, 0.35, "dismiss popup")
        except Exception:
            pass


# --------------------- 2) 搜索页：点击卡片打开详情 ---------------------


def get_title_from_item(item) -> str:
    # 你之前定位标题的那个 span，本质就是 footer a.title span
    tloc = item.locator(":scope div.footer a.title > span")
    if tloc.count():
        return safe_text(tloc.first.text_content())
    return ""


def click_card_open_detail(page, item) -> bool:
    """
    按你的要求：不请求卡片链接，不用 goto(href)，而是“点击卡片/section”触发详情出现。
    实际点击用 a.cover.mask.ld 最稳（也算点击卡片）。
    """
    try_dismiss_popups(page)

    cover = item.locator("a.cover.mask.ld").first
    if cover.count() == 0:
        # 退一步：点整个 section
        try:
            item.click(timeout=1500)
            return True
        except Exception:
            return False

    try:
        cover.scroll_into_view_if_needed(timeout=3000)
    except Exception:
        pass

    try:
        cover.click(timeout=5000)
        return True
    except Exception:
        # 某些情况下覆盖层挡住，点 section 再试
        try:
            item.click(timeout=1500)
            return True
        except Exception:
            return False


def wait_comments_ready(page):
    """
    等到评论容器出现并稳定：
    - #noteContainer 存在
    - list-container 存在
    - parent-comment 有至少 1 条（或确实为 0，但容器加载出来）
    """
    page.wait_for_selector("#noteContainer", timeout=20000)
    page.wait_for_selector(
        "#noteContainer div.comments-el div.list-container", timeout=20000
    )

    # 稳定等待：parent-comment 数量连续两次一样就认为稳定
    lc = page.locator("#noteContainer div.comments-el div.list-container")
    pc = lc.locator(":scope div.parent-comment")

    last = -1
    stable = 0
    for _ in range(20):
        try_dismiss_popups(page)
        cnt = pc.count()
        if cnt == last:
            stable += 1
        else:
            stable = 0
            last = cnt
        if stable >= 2:
            break
        rsleep(0.2, 0.5, "wait comments stable")


def go_back_to_search(page):
    """
    点击卡片后通常会导航到详情路由；
    抓完后回到搜索结果页（尽量保持滚动位置）
    """
    try:
        page.go_back(wait_until="domcontentloaded", timeout=20000)
    except Exception:
        # 如果 go_back 不行，就直接回搜索页（会丢滚动位置，但能继续跑）
        page.goto(SEARCH_URL, wait_until="domcontentloaded", timeout=30000)
    rsleep(0.6, 1.2, "back to search")
    try_dismiss_popups(page)


# --------------------- 3) 评论DOM：顶层+回复+展开更多回复 ---------------------


def get_comment_id_from_node(node) -> str:
    """
    comment 节点 id 是 comment-xxxxxxxx
    """
    cid = safe_text(node.get_attribute("id"))
    if cid.startswith("comment-"):
        return cid[len("comment-") :]
    return cid


def extract_author_and_href(comment_node) -> Tuple[str, str]:
    # 你给的：div.right > div.author-wrapper > div.author > a
    a = comment_node.locator(":scope div.right div.author-wrapper div.author a").first
    name = safe_text(a.text_content()) if a.count() else ""
    href = prefix_url(a.get_attribute("href") if a.count() else "")
    return name, href


def extract_content(comment_node) -> str:
    # 你给的：div.right > div.content > span > span
    c = comment_node.locator(":scope div.right div.content span > span").first
    return safe_text(c.text_content()) if c.count() else ""


def extract_time_ip(comment_node) -> Tuple[str, str]:
    """
    你给的 selector 写成同一个了：span:nth-child(1)
    实际上一般是同一行多个 span：
      div.right > div.info > div.date > span (第1个=时间，第2个=IP属地 或 地区)
    这里按“抓所有 span，按位置推断”：
    """
    spans = comment_node.locator(":scope div.right div.info div.date span")
    texts = []
    for i in range(spans.count()):
        texts.append(safe_text(spans.nth(i).text_content()))

    # 兜底：从 texts 里找“IP属地”
    time_text = ""
    ip_text = ""

    if texts:
        # 常见：第一个是时间
        time_text = texts[0]

        # IP可能在后面，可能写成“IP属地：四川”或“IP属地 四川”
        for t in texts[1:]:
            if "IP" in t or "属地" in t:
                ip_text = t
                break
        # 如果没有明确IP字段，就把第二个当作 ip/地区（不少页面是“2025-..  四川”）
        if not ip_text and len(texts) >= 2:
            ip_text = texts[1]

    # 统一清洗：提取“IP属地：xxx”里的 xxx
    m = re.search(r"IP属地[:：]?\s*(.*)$", ip_text)
    if m:
        ip_text = m.group(1).strip()

    return time_text, ip_text


def click_show_more_within_parent(parent_node, max_clicks=30):
    """
    在一个 parent-comment 里，把所有 show-more 点到没有为止
    你给的：div.reply-container > div.show-more
    """
    for _ in range(max_clicks):
        btns = parent_node.locator(":scope div.reply-container div.show-more")
        clicked = False
        for i in range(btns.count()):
            b = btns.nth(i)
            try:
                if b.is_visible():
                    b.click(timeout=1500)
                    rsleep(0.2, 0.6, "click show-more")
                    clicked = True
            except Exception:
                continue
        if not clicked:
            break


def extract_comments_from_detail(page) -> List[dict]:
    """
    在详情页里：
    - 遍历每个 parent-comment
    - 先点完 show-more
    - 抓 parent comment
    - 再抓 sub comments（class=comment-item comment-item-sub）
    """
    lc = page.locator("#noteContainer div.comments-el div.list-container")
    parent_list = lc.locator(":scope div.parent-comment")
    results = []

    for i in range(parent_list.count()):
        parent = parent_list.nth(i)

        # parent 里顶层 comment 节点一般是 id^=comment-
        parent_comment_node = parent.locator(":scope [id^='comment-']").first
        if parent_comment_node.count() == 0:
            continue

        # 先展开所有回复
        click_show_more_within_parent(parent, max_clicks=40)

        # 采集顶层评论
        pid = get_comment_id_from_node(parent_comment_node)
        p_author, p_user_url = extract_author_and_href(parent_comment_node)
        p_content = extract_content(parent_comment_node)
        p_time, p_ip = extract_time_ip(parent_comment_node)

        results.append(
            {
                "level": "parent",
                "comment_id": pid,
                "author_name": p_author,
                "user_url": p_user_url,
                "content": p_content,
                "time": p_time,
                "ip_location": p_ip,
            }
        )

        # 采集回复评论（sub）
        sub_nodes = parent.locator(
            ":scope .comment-item.comment-item-sub[id^='comment-']"
        )
        for j in range(sub_nodes.count()):
            sub = sub_nodes.nth(j)
            sid = get_comment_id_from_node(sub)
            s_author, s_user_url = extract_author_and_href(sub)
            s_content = extract_content(sub)
            s_time, s_ip = extract_time_ip(sub)

            results.append(
                {
                    "level": "sub",
                    "parent_comment_id": pid,
                    "comment_id": sid,
                    "author_name": s_author,
                    "user_url": s_user_url,
                    "content": s_content,
                    "time": s_time,
                    "ip_location": s_ip,
                }
            )

        if len(results) >= MAX_COMMENTS_PER_NOTE:
            break

    return results


# --------------------- 4) 用户主页：抓小红书号（redId） ---------------------


def fetch_red_id(context, user_url: str, cache: Dict[str, str]) -> str:
    if not user_url:
        return ""
    if user_url in cache:
        return cache[user_url]

    p2 = context.new_page()
    red_id = ""
    try:
        p2.goto(user_url, wait_until="domcontentloaded", timeout=30000)
        # 你给的：span.user-redId
        loc = p2.locator("span.user-redId")
        loc.wait_for(timeout=15000)
        red_id = safe_text(loc.first.text_content())
        rsleep(0.5, 1.2, "open user profile")
    except Exception:
        red_id = ""
    finally:
        try:
            p2.close()
        except Exception:
            pass

    cache[user_url] = red_id
    return red_id


# --------------------- 5) 主程序 ---------------------


def main():
    with sync_playwright() as p:
        context = p.chromium.launch_persistent_context(
            executable_path=CHROME_EXE,
            user_data_dir=USER_DATA_DIR,
            headless=False,
        )

        page = context.new_page()
        page.goto(SEARCH_URL, wait_until="domcontentloaded", timeout=30000)

        # 登录处理
        try:
            page.wait_for_selector("section.note-item", timeout=12000)
        except PWTimeoutError:
            input("可能需要登录：请在浏览器完成登录后回车继续...")
            page.wait_for_selector("section.note-item", timeout=30000)

        try_dismiss_popups(page)

        processed_index = set()
        user_cache: Dict[str, str] = {}

        with open(OUT_JSONL, "w", encoding="utf-8") as f:
            note_count = 0

            while note_count < MAX_NOTES:
                items = page.locator("section.note-item")
                if items.count() == 0:
                    page.mouse.wheel(0, SCROLL_WHEEL)
                    rsleep(0.3, 0.7, "scroll search")
                    continue

                progressed = False

                for k in range(items.count()):
                    it = items.nth(k)
                    idx_str = safe_text(it.get_attribute("data-index"))
                    if not idx_str.isdigit():
                        continue
                    idx = int(idx_str)
                    if idx in processed_index:
                        continue

                    title = get_title_from_item(it)
                    print(
                        f"\n===== [{note_count+1}/{MAX_NOTES}] index={idx} title={title} ====="
                    )

                    ok = click_card_open_detail(page, it)
                    if not ok:
                        processed_index.add(idx)
                        continue

                    try:
                        wait_comments_ready(page)
                        rsleep(0.4, 0.9, "detail ready")

                        # 抓评论（顶层+回复）
                        rows = extract_comments_from_detail(page)

                        # 补充 redId + note信息
                        for r in rows:
                            red_id = (
                                fetch_red_id(context, r.get("user_url", ""), user_cache)
                                if r.get("user_url")
                                else ""
                            )
                            r["red_id"] = red_id
                            r["note_index"] = idx
                            r["note_title"] = title
                            r["note_url"] = page.url  # 当前详情页url（点击后生成的）
                            f.write(json.dumps(r, ensure_ascii=False) + "\n")

                        print(f"  [ok] 评论记录（含回复）: {len(rows)}")
                        note_count += 1

                    except Exception as e:
                        print("  [error]", repr(e))

                    processed_index.add(idx)
                    progressed = True

                    # 回到搜索页继续下一个
                    go_back_to_search(page)

                    # 类人间隔
                    rsleep(1.5, 4.0, "between notes")

                    if note_count >= MAX_NOTES:
                        break

                if not progressed:
                    # 当前屏都处理完了，继续滚动加载下一屏
                    page.mouse.wheel(0, SCROLL_WHEEL)
                    rsleep(0.4, 0.9, "scroll search next")

        input("\n完成。浏览器保持打开便于调试，按回车退出...\n")


if __name__ == "__main__":
    main()
