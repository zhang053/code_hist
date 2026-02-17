import os
import re
import json
import time
import random
import traceback
from typing import Dict, List, Any, Tuple
from urllib.parse import urlparse, parse_qs
from datetime import datetime, timedelta

from playwright.sync_api import sync_playwright


# =========================
# 配置区（都放最前面，方便你改）
# =========================
SEARCH_URL = "https://www.xiaohongshu.com/search_result?keyword=%25E8%258B%25B1%25E8%25AF%25AD%25E5%25AD%25A6%25E4%25B9%25A0%25E6%259C%25BA&source=web_search_result_notes"

MAX_CARDS_TO_RUN = 999999
SLEEP_EVERY_N_CARDS = 10
SLEEP_SECONDS = 60
CLICK_GAP = (1.0, 2.0)

USER_DATA_DIR = "./pw_user_data"
VIEWPORT = {"width": 1300, "height": 760}

# 评论右侧滚动位置（你给的）
COMMENT_SCROLL_POINT = (940, 500)

# 顶评滚动（右侧评论区域）
TOP_WHEEL_DELTA = 2000
TOP_WHEEL_GAP = (0.06, 0.14)
TOP_WAIT_WINDOW = 0.8
TOP_EMPTY_LIMIT = 12

# ✅ show-more 节奏（重点：两次点击之间要冷却）
SHOWMORE_WAIT_WINDOW = 1.2
SHOWMORE_CLICK_COOLDOWN = (0.35, 0.75)
SHOWMORE_CLICK_HUMAN_GAP = (0.08, 0.20)
SHOWMORE_PER_ROOT_EMPTY_LIMIT = 6
SHOWMORE_GLOBAL_NO_GROWTH_LIMIT = 14
EMPTY_PAGE_LIMIT = 2

# 搜索页滚动：必须很小
SEARCH_SCROLL_WHEEL_DELTA_RANGE = (90, 180)
SEARCH_SCROLL_GAP = (0.06, 0.14)
SEARCH_NO_PROGRESS_LIMIT = 30

RESULT_PATH = "result_comments.json"
CHECKPOINT_PATH = "checkpoint_comments.json"

# ⭐ 每 50 张重开 page
REOPEN_PAGE_EVERY = 50

# MongoDB
MONGO_URI = "mongodb://localhost:27017"
MONGO_DB = "xhs"
MONGO_COL = "result_comments"


# =========================
# Selector（按你整理）
# =========================
SEL_SEARCH_MAIN = "#global > div.main-container > div.with-side-bar.main-content > div > div > div.search-layout__main"
SEL_FEEDS = SEL_SEARCH_MAIN + " > div.feeds-container"
SEL_SECTION_ALL = SEL_FEEDS + " > section.note-item"

# section 内部：可点击的卡片 a（广告没有这个）
SEL_ANCHOR = "div > a.cover.mask.ld"
SEL_TITLE_IN_SECTION = "div > div > a > span"

# 详情页出现判断（关闭 ×）
SEL_DETAIL_CLOSE_X = "body > div.note-detail-mask > div.close-circle > div > svg > use"

# 评论总数：共 N 条评论
SEL_TOTAL = "#noteContainer > div.interaction-container > div.note-scroller > div.comments-el > div > div.total"

# 广告（大家都在搜）关键 class
SEL_AD_QUERY_WRAPPER = ".query-note-wrapper"
AD_TEXT_HINT = "大家都在搜"

# 你指定的时间/IP selector（按 comment id 拼）
SEL_TIME_TMPL = (
    lambda cid: f"#comment-{cid} > div > div.right > div.info > div.date > span:nth-child(1)"
)
SEL_IP_TMPL = (
    lambda cid: f"#comment-{cid} > div > div.right > div.info > div.date > span.location"
)


# =========================
# 日志/工具
# =========================
def ts() -> str:
    return time.strftime("%H:%M:%S")


def log_info(msg: str):
    print(f"[{ts()}][INFO] {msg}")


def log_warn(msg: str):
    print(f"[{ts()}][WARN] {msg}")


def log_err(msg: str):
    print(f"[{ts()}][ERROR] {msg}")


def jitter(a, b):
    time.sleep(random.uniform(a, b))


def now():
    return time.time()


def safe_json(resp):
    try:
        return resp.json()
    except Exception:
        return None


