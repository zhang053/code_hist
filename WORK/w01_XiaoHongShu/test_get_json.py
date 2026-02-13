import re
import json
import time
import random
from urllib.parse import urlparse, parse_qs

from playwright.sync_api import sync_playwright

# =========================
# 配置区（只改这里）
# =========================
SEARCH_URL = "https://www.xiaohongshu.com/search_result?keyword=%25E8%258B%25B1%25E8%25AF%25AD%25E5%25AD%25A6%25E4%25B9%25A0%25E6%259C%25BA&source=web_search_result_notes"
TARGET_NOTE_ID = "688320be00000000170370d9"

USER_DATA_DIR = "./pw_user_data"
VIEWPORT = {"width": 1300, "height": 760}

# 右侧评论区滚动点
COMMENT_SCROLL_POINT = (940, 500)

# 顶评翻页滚动
TOP_WHEEL_DELTA = 1600
TOP_WHEEL_GAP = (0.08, 0.18)
TOP_WAIT_WINDOW = 0.9
TOP_EMPTY_LIMIT = 8

# 展开回复点击节奏
SHOWMORE_CLICK_GAP = (0.18, 0.40)
SHOWMORE_PER_ROOT_EMPTY_LIMIT = 5
SHOWMORE_GLOBAL_EMPTY_ROUNDS = 12

# 空页兜底：comments=[] 但 has_more=true
EMPTY_PAGE_LIMIT = 3

OUT_JSON = f"card_{TARGET_NOTE_ID}.json"
OUT_REPORT = f"card_{TARGET_NOTE_ID}_report.json"

# =========================
# Selector（你整理的）
# =========================
SEL_SEARCH_MAIN = "#global > div.main-container > div.with-side-bar.main-content > div > div > div.search-layout__main"
SEL_FEEDS = SEL_SEARCH_MAIN + " > div.feeds-container"
SEL_SECTION_ALL = SEL_FEEDS + " > section"
SEL_CARD_ANCHOR_ALL = SEL_FEEDS + " a.cover.mask.ld"
SEL_TITLE_IN_SECTION = "div > div > a > span"

SEL_DETAIL_CLOSE_X = "body > div.note-detail-mask > div.close-circle > div > svg > use"
SEL_TOTAL = "#noteContainer > div.interaction-container > div.note-scroller > div.comments-el > div > div.total"

SEL_SHOW_MORE = ".show-more"


# =========================
# 工具函数
# =========================
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


def pick_data_comments(payload: dict):
    """
    解析接口：payload["data"]["comments"] 必须是 list
    同时读 has_more / cursor
    """
    if not isinstance(payload, dict):
        return None, None, None, None
    d = payload.get("data")
    if not isinstance(d, dict):
        return None, None, None, None
    comments = d.get("comments")
    if not isinstance(comments, list):
        return None, None, None, None
    return comments, d.get("has_more"), d.get("cursor"), d


def is_reply_batch(comments: list) -> bool:
    """
    回复接口：每条通常带 target_comment
    """
    if not comments:
        # 空页无法判断，交给上层用 qs / root_hint 处理
        return True
    x = comments[0]
    return isinstance(x, dict) and isinstance(x.get("target_comment"), dict)


def norm_top_comment_obj(item: dict):
    ui = item.get("user_info") if isinstance(item.get("user_info"), dict) else {}
    return {
        "id": str(item.get("id") or ""),
        "name": str(ui.get("nickname") or ""),
        "xhs_no": str(ui.get("user_id") or ""),
        "ip": str(item.get("ip_location") or ""),
        "time": str(item.get("create_time") or ""),
        "content": str(item.get("content") or ""),
        "replies": [],
        # 内部字段（写 report 用）
        "_sub_comment_has_more": (
            bool(item.get("sub_comment_has_more"))
            if item.get("sub_comment_has_more") is not None
            else False
        ),
        "_sub_comment_cursor": str(item.get("sub_comment_cursor") or ""),
        "_sub_comment_count": str(item.get("sub_comment_count") or ""),
    }


def norm_reply_obj(item: dict):
    ui = item.get("user_info") if isinstance(item.get("user_info"), dict) else {}
    return {
        "id": str(item.get("id") or ""),
        "name": str(ui.get("nickname") or ""),
        "xhs_no": str(ui.get("user_id") or ""),
        "ip": str(item.get("ip_location") or ""),
        "time": str(item.get("create_time") or ""),
        "content": str(item.get("content") or ""),
        "target_id": (
            str(item.get("target_comment", {}).get("id") or "")
            if isinstance(item.get("target_comment"), dict)
            else ""
        ),
    }


# =========================
# 主逻辑
# =========================
def main():
    # 顶评：top_id -> obj
    tops = {}

    # 回复：root_top_id -> {reply_id -> reply_obj}
    # 这里做“并集”：顶评接口 sub_comments + 展开接口 data.comments 都往这里放
    replies_by_root = {}

    # 用于“回复回复”归并到顶评（因为你只要两层树）
    # reply_id -> root_top_id
    reply_id_to_root = {}

    # pending：target_id 暂时找不到归属时先挂起
    pending = []  # (reply_id, target_id, reply_obj)

    def attach_reply(reply_id: str, target_id: str, obj: dict) -> bool:
        # 1) target 是顶评
        if target_id in tops:
            root = target_id
            reply_id_to_root[reply_id] = root
            replies_by_root.setdefault(root, {})
            replies_by_root[root][reply_id] = obj
            return True

        # 2) target 是某条 reply（回复回复）
        if target_id in reply_id_to_root:
            root = reply_id_to_root[target_id]
            reply_id_to_root[reply_id] = root
            replies_by_root.setdefault(root, {})
            replies_by_root[root][reply_id] = obj
            return True

        # 3) 暂存
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

    # 顶评分页状态
    top_state = {
        "count_resp": 0,
        "has_more": None,
        "cursor": None,
        "seen_keys": set(),
    }

    # 回复状态（按 root 统计空页次数）
    reply_state = {
        "resp_count": 0,
        "added_total": 0,
        "empty_pages_by_root": {},
    }

    # 点击 show-more 的 root hint（用于空页/无 root 参数时归类）
    active_root_hint = {"root": "", "ts": 0.0}

    def on_response(resp):
        url = resp.url
        if resp.request.resource_type != "xhr":
            return

        ct = (resp.headers.get("content-type") or "").lower()
        if "application/json" not in ct:
            return

        qs = get_qs(url)
        nid = (qs.get("note_id", [""]) or [""])[0]
        if nid != TARGET_NOTE_ID:
            return

        payload = safe_json(resp)
        comments, has_more, cursor, d = pick_data_comments(payload)
        if comments is None:
            return

        # 先用“是否带 target_comment”区分（空列表默认为 reply，再交给 root_hint）
        reply_batch = is_reply_batch(comments)

        if not reply_batch:
            # ===== 顶评分页 =====
            key = cursor or url.split("?")[-1]
            if key in top_state["seen_keys"]:
                return
            top_state["seen_keys"].add(key)
            top_state["count_resp"] += 1
            top_state["has_more"] = has_more
            top_state["cursor"] = cursor

            added_top = 0
            added_sub = 0

            for it in comments:
                if not isinstance(it, dict):
                    continue
                tid = str(it.get("id") or "")
                if not tid:
                    continue

                # 1) 顶评入库
                if tid not in tops:
                    tops[tid] = norm_top_comment_obj(it)
                    added_top += 1

                # 2) 关键修复：把顶评接口自带 sub_comments 也入库（不管有没有 show-more）
                sub_list = it.get("sub_comments")
                if isinstance(sub_list, list) and sub_list:
                    for sub in sub_list:
                        if not isinstance(sub, dict):
                            continue
                        rid = str(sub.get("id") or "")
                        if not rid:
                            continue
                        obj = norm_reply_obj(sub)
                        # 这类 sub 通常带 target_comment.id = 某条评论 id（可能是顶评也可能是回复）
                        target_id = obj.get("target_id") or tid
                        # 如果顶评还没在 tops（极少），先兜底当作 tid
                        if tid not in tops:
                            tops[tid] = norm_top_comment_obj(it)
                        # 先强制认为 root = tid（因为这是“tid 的 sub_comments”）
                        # 同时也记录 reply_id_to_root，方便后续“回复回复”追溯
                        replies_by_root.setdefault(tid, {})
                        if rid not in replies_by_root[tid]:
                            replies_by_root[tid][rid] = obj
                            reply_id_to_root[rid] = tid
                            added_sub += 1

            # 冲洗 pending（因为 tops 可能变多了）
            added_sub += flush_pending()

            print(
                f"[TOP] items={len(comments)} add_top={added_top} add_sub_from_top={added_sub} has_more={has_more} cursor={cursor}"
            )
            return

        # ===== 回复分页（展开回复触发）=====
        reply_state["resp_count"] += 1

        # 尝试识别 root（从 query 参数取）
        root = ""
        for k in ("root_comment_id", "top_comment_id", "comment_id"):
            v = (qs.get(k, [""]) or [""])[0]
            if v:
                root = v
                break

        # 没有 root 参数：用刚点击的 root_hint（2 秒窗口）
        if (
            not root
            and active_root_hint["root"]
            and (now() - active_root_hint["ts"] <= 2.0)
        ):
            root = active_root_hint["root"]

        # 空页处理：你截图那种 comments=[] 但 has_more=true
        if root:
            if len(comments) == 0:
                reply_state["empty_pages_by_root"][root] = (
                    reply_state["empty_pages_by_root"].get(root, 0) + 1
                )
            else:
                reply_state["empty_pages_by_root"][root] = 0

        if not root:
            # 无法安全归类，不入库，只打印
            print(
                f"[REPLY?] batch={len(comments)} has_more={has_more} cursor={cursor} (无root，跳过入库)"
            )
            return

        bucket = replies_by_root.setdefault(root, {})
        added = 0

        for it in comments:
            if not isinstance(it, dict):
                continue
            rid = str(it.get("id") or "")
            if not rid:
                continue
            if rid in bucket:
                continue
            obj = norm_reply_obj(it)
            target_id = obj.get("target_id") or root

            # 如果 root 自己不是顶评（理论上 root 是顶评 id），也能用 target_id 去归并
            if root in tops:
                # 直接归到 root
                bucket[rid] = obj
                reply_id_to_root[rid] = root
                added += 1
            else:
                # 用 target_id 追溯顶评归属（更稳）
                if attach_reply(rid, target_id, obj):
                    added += 1

        added += flush_pending()
        reply_state["added_total"] += added

        print(
            f"[REPLY] root={root} batch={len(comments)} add={added} has_more={has_more} cursor={cursor} empty_pages={reply_state['empty_pages_by_root'].get(root,0)}"
        )

    with sync_playwright() as p:
        ctx = p.chromium.launch_persistent_context(
            USER_DATA_DIR,
            headless=False,
            viewport=VIEWPORT,
            args=["--disable-blink-features=AutomationControlled"],
        )
        page = ctx.new_page()
        page.on("response", on_response)

        page.goto(SEARCH_URL, wait_until="domcontentloaded")
        print("请先在浏览器里完成登录/验证，然后回到终端按回车继续...")
        input()

        page.wait_for_selector(SEL_SECTION_ALL, timeout=30000)

        # ===== 找到目标卡片 =====
        anchors = page.locator(SEL_CARD_ANCHOR_ALL)
        if anchors.count() == 0:
            raise RuntimeError("搜索页找不到任何卡片 a.cover.mask.ld")

        target_anchor = None
        target_section = None
        for i in range(anchors.count()):
            a = anchors.nth(i)
            href = a.get_attribute("href") or ""
            if f"/search_result/{TARGET_NOTE_ID}" in href:
                target_anchor = a
                target_section = a.locator("xpath=ancestor::section[1]")
                break

        if target_anchor is None:
            raise RuntimeError(f"未找到目标卡片 /search_result/{TARGET_NOTE_ID}")

        title = ""
        try:
            if target_section and target_section.count():
                tloc = target_section.locator(SEL_TITLE_IN_SECTION).first
                if tloc.count():
                    title = (tloc.inner_text() or "").strip()
        except Exception:
            pass

        print(f"[CARD] note_id={TARGET_NOTE_ID} title={title!r}")

        jitter(0.3, 0.8)
        target_anchor.click()
        page.wait_for_selector(SEL_DETAIL_CLOSE_X, timeout=15000)

        shown_total = None
        try:
            total_text = page.locator(SEL_TOTAL).first.inner_text().strip()
            shown_total = parse_total_count(total_text)
        except Exception:
            pass
        print(f"[TOTAL] shown_total={shown_total}")

        # ===== 1) 拉完顶评分页 =====
        page.mouse.move(*COMMENT_SCROLL_POINT)
        jitter(0.1, 0.2)

        # 等首包
        t0 = now()
        while now() - t0 < 2.0 and top_state["count_resp"] == 0:
            time.sleep(0.03)

        empty = 0
        last_resp = top_state["count_resp"]

        while True:
            if top_state["has_more"] is False:
                print("[STOP] top has_more=false")
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
                print(f"[EMPTY] no new TOP resp {empty}/{TOP_EMPTY_LIMIT}")
                if empty >= TOP_EMPTY_LIMIT:
                    print("[STOP] top fallback empty")
                    break

        print(
            f"[TOP DONE] tops={len(tops)} top_page_responses={top_state['count_resp']}"
        )
        print(
            f"[SUB FROM TOP] replies_from_top_total={sum(len(v) for v in replies_by_root.values())} pending={len(pending)}"
        )

        # ===== 2) 只对 sub_comment_has_more=true 的顶评补全（点击 show-more）=====
        need_roots = [
            tid for tid, obj in tops.items() if obj.get("_sub_comment_has_more")
        ]
        print(f"[NEED REPLY] roots_need_fill={len(need_roots)}")

        def ensure_comment_dom(tid: str, max_scroll=50) -> bool:
            sel = f"#comment-{tid}"
            for _ in range(max_scroll):
                if page.locator(sel).count() > 0:
                    return True
                page.mouse.move(*COMMENT_SCROLL_POINT)
                page.mouse.wheel(0, 1200)
                jitter(0.06, 0.12)
            return False

        def click_show_more_for_root(tid: str) -> bool:
            root = page.locator(f"#comment-{tid}")
            if root.count() == 0:
                return False
            parent = root.locator("xpath=..")
            btn = parent.locator(".reply-container .show-more").first
            if btn.count() == 0:
                return False
            try:
                btn.scroll_into_view_if_needed(timeout=2000)
                jitter(*SHOWMORE_CLICK_GAP)
                active_root_hint["root"] = tid
                active_root_hint["ts"] = now()
                btn.click(timeout=2000)
                return True
            except Exception:
                return False

        global_no_new_rounds = 0
        last_added_total = reply_state["added_total"]

        roots_failed = []
        roots_done = []

        for idx, tid in enumerate(need_roots, 1):
            print(
                f"\n[ROOT] ({idx}/{len(need_roots)}) {tid} sub_count={tops[tid].get('_sub_comment_count')} cursor={tops[tid].get('_sub_comment_cursor')}"
            )
            if not ensure_comment_dom(tid):
                roots_failed.append({"root": tid, "reason": "dom_not_found"})
                print("[ROOT] dom_not_found")
                continue

            per_empty = 0
            while True:
                clicked = click_show_more_for_root(tid)
                if not clicked:
                    roots_done.append({"root": tid, "reason": "no_show_more"})
                    break

                before = reply_state["added_total"]
                start = now()
                while now() - start < 1.2:
                    if reply_state["added_total"] > before:
                        break
                    time.sleep(0.05)

                if reply_state["added_total"] > before:
                    per_empty = 0
                else:
                    per_empty += 1

                ep = reply_state["empty_pages_by_root"].get(tid, 0)
                if ep >= EMPTY_PAGE_LIMIT:
                    roots_failed.append(
                        {"root": tid, "reason": f"empty_pages>={EMPTY_PAGE_LIMIT}"}
                    )
                    print("[ROOT] too many empty pages, stop")
                    break

                if per_empty >= SHOWMORE_PER_ROOT_EMPTY_LIMIT:
                    roots_done.append(
                        {
                            "root": tid,
                            "reason": f"no_new_after_{SHOWMORE_PER_ROOT_EMPTY_LIMIT}_clicks",
                        }
                    )
                    break

                page.mouse.move(*COMMENT_SCROLL_POINT)
                page.mouse.wheel(0, 600)
                jitter(0.06, 0.12)

            if reply_state["added_total"] > last_added_total:
                last_added_total = reply_state["added_total"]
                global_no_new_rounds = 0
            else:
                global_no_new_rounds += 1
                if global_no_new_rounds >= SHOWMORE_GLOBAL_EMPTY_ROUNDS:
                    print("[GLOBAL STOP] too many rounds without any new replies")
                    break

        # 最后冲洗 pending
        flush_pending()

        # ===== 3) 生成最终输出（你要求的结构）=====
        comments_out = []
        mismatch_roots = []

        for tid, obj in tops.items():
            bucket = replies_by_root.get(tid, {})
            obj["replies"] = [
                {
                    "name": r["name"],
                    "xhs_no": r["xhs_no"],
                    "ip": r["ip"],
                    "time": r["time"],
                    "content": r["content"],
                }
                for r in bucket.values()
            ]

            # 对账：sub_comment_count vs 实际 replies
            sub_cnt = obj.get("_sub_comment_count")
            try:
                sub_cnt_int = int(sub_cnt) if sub_cnt not in ("", None) else None
            except Exception:
                sub_cnt_int = None
            real = len(bucket)
            if sub_cnt_int is not None and real != sub_cnt_int:
                mismatch_roots.append(
                    {"root": tid, "sub_comment_count": sub_cnt_int, "got_replies": real}
                )

            comments_out.append(
                {
                    "name": obj["name"],
                    "xhs_no": obj["xhs_no"],
                    "ip": obj["ip"],
                    "time": obj["time"],
                    "content": obj["content"],
                    "replies": obj["replies"],
                }
            )

        got_top = len(tops)
        got_replies = sum(len(v) for v in replies_by_root.values())
        got_total = got_top + got_replies
        diff_total = (shown_total - got_total) if shown_total is not None else None

        out = {
            "cards": [
                {
                    "title": title,
                    "comments": comments_out,
                }
            ]
        }
        with open(OUT_JSON, "w", encoding="utf-8") as f:
            json.dump(out, f, ensure_ascii=False, indent=2)

        report = {
            "note_id": TARGET_NOTE_ID,
            "title": title,
            "shown_total": shown_total,
            "got_top": got_top,
            "got_replies": got_replies,
            "got_total": got_total,
            "diff_total": diff_total,
            "top_page_responses": top_state["count_resp"],
            "reply_responses": reply_state["resp_count"],
            "replies_from_top_total": sum(len(v) for v in replies_by_root.values()),
            "pending_left": len(pending),
            "roots_need_fill": len(need_roots),
            "roots_done": roots_done[:100],
            "roots_failed": roots_failed[:100],
            "roots_reply_count_mismatch": mismatch_roots[:300],
        }
        with open(OUT_REPORT, "w", encoding="utf-8") as f:
            json.dump(report, f, ensure_ascii=False, indent=2)

        print("\n=== DONE ===")
        print("saved:", OUT_JSON)
        print("saved:", OUT_REPORT)
        print(
            "shown_total:",
            shown_total,
            "got_total:",
            got_total,
            "diff_total:",
            diff_total,
        )
        print("got_top:", got_top, "got_replies:", got_replies)
        print(
            "mismatch_roots:", len(mismatch_roots), "failed_roots:", len(roots_failed)
        )

        print("\n按回车退出...")
        input()
        ctx.close()


if __name__ == "__main__":
    main()