def get_qs(url: str):
    try:
        return parse_qs(urlparse(url).query)
    except Exception:
        return {}


def parse_total_count(text: str):
    m = re.search(r"(\d+)", (text or "").replace(",", ""))
    return int(m.group(1)) if m else None


def extract_note_id_from_href(href: str) -> str:
    m = re.search(r"/search_result/([0-9a-fA-F]+)", href or "")
    return m.group(1) if m else ""


def profile_url(user_id: str) -> str:
    return f"https://www.xiaohongshu.com/user/profile/{user_id}" if user_id else ""


def load_json_file(path: str, default):
    if not os.path.exists(path):
        return default
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return default


def atomic_write_json(path: str, obj: Any):
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=2)
    os.replace(tmp, path)


# =========================
# 时间文本 -> YYYY-MM-DD
# =========================
def normalize_time_text_to_ymd(t: str) -> str:
    if not t:
        return ""

    s = t.strip()

    m = re.search(r"(\d{4})[./-](\d{1,2})[./-](\d{1,2})", s)
    if m:
        y, mo, d = int(m.group(1)), int(m.group(2)), int(m.group(3))
        return f"{y:04d}-{mo:02d}-{d:02d}"

    m = re.search(r"(\d{1,2})[./-](\d{1,2})", s)
    if m and not re.search(r"\d{4}", s):
        y = datetime.now().year
        mo, d = int(m.group(1)), int(m.group(2))
        return f"{y:04d}-{mo:02d}-{d:02d}"

    if "今天" in s:
        return datetime.now().strftime("%Y-%m-%d")
    if "昨天" in s:
        return (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")

    m = re.search(r"(\d+)\s*天前", s)
    if m:
        n = int(m.group(1))
        return (datetime.now() - timedelta(days=n)).strftime("%Y-%m-%d")

    return s


# =========================
# MongoDB（结构不改：_id=note_id,title,comments）
# =========================
def mongo_upsert_one(note_id: str, card_obj: dict):
    try:
        from pymongo import MongoClient

        client = MongoClient(MONGO_URI)
        col = client[MONGO_DB][MONGO_COL]

        doc = {
            "_id": note_id,
            "title": card_obj["title"],
            "comments": card_obj["comments"],
        }
        col.replace_one({"_id": note_id}, doc, upsert=True)

    except Exception as e:
        log_warn(f"MongoDB 写入失败 note_id={note_id}: {e}")


# =========================
# JSON 解析/归一化（time 留空，后面用 DOM 填）
# =========================
def pick_data_comments(payload: dict):
    """
    兼容你截图这种：data.comments = [] 且 has_more=false
    """
    if not isinstance(payload, dict):
        return None, None, None
    d = payload.get("data")
    if not isinstance(d, dict):
        return None, None, None
    comments = d.get("comments")
    if not isinstance(comments, list):
        return None, None, None
    return comments, d.get("has_more"), d.get("cursor")


def is_reply_batch(comments: list) -> bool:
    if not comments:
        return True
    x = comments[0]
    return isinstance(x, dict) and isinstance(x.get("target_comment"), dict)


def norm_top_comment_obj(item: dict):
    ui = item.get("user_info") if isinstance(item.get("user_info"), dict) else {}
    return {
        "id": str(item.get("id") or ""),
        "name": str(ui.get("nickname") or ""),
        "xhs_no": profile_url(str(ui.get("user_id") or "")),
        "ip": str(item.get("ip_location") or ""),
        "time": "",
        "content": str(item.get("content") or ""),
        "replies": [],
        "_sub_comment_has_more": (
            bool(item.get("sub_comment_has_more"))
            if item.get("sub_comment_has_more") is not None
            else False
        ),
        "_sub_comment_count": str(item.get("sub_comment_count") or ""),
    }


def norm_reply_obj(item: dict):
    ui = item.get("user_info") if isinstance(item.get("user_info"), dict) else {}
    target_id = ""
    if isinstance(item.get("target_comment"), dict):
        target_id = str(item.get("target_comment", {}).get("id") or "")
    return {
        "id": str(item.get("id") or ""),
        "name": str(ui.get("nickname") or ""),
        "xhs_no": profile_url(str(ui.get("user_id") or "")),
        "ip": str(item.get("ip_location") or ""),
        "time": "",
        "content": str(item.get("content") or ""),
        "target_id": target_id,
    }


# =========================
# DOM 补 time/ip（按你给的 selector）
# =========================
def dom_get_text(page, selector: str) -> str:
    try:
        loc = page.locator(selector).first
        if loc.count() == 0:
            return ""
        return (loc.inner_text() or "").strip()
    except Exception:
        return ""


def fill_time_ip_from_dom(page, top_obj: dict, replies: List[dict]):
    cid = top_obj.get("id", "")
    if cid:
        raw_t = dom_get_text(page, SEL_TIME_TMPL(cid))
        top_obj["time"] = normalize_time_text_to_ymd(raw_t)

        raw_ip = dom_get_text(page, SEL_IP_TMPL(cid))
        if raw_ip:
            top_obj["ip"] = raw_ip

    for r in replies:
        rid = r.get("id", "")
        if not rid:
            continue
        raw_t = dom_get_text(page, SEL_TIME_TMPL(rid))
        r["time"] = normalize_time_text_to_ymd(raw_t)

        raw_ip = dom_get_text(page, SEL_IP_TMPL(rid))
        if raw_ip:
            r["ip"] = raw_ip


# =========================
# 展开回复（两次点击之间加延迟：你要的节奏）
# =========================
def ensure_comment_dom(page, tid: str, max_scroll=90) -> bool:
    sel = f"#comment-{tid}"
    for _ in range(max_scroll):
        if page.locator(sel).count() > 0:
            return True
        page.mouse.move(*COMMENT_SCROLL_POINT)
        page.mouse.wheel(0, 360)
        jitter(*SHOWMORE_CLICK_HUMAN_GAP)
    return False


def click_show_more_for_root(page, tid: str, active_root_hint: dict) -> bool:
    root = page.locator(f"#comment-{tid}")
    if root.count() == 0:
        return False

    parent = root.locator("xpath=..")
    btn = parent.locator(".reply-container .show-more").first
    if btn.count() == 0:
        parent2 = parent.locator("xpath=..")
        btn = parent2.locator(".reply-container .show-more").first
        if btn.count() == 0:
            return False

    try:
        btn.scroll_into_view_if_needed(timeout=2000)
        try:
            btn.hover(timeout=800)
        except Exception:
            pass
        time.sleep(random.uniform(*SHOWMORE_CLICK_HUMAN_GAP))

        active_root_hint["root"] = tid
        active_root_hint["ts"] = now()

        btn.click(timeout=2000)
        return True
    except Exception:
        try:
            page.evaluate("(el)=>el.click()", btn.element_handle())
            return True
        except Exception:
            return False


# =========================
# 单卡抓取：监听 XHR + 右侧滚动 + show-more 展开
# =========================
def fetch_one_card(page, note_id: str, title: str) -> Tuple[dict, dict]:
    tops: Dict[str, dict] = {}
    replies_by_root: Dict[str, Dict[str, dict]] = {}
    reply_id_to_root: Dict[str, str] = {}
    pending: List[Tuple[str, str, dict]] = []

    top_state = {"count_resp": 0, "has_more": None, "seen_keys": set()}
    reply_state = {"resp_count": 0, "empty_pages_by_root": {}}
    active_root_hint = {"root": "", "ts": 0.0}

    # ⭐ 用于“无评论不空等”的快速判断
    # 一旦收到任意一条 data.comments=[] 且 has_more=false 的顶评响应，就可立即确认无评论
    # 但为了稳妥：必须是“顶评批次”（not reply batch）的 payload，且 comments 为空
    no_comment_fast_confirmed = {"hit": False}

    def attach_reply(reply_id: str, target_id: str, obj: dict) -> bool:
        if target_id in tops:
            root = target_id
            reply_id_to_root[reply_id] = root
            replies_by_root.setdefault(root, {})
            replies_by_root[root][reply_id] = obj
            return True
        if target_id in reply_id_to_root:
            root = reply_id_to_root[target_id]
            reply_id_to_root[reply_id] = root
            replies_by_root.setdefault(root, {})
            replies_by_root[root][reply_id] = obj
            return True
        pending.append((reply_id, target_id, obj))
        return False

    def flush_pending() -> int:
        nonlocal pending
        if not pending:
            return 0
        new_pending = []
        attached = 0
        for rid, tid, obj in pending:
            if attach_reply(rid, tid, obj):
                attached += 1
            else:
                new_pending.append((rid, tid, obj))
        pending = new_pending
        return attached

    def on_response(resp):
        url = resp.url
        if resp.request.resource_type != "xhr":
            return
        ct = (resp.headers.get("content-type") or "").lower()
        if "application/json" not in ct:
            return

        qs = get_qs(url)
        nid = (qs.get("note_id", [""]) or [""])[0]
        if nid != note_id:
            return

        payload = safe_json(resp)
        comments, has_more, cursor = pick_data_comments(payload)
        if comments is None:
            return

        # 顶评批次：comments 为空且 has_more=false -> 直接确认为“无评论”
        if not is_reply_batch(comments):
            if len(comments) == 0 and has_more is False:
                no_comment_fast_confirmed["hit"] = True
                top_state["has_more"] = False
                top_state["count_resp"] += 1
                return

            key = cursor or url.split("?")[-1]
            if key in top_state["seen_keys"]:
                return
            top_state["seen_keys"].add(key)
            top_state["count_resp"] += 1
            top_state["has_more"] = has_more

            for it in comments:
                if not isinstance(it, dict):
                    continue
                tid = str(it.get("id") or "")
                if not tid:
                    continue
                if tid not in tops:
                    tops[tid] = norm_top_comment_obj(it)

                # 顶评接口自带 sub_comments（未折叠的第一条回复）
                sub_list = it.get("sub_comments")
                if isinstance(sub_list, list) and sub_list:
                    replies_by_root.setdefault(tid, {})
                    for sub in sub_list:
                        if not isinstance(sub, dict):
                            continue
                        rid = str(sub.get("id") or "")
                        if not rid:
                            continue
                        obj = norm_reply_obj(sub)
                        if rid not in replies_by_root[tid]:
                            replies_by_root[tid][rid] = obj
                            reply_id_to_root[rid] = tid

            flush_pending()
            return

        # reply batch（show-more 触发）
        reply_state["resp_count"] += 1

        root = ""
        for k in ("root_comment_id", "top_comment_id", "comment_id"):
            v = (qs.get(k, [""]) or [""])[0]
            if v:
                root = v
                break
        if (
            not root
            and active_root_hint["root"]
            and (now() - active_root_hint["ts"] <= 2.2)
        ):
            root = active_root_hint["root"]

        if root:
            if len(comments) == 0:
                reply_state["empty_pages_by_root"][root] = (
                    reply_state["empty_pages_by_root"].get(root, 0) + 1
                )
            else:
                reply_state["empty_pages_by_root"][root] = 0
        if not root:
            return

        bucket = replies_by_root.setdefault(root, {})
        for it in comments:
            if not isinstance(it, dict):
                continue
            rid = str(it.get("id") or "")
            if not rid or rid in bucket:
                continue
            obj = norm_reply_obj(it)
            target_id = obj.get("target_id") or root

            if root in tops:
                bucket[rid] = obj
                reply_id_to_root[rid] = root
            else:
                attach_reply(rid, target_id, obj)

        flush_pending()

    page.on("response", on_response)

    # 等详情页打开
    page.wait_for_selector(SEL_DETAIL_CLOSE_X, timeout=15000)

    shown_total = None
    try:
        total_text = page.locator(SEL_TOTAL).first.inner_text().strip()
        shown_total = parse_total_count(total_text)
    except Exception:
        pass

    # ✅ 如果页面显示“荒地 点击评论”（无评论），shown_total 往往解析不到或为 0
    # 但我们以监听到的 JSON 为准，不空等。

    # 顶评翻页：右侧评论区域
    page.mouse.move(*COMMENT_SCROLL_POINT)
    jitter(0.08, 0.15)

    # 等首包顶评（但如果无评论，JSON会很快返回空）
    t0 = now()
    while (
        now() - t0 < 2.3
        and top_state["count_resp"] == 0
        and not no_comment_fast_confirmed["hit"]
    ):
        time.sleep(0.03)

    # ⭐ 无评论：直接返回
    if no_comment_fast_confirmed["hit"] or (shown_total == 0):
        # 仍然构造 card_obj / report
        card_obj = {"title": title, "comments": []}
        report = {
            "title": title,
            "shown_total": shown_total,
            "got_total": 0,
            "diff_total": 0 if shown_total in (None, 0) else (shown_total - 0),
            "got_top": 0,
            "got_replies": 0,
            "reply_resp": 0,
        }
        try:
            page.remove_listener("response", on_response)
        except Exception:
            pass
        return card_obj, report

    # 顶评继续翻页：拿全顶评
    empty = 0
    last_resp = top_state["count_resp"]
    while True:
        if top_state["has_more"] is False:
            break

        page.mouse.wheel(0, TOP_WHEEL_DELTA)
        jitter(*TOP_WHEEL_GAP)

        start = now()
        got_new = False
        while now() - start < TOP_WAIT_WINDOW:
            if top_state["count_resp"] > last_resp:
                got_new = True
                break
            time.sleep(0.03)

        if got_new:
            last_resp = top_state["count_resp"]
            empty = 0
        else:
            empty += 1
            if empty >= TOP_EMPTY_LIMIT:
                break

    log_info(f"[TOP DONE] tops={len(tops)} top_resp={top_state['count_resp']}")

    # show-more 补全：只对 sub_comment_has_more 的顶评做展开
    need_roots = [tid for tid, obj in tops.items() if obj.get("_sub_comment_has_more")]

    last_reply_resp = reply_state["resp_count"]
    global_no_growth = 0

    for tid in need_roots:
        if not ensure_comment_dom(page, tid):
            continue

        per_empty = 0
        while True:
            clicked = click_show_more_for_root(page, tid, active_root_hint)
            if not clicked:
                break

            start = now()
            grew = False
            while now() - start < SHOWMORE_WAIT_WINDOW:
                if reply_state["resp_count"] > last_reply_resp:
                    grew = True
                    last_reply_resp = reply_state["resp_count"]
                    break
                time.sleep(0.05)

            time.sleep(random.uniform(*SHOWMORE_CLICK_COOLDOWN))

            ep = reply_state["empty_pages_by_root"].get(tid, 0)
            if ep >= EMPTY_PAGE_LIMIT:
                break

            if grew:
                per_empty = 0
                global_no_growth = 0
            else:
                per_empty += 1
                global_no_growth += 1
                if per_empty >= SHOWMORE_PER_ROOT_EMPTY_LIMIT:
                    break
                if global_no_growth >= SHOWMORE_GLOBAL_NO_GROWTH_LIMIT:
                    break

            page.mouse.move(*COMMENT_SCROLL_POINT)
            page.mouse.wheel(0, 420)
            time.sleep(random.uniform(0.05, 0.12))

        if global_no_growth >= SHOWMORE_GLOBAL_NO_GROWTH_LIMIT:
            break

    flush_pending()

    # 最后：DOM 补 time/ip
    comments_out = []
    got_top = len(tops)
    got_replies = 0

    for tid, top in tops.items():
        bucket = replies_by_root.get(tid, {})
        replies_list = list(bucket.values())

        fill_time_ip_from_dom(page, top, replies_list)

        got_replies += len(replies_list)

        replies_out = [
            {
                "name": r["name"],
                "xhs_no": r["xhs_no"],
                "ip": r["ip"],
                "time": r["time"],
                "content": r["content"],
            }
            for r in replies_list
        ]
        comments_out.append(
            {
                "name": top["name"],
                "xhs_no": top["xhs_no"],
                "ip": top["ip"],
                "time": top["time"],
                "content": top["content"],
                "replies": replies_out,
            }
        )

    got_total = got_top + got_replies
    diff_total = (shown_total - got_total) if shown_total is not None else None

    card_obj = {"title": title, "comments": comments_out}
    report = {
        "title": title,
        "shown_total": shown_total,
        "got_total": got_total,
        "diff_total": diff_total,
        "got_top": got_top,
        "got_replies": got_replies,
        "reply_resp": reply_state["resp_count"],
    }

    try:
        page.remove_listener("response", on_response)
    except Exception:
        pass

    return card_obj, report


# =========================
# 搜索页扫描：可点击卡片 + 跳广告
# =========================
def section_is_ad_or_query(section) -> bool:
    try:
        if section.locator(SEL_AD_QUERY_WRAPPER).count() > 0:
            return True
    except Exception:
        pass
    try:
        txt = section.inner_text(timeout=200) or ""
        if AD_TEXT_HINT in txt:
            return True
    except Exception:
        pass
    return False


def scan_clickable_cards(page) -> List[dict]:
    out = []
    secs = page.locator(SEL_SECTION_ALL)
    n = secs.count()

    for i in range(n):
        sec = secs.nth(i)

        idx_s = sec.get_attribute("data-index") or ""
        if not idx_s.isdigit():
            continue
        idx = int(idx_s)

        if section_is_ad_or_query(sec):
            continue

        a = sec.locator(SEL_ANCHOR).first
        if a.count() == 0:
            continue

        href = a.get_attribute("href") or ""
        nid = extract_note_id_from_href(href)
        if not nid:
            continue

        title = ""
        try:
            tloc = sec.locator(SEL_TITLE_IN_SECTION).first
            if tloc.count():
                # ✅ 不 strip：原样（你要求的）
                title = tloc.inner_text() or ""
        except Exception:
            title = ""

        out.append({"index": idx, "note_id": nid, "title": title, "anchor": a})

    out.sort(key=lambda x: x["index"])
    return out


# =========================
# 断点 key：标题优先，空标题用 index
# =========================
def make_resume_key(title: str, index: int) -> str:
    if title:
        return title  # 原样（不 strip）
    return f"__EMPTY__@{index}"


# =========================
# main：断点续跑 + 每卡保存 + Mongo 同步
# =========================
def main():
    checkpoint = load_json_file(
        CHECKPOINT_PATH,
        default={"done_keys": [], "last_index": 0, "failed": [], "mismatch": []},
    )

    done_keys = set(checkpoint.get("done_keys", []))
    next_min_index = checkpoint.get("last_index", 0)

    # ⭐ 从 result.json 里补齐 done_keys（防止 checkpoint 丢/少）
    result = load_json_file(RESULT_PATH, default={"cards": []})
    if not isinstance(result, dict) or "cards" not in result:
        result = {"cards": []}
    for i, c in enumerate(result.get("cards", []) or []):
        title = ""
        if isinstance(c, dict):
            title = c.get("title") or ""
        k = make_resume_key(title, i)
        if title:
            done_keys.add(title)
        else:
            # 空标题：尽量用占位，但这里 index 是 result 内序号，不一定等于 data-index
            # 不强行加入，避免误判
            pass

    # 写回一次（包含标题）
    checkpoint["done_keys"] = list(done_keys)
    atomic_write_json(CHECKPOINT_PATH, checkpoint)

    with sync_playwright() as p:
        ctx = p.chromium.launch_persistent_context(
            USER_DATA_DIR,
            headless=False,
            viewport=VIEWPORT,
            args=["--disable-blink-features=AutomationControlled"],
        )

        def open_new_page():
            page = ctx.new_page()
            page.goto(SEARCH_URL, wait_until="domcontentloaded")
            page.wait_for_selector(SEL_FEEDS, timeout=30000)
            return page

        page = open_new_page()

        log_info("如果需要登录/验证，请在浏览器完成后回到终端按回车继续...")
        input()

        processed = 0
        failed_cards = []
        mismatch_cards = []

        no_progress = 0
        max_seen_clickable = -1

        log_info(
            f"[SEARCH] start need_count={MAX_CARDS_TO_RUN}, already_done={len(done_keys)} start_index={next_min_index}"
        )

        while processed < MAX_CARDS_TO_RUN:
            cards = scan_clickable_cards(page)
            if cards:
                max_seen_clickable = max(max_seen_clickable, cards[-1]["index"])

            target = None
            for c in cards:
                if c["index"] < next_min_index:
                    continue

                resume_key = make_resume_key(c["title"], c["index"])
                if resume_key in done_keys:
                    continue

                target = c
                break

            if target is None:
                before = max_seen_clickable
                delta = random.randint(*SEARCH_SCROLL_WHEEL_DELTA_RANGE)
                page.mouse.wheel(0, delta)
                jitter(*SEARCH_SCROLL_GAP)

                cards2 = scan_clickable_cards(page)
                if cards2:
                    max_seen_clickable = max(max_seen_clickable, cards2[-1]["index"])

                if max_seen_clickable <= before:
                    no_progress += 1
                    log_warn(
                        f"[SEARCH] no_progress={no_progress}/{SEARCH_NO_PROGRESS_LIMIT} max_clickable_index={max_seen_clickable}"
                    )
                    if no_progress >= SEARCH_NO_PROGRESS_LIMIT:
                        log_warn("[SEARCH STOP] 长时间没有新卡片出现，停止")
                        break
                else:
                    no_progress = 0
                continue

            no_progress = 0
            idx = target["index"]
            nid = target["note_id"]
            title = target["title"]
            resume_key = make_resume_key(title, idx)

            log_info(
                f"\n===== [CARD {processed+1}] index={idx} note_id={nid} title={title!r} ====="
            )

            try:
                jitter(*CLICK_GAP)
                target["anchor"].click()

                card_obj, report = fetch_one_card(page, note_id=nid, title=title)

                # 关闭详情
                try:
                    if page.locator(SEL_DETAIL_CLOSE_X).count():
                        page.locator(SEL_DETAIL_CLOSE_X).first.click(timeout=2000)
                    else:
                        page.keyboard.press("Escape")
                except Exception:
                    try:
                        page.keyboard.press("Escape")
                    except Exception:
                        pass

                # ✅ 每卡写一次 result（结构不改：{"cards":[...] }）
                result["cards"].append(card_obj)
                atomic_write_json(RESULT_PATH, result)

                # ✅ Mongo 同步（结构不改）
                mongo_upsert_one(nid, card_obj)

                # ✅ checkpoint：写入标题 key
                done_keys.add(resume_key)
                checkpoint["done_keys"] = list(done_keys)
                checkpoint["last_index"] = idx + 1

                if report.get("diff_total") not in (None, 0):
                    checkpoint.setdefault("mismatch", []).append(
                        {
                            "title": title,
                            "diff_total": report.get("diff_total"),
                            "shown_total": report.get("shown_total"),
                            "got_total": report.get("got_total"),
                        }
                    )
                    mismatch_cards.append(
                        (
                            title,
                            report.get("diff_total"),
                            report.get("shown_total"),
                            report.get("got_total"),
                        )
                    )

                atomic_write_json(CHECKPOINT_PATH, checkpoint)

                processed += 1
                log_info(
                    f"[CARD OK] index={idx} shown={report.get('shown_total')} got={report.get('got_total')} diff={report.get('diff_total')} reply_resp={report.get('reply_resp')}"
                )

                next_min_index = idx + 1

                # ⭐ 每 50 张重开 page
                if REOPEN_PAGE_EVERY and processed % REOPEN_PAGE_EVERY == 0:
                    log_warn(
                        f"[REOPEN PAGE] processed={processed} 重开 page 防止卡顿..."
                    )
                    try:
                        page.close()
                    except Exception:
                        pass
                    page = open_new_page()

                if (
                    processed % SLEEP_EVERY_N_CARDS == 0
                    and processed < MAX_CARDS_TO_RUN
                ):
                    log_info(f"[SLEEP] processed={processed}, sleep {SLEEP_SECONDS}s")
                    time.sleep(SLEEP_SECONDS)

            except Exception as e:
                err_text = f"{type(e).__name__}: {e}"
                log_err(f"[CARD FAIL] index={idx} note_id={nid} {err_text}")
                log_err(traceback.format_exc())

                failed_cards.append((title, err_text))
                checkpoint.setdefault("failed", []).append(
                    {"title": title, "error": err_text}
                )
                atomic_write_json(CHECKPOINT_PATH, checkpoint)

                try:
                    if page.locator(SEL_DETAIL_CLOSE_X).count():
                        page.locator(SEL_DETAIL_CLOSE_X).first.click(timeout=1500)
                    else:
                        page.keyboard.press("Escape")
                except Exception:
                    pass

                next_min_index = idx + 1
                continue

        log_info("\n========== RUN SUMMARY ==========")
        log_info(f"processed={processed}, done_total={len(done_keys)}")

        if failed_cards:
            log_warn("未正常结束（失败）的卡片：")
            for t, err in failed_cards:
                log_warn(f"  - title={t!r}  {err}")
        else:
            log_info("失败卡片：无")

        if mismatch_cards:
            log_warn("评论数有差异（diff!=0）的卡片（本次运行）：")
            for t, diff, shown, got in mismatch_cards:
                log_warn(f"  - title={t!r}  shown={shown} got={got} diff={diff}")
        else:
            log_info("评论数差异：本次无")

        log_info(f"\n结果文件：{RESULT_PATH}")
        log_info(f"断点文件：{CHECKPOINT_PATH}")
        log_info("按回车关闭浏览器...")
        input()
        ctx.close()


if __name__ == "__main__":
    main()
