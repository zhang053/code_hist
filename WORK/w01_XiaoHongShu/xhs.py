import os
import atexit
import argparse
import re
import json
import time
import random
import traceback
from typing import Dict, List, Any, Tuple, Optional, Iterable
from urllib.parse import urlparse, parse_qs
from datetime import datetime, timedelta
from pathlib import Path
from dataclasses import dataclass
from html import unescape

from playwright.sync_api import sync_playwright


# =========================
# 配置区：目标URL / 抓取参数（已移除所有“防风控等待”）
# =========================
SEARCH_URL = "https://www.xiaohongshu.com/search_result?keyword=%25E8%258B%25B1%25E8%25AF%25AD%25E5%25AD%25A6%25E4%25B9%25A0%25E6%259C%25BA&source=web_search_result_notes"

MAX_CARDS_TO_RUN = 999999
VIEWPORT = {"width": 1300, "height": 760}

# 评论区滚动时鼠标移动到的区域坐标（避免滚动错位置）
COMMENT_SCROLL_POINT = (940, 500)

# 顶层评论滚动加载参数（不含“人为等待”）
TOP_WHEEL_DELTA = 2000
TOP_WAIT_WINDOW = 0.8
TOP_EMPTY_LIMIT = 12

# show-more 展开回复等待窗口（保留“等响应到来”的窗口；已移除人为冷却）
SHOWMORE_WAIT_WINDOW = 1.2
SHOWMORE_PER_ROOT_EMPTY_LIMIT = 6
SHOWMORE_GLOBAL_NO_GROWTH_LIMIT = 14
EMPTY_PAGE_LIMIT = 2

# 搜索列表滚动策略（不含人为等待）
SEARCH_SCROLL_WHEEL_DELTA_RANGE = (90, 180)
SEARCH_NO_PROGRESS_LIMIT = 30

BASE_DIR = Path(__file__).resolve().parent
RESULT_PATH = str(BASE_DIR / "result_comments.json")
CHECKPOINT_PATH = str(BASE_DIR / "checkpoint_pipeline.json")
USER_DATA_DIR = str(BASE_DIR / "pw_user_data")

# 每处理 N 张卡片重开一次 page（稳定性用；不是防风控等待）
REOPEN_PAGE_EVERY = 50

# MongoDB
MONGO_URI = "mongodb://localhost:27017"
MONGO_DB = "xhs"
MONGO_COL = "result_comments"

PROFILES_PATH = BASE_DIR / "result_xhs_profiles.json"
DEBUG_HTML_DIR = BASE_DIR / "debug_html"
DEBUG_HTML_DIR.mkdir(exist_ok=True)

PLAYWRIGHT_UA = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/122.0.6261.57 Safari/537.36"
)

# 连续 profile 失败阈值（命中后停止，避免死跑）
WIND_CONTROL_LIMIT = 3

SPAN_PATTERNS = {
    "user-redId": re.compile(
        r"<span[^>]+class=\"[^\"]*user-redId[^\"]*\"[^>]*>(.*?)</span>",
        re.IGNORECASE | re.DOTALL,
    ),
    "user-IP": re.compile(
        r"<span[^>]+class=\"[^\"]*user-IP[^\"]*\"[^>]*>(.*?)</span>",
        re.IGNORECASE | re.DOTALL,
    ),
}
JSON_RED_ID_PATTERN = re.compile(r"\"redId\"\s*:\s*\"([0-9A-Za-z]+)\"")
JSON_IP_PATTERN = re.compile(r"\"ipLocation\"\s*:\s*\"([^\"\\]*)\"")
UNDEFINED_VALUE_PATTERN = re.compile(r":\s*undefined")
PROFILE_URL_PATTERN = re.compile(r"/user/profile/([0-9a-zA-Z]+)")
TAG_STRIPPER = re.compile(r"<[^>]+>")


# =========================
# Selector 区：页面元素定位
# =========================
SEL_SEARCH_MAIN = "#global > div.main-container > div.with-side-bar.main-content > div > div > div.search-layout__main"
SEL_FEEDS = SEL_SEARCH_MAIN + " > div.feeds-container"
SEL_SECTION_ALL = SEL_FEEDS + " > section.note-item"

SEL_ANCHOR = "div > a.cover.mask.ld"
SEL_TITLE_IN_SECTION = "div > div > a > span"
SEL_CARD_AUTHOR_LINK = "div > div > div > a"
SEL_CARD_AUTHOR_NAME = SEL_CARD_AUTHOR_LINK + " > div > div.name"
SEL_CARD_PUBLISH_TIME = SEL_CARD_AUTHOR_LINK + " > div > div.time"

SEL_DETAIL_CLOSE_X = "body > div.note-detail-mask > div.close-circle > div > svg > use"
SEL_TOTAL = "#noteContainer > div.interaction-container > div.note-scroller > div.comments-el > div > div.total"

SEL_AD_QUERY_WRAPPER = ".query-note-wrapper"
AD_TEXT_HINT = "大家都在搜"

SEL_TIME_TMPL = (
    lambda cid: f"#comment-{cid} > div > div.right > div.info > div.date > span:nth-child(1)"
)
SEL_IP_TMPL = (
    lambda cid: f"#comment-{cid} > div > div.right > div.info > div.date > span.location"
)
SEL_NO_COMMENT_TEXT = "#noteContainer > div.interaction-container > div.note-scroller > div.comments-el > div > p.no-comments-text"


# =========================
# 日志 & 工具函数（已移除所有“防风控等待”）
# =========================
def ts() -> str:
    return time.strftime("%H:%M:%S")


def log_info(msg: str):
    print(f"[{ts()}][INFO] {msg}")


def log_warn(msg: str):
    print(f"[{ts()}][WARN] {msg}")


def log_err(msg: str):
    print(f"[{ts()}][ERROR] {msg}")


def jitter(_a=None, _b=None):
    # ✅ 禁用所有“拟人/防风控”随机等待
    return


def now() -> float:
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


def extract_user_id_from_profile_href(href: str) -> str:
    m = re.search(r"/user/profile/([0-9a-zA-Z]+)", href or "")
    return m.group(1) if m else ""


def load_json_file(path: str, default):
    path = str(path)
    if not os.path.exists(path):
        return default
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return default


def atomic_write_json(path: str, obj: Any):
    path = str(path)
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=2)
    os.replace(tmp, path)


def default_comments_checkpoint() -> Dict[str, Any]:
    return {
        "done_keys": [],
        "last_index": 0,
        "failed": [],
        "mismatch": [],
        "card_meta": [],
    }


def default_profiles_checkpoint() -> Dict[str, Any]:
    return {"entries": [], "last_index": 0}


def make_card_key(
    title: str,
    author_name: str,
    publish_time: str,
    fallback: Optional[str] = None,
) -> Optional[str]:
    title = (title or "").strip()
    author_name = (author_name or "").strip()
    publish_time = (publish_time or "").strip()

    if title:
        return f"title::{title}"
    if author_name:
        return f"author::{author_name}::time::{publish_time}"
    if fallback is not None:
        return fallback
    return "__EMPTY__"


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


def mongo_upsert_one(note_id: str, card_obj: dict):
    try:
        from pymongo import MongoClient

        client = MongoClient(MONGO_URI)
        col = client[MONGO_DB][MONGO_COL]

        doc = {
            "_id": note_id,
            "title": card_obj.get("title") or "",
            "name": card_obj.get("name") or "",
            "xhs_no": card_obj.get("xhs_no") or "",
            "time": card_obj.get("time") or "",
            "comments": card_obj.get("comments") or [],
        }
        col.replace_one({"_id": note_id}, doc, upsert=True)
    except Exception as e:
        log_warn(f"MongoDB 写入失败 note_id={note_id}: {e}")


# =========================
# 断点存储
# =========================
class PipelineStore:
    def __init__(self, path: str):
        self.path = str(path)
        payload = load_json_file(self.path, default={})
        if not isinstance(payload, dict):
            payload = {}
        self.payload = payload
        self.comments_data = payload.setdefault(
            "comments", default_comments_checkpoint()
        )
        self.profiles_data = payload.setdefault(
            "profiles", default_profiles_checkpoint()
        )

    def save(self):
        atomic_write_json(self.path, self.payload)


PIPELINE_STORE: Optional[PipelineStore] = None


def get_pipeline_store() -> PipelineStore:
    global PIPELINE_STORE
    if PIPELINE_STORE is None:
        PIPELINE_STORE = PipelineStore(CHECKPOINT_PATH)
    return PIPELINE_STORE


class CheckpointManager:
    def __init__(self, result_path: str, store: Optional[PipelineStore] = None):
        self.result_path = result_path
        self.store = store or get_pipeline_store()
        self.result_data = load_json_file(result_path, default={"cards": []})
        if not isinstance(self.result_data, dict) or "cards" not in self.result_data:
            self.result_data = {"cards": []}

        self.checkpoint_data = self.store.comments_data
        if not isinstance(self.checkpoint_data, dict):
            self.checkpoint_data = default_comments_checkpoint()
            self.store.payload["comments"] = self.checkpoint_data

        for key in ("failed", "mismatch", "card_meta"):
            if key not in self.checkpoint_data or not isinstance(
                self.checkpoint_data[key], list
            ):
                self.checkpoint_data[key] = []

        if not isinstance(self.checkpoint_data.get("done_keys"), list):
            self.checkpoint_data["done_keys"] = []
        if not isinstance(self.checkpoint_data.get("last_index"), int):
            self.checkpoint_data["last_index"] = 0

        self.done_keys = set()
        self.card_meta: Dict[str, Dict[str, str]] = {}
        self.result_lookup: Dict[str, dict] = {}

        self._hydrate_from_checkpoint()
        self._hydrate_from_result()
        self.save_checkpoint()

    def _hydrate_from_checkpoint(self):
        for raw in self.checkpoint_data.get("done_keys") or []:
            if not raw:
                continue
            if raw.startswith("__EMPTY__@"):
                raw = "__EMPTY__"
            elif not (
                raw.startswith("title::")
                or raw.startswith("author::")
                or raw.startswith("__EMPTY__")
            ):
                raw = make_card_key(raw, "", "", fallback=raw) or raw
            self.done_keys.add(raw)

        for meta in self.checkpoint_data.get("card_meta") or []:
            if not isinstance(meta, dict):
                continue
            title = meta.get("title") or ""
            name = meta.get("name") or ""
            publish_time = meta.get("time") or ""
            fallback = meta.get("fallback") or meta.get("resume_key") or ""
            if isinstance(fallback, str) and fallback.startswith("__EMPTY__@"):
                fallback = "__EMPTY__"
            key = meta.get("key") or make_card_key(
                title, name, publish_time, fallback=fallback
            )
            if not key:
                continue
            self.card_meta[key] = {"title": title, "name": name, "time": publish_time}
            self.done_keys.add(key)

    def _hydrate_from_result(self):
        for card in self.result_data.get("cards") or []:
            if not isinstance(card, dict):
                continue
            title = card.get("title") or ""
            name = card.get("name") or ""
            publish_time = card.get("time") or ""
            fallback = None
            if not title and not name:
                legacy = (card.get("resume_key") or "").strip()
                fallback = (
                    "__EMPTY__"
                    if not legacy or legacy.startswith("__EMPTY__@")
                    else legacy
                )
            key = make_card_key(title, name, publish_time, fallback=fallback)
            if not key:
                continue
            self.result_lookup.setdefault(key, card)
            self.card_meta.setdefault(
                key, {"title": title, "name": name, "time": publish_time}
            )
            self.done_keys.add(key)

    def has_done(self, key: Optional[str]) -> bool:
        return bool(key and key in self.done_keys)

    def append_card(self, key: Optional[str], card_obj: dict, meta: Dict[str, str]):
        self.result_data.setdefault("cards", []).append(card_obj)
        if key:
            self.done_keys.add(key)
            self.card_meta[key] = {
                "title": meta.get("title", ""),
                "name": meta.get("name", ""),
                "time": meta.get("time", ""),
            }
            self.result_lookup[key] = card_obj

    def update_metadata_if_needed(
        self, key: Optional[str], candidate: Dict[str, Any]
    ) -> bool:
        if not key or key not in self.done_keys:
            return False

        meta_changed = False
        card_changed = False

        stored = self.card_meta.get(key, {"title": "", "name": "", "time": ""})
        for field in ("title", "name", "time"):
            new_val = (candidate.get(field) or "").strip()
            if new_val and stored.get(field) != new_val:
                stored[field] = new_val
                meta_changed = True
        self.card_meta[key] = stored

        card = self.result_lookup.get(key)
        if card:
            for field in ("name", "xhs_no", "time"):
                new_val = (candidate.get(field) or "").strip()
                if new_val and card.get(field) != new_val:
                    card[field] = new_val
                    card_changed = True

        if card_changed:
            self.save_result()
        if meta_changed:
            self.save_checkpoint()
        return card_changed or meta_changed

    def set_last_index(self, value: int):
        self.checkpoint_data["last_index"] = value

    def get_last_index(self) -> int:
        try:
            return int(self.checkpoint_data.get("last_index", 0) or 0)
        except Exception:
            return 0

    def save_result(self):
        atomic_write_json(self.result_path, self.result_data)

    def save_checkpoint(self):
        self.checkpoint_data["done_keys"] = sorted(self.done_keys)
        self.checkpoint_data["card_meta"] = [
            {
                "key": k,
                "title": v.get("title", ""),
                "name": v.get("name", ""),
                "time": v.get("time", ""),
            }
            for k, v in self.card_meta.items()
        ]
        self.store.save()

    def save_all(self):
        self.save_result()
        self.save_checkpoint()


# =========================
# 页面读取小工具（精简重复 try/except）
# =========================
def loc_text(loc, default: str = "") -> str:
    try:
        if loc.count():
            return (loc.inner_text() or "").strip()
    except Exception:
        pass
    return default


def loc_attr(loc, name: str, default: str = "") -> str:
    try:
        if loc.count():
            return (loc.get_attribute(name) or "").strip()
    except Exception:
        pass
    return default


# =========================
# CardFetcher：进入详情页，监听 XHR JSON，组装评论/回复
# =========================
class CardFetcher:
    def __init__(self, page):
        self.page = page

    @staticmethod
    def pick_data_comments(payload: dict):
        if not isinstance(payload, dict):
            return None, None, None
        data = payload.get("data")
        if not isinstance(data, dict):
            return None, None, None
        comments = data.get("comments")
        if not isinstance(comments, list):
            return None, None, None
        return comments, data.get("has_more"), data.get("cursor")

    @staticmethod
    def is_reply_batch(comments: list) -> bool:
        if not comments:
            return True
        head = comments[0]
        return isinstance(head, dict) and isinstance(head.get("target_comment"), dict)

    @staticmethod
    def norm_top_comment_obj(item: dict):
        ui = item.get("user_info") if isinstance(item.get("user_info"), dict) else {}
        return {
            "id": str(item.get("id") or ""),
            "name": str(ui.get("nickname") or ""),
            "xhs_no": profile_url(str(ui.get("user_id") or "")),
            "ip": str(item.get("ip_location") or ""),
            "time": "",
            "content": str(item.get("content") or ""),
            "_sub_comment_has_more": (
                bool(item.get("sub_comment_has_more"))
                if item.get("sub_comment_has_more") is not None
                else False
            ),
            "_sub_comment_count": str(item.get("sub_comment_count") or ""),
        }

    @staticmethod
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

    def dom_get_text(self, selector: str) -> str:
        try:
            loc = self.page.locator(selector).first
            return loc_text(loc, "")
        except Exception:
            return ""

    def fill_time_ip_from_dom(self, top_obj: dict, replies: List[dict]):
        cid = top_obj.get("id", "")
        if cid:
            top_obj["time"] = normalize_time_text_to_ymd(
                self.dom_get_text(SEL_TIME_TMPL(cid))
            )
            raw_ip = self.dom_get_text(SEL_IP_TMPL(cid))
            if raw_ip:
                top_obj["ip"] = raw_ip

        for r in replies:
            rid = r.get("id", "")
            if not rid:
                continue
            r["time"] = normalize_time_text_to_ymd(
                self.dom_get_text(SEL_TIME_TMPL(rid))
            )
            raw_ip = self.dom_get_text(SEL_IP_TMPL(rid))
            if raw_ip:
                r["ip"] = raw_ip

    def ensure_comment_dom(self, tid: str, max_scroll=90) -> bool:
        sel = f"#comment-{tid}"
        for _ in range(max_scroll):
            if self.page.locator(sel).count() > 0:
                return True
            self.page.mouse.move(*COMMENT_SCROLL_POINT)
            self.page.mouse.wheel(0, 360)
        return False

    def click_show_more_for_root(self, tid: str, active_root_hint: dict) -> bool:
        root = self.page.locator(f"#comment-{tid}")
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
            active_root_hint["root"] = tid
            active_root_hint["ts"] = now()
            btn.click(timeout=2000)
            return True
        except Exception:
            try:
                self.page.evaluate("(el)=>el.click()", btn.element_handle())
                return True
            except Exception:
                return False

    def fetch_card(
        self, note_id: str, title: str, author_meta: Optional[Dict[str, Any]] = None
    ) -> Tuple[dict, dict]:
        tops: Dict[str, dict] = {}
        replies_by_root: Dict[str, Dict[str, dict]] = {}
        reply_id_to_root: Dict[str, str] = {}
        pending: List[Tuple[str, str, dict]] = []

        top_state = {"count_resp": 0, "has_more": None, "seen_keys": set()}
        reply_state = {"resp_count": 0, "empty_pages_by_root": {}}
        active_root_hint = {"root": "", "ts": 0.0}
        no_comment_fast_confirmed = {"hit": False}

        author_meta = author_meta or {}
        card_meta = {
            "name": author_meta.get("name") or "",
            "xhs_no": author_meta.get("xhs_no") or "",
            "time": author_meta.get("time") or "",
        }

        def attach_reply(reply_id: str, target_id: str, obj: dict) -> bool:
            if target_id in tops:
                root_id = target_id
                reply_id_to_root[reply_id] = root_id
                replies_by_root.setdefault(root_id, {})
                replies_by_root[root_id][reply_id] = obj
                return True
            if target_id in reply_id_to_root:
                root_id = reply_id_to_root[target_id]
                reply_id_to_root[reply_id] = root_id
                replies_by_root.setdefault(root_id, {})
                replies_by_root[root_id][reply_id] = obj
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
            comments, has_more, cursor = self.pick_data_comments(payload)
            if comments is None:
                return

            # 顶层评论包
            if not self.is_reply_batch(comments):
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

                for item in comments:
                    if not isinstance(item, dict):
                        continue
                    tid = str(item.get("id") or "")
                    if not tid:
                        continue
                    if tid not in tops:
                        tops[tid] = self.norm_top_comment_obj(item)

                    sub_list = item.get("sub_comments")
                    if isinstance(sub_list, list) and sub_list:
                        replies_by_root.setdefault(tid, {})
                        for sub in sub_list:
                            if not isinstance(sub, dict):
                                continue
                            rid = str(sub.get("id") or "")
                            if not rid:
                                continue
                            obj = self.norm_reply_obj(sub)
                            if rid not in replies_by_root[tid]:
                                replies_by_root[tid][rid] = obj
                                reply_id_to_root[rid] = tid

                flush_pending()
                return

            # 回复包
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
            for item in comments:
                if not isinstance(item, dict):
                    continue
                rid = str(item.get("id") or "")
                if not rid or rid in bucket:
                    continue
                obj = self.norm_reply_obj(item)
                target_id = obj.get("target_id") or root

                if root in tops:
                    bucket[rid] = obj
                    reply_id_to_root[rid] = root
                else:
                    attach_reply(rid, target_id, obj)

            flush_pending()

        self.page.on("response", on_response)

        self.page.wait_for_selector(SEL_DETAIL_CLOSE_X, timeout=15000)

        shown_total = None
        try:
            shown_total = parse_total_count(
                loc_text(self.page.locator(SEL_TOTAL).first, "")
            )
        except Exception:
            pass

        self.page.mouse.move(*COMMENT_SCROLL_POINT)

        # 允许首包 XHR 到来（这是正确性等待，不是防风控）
        t0 = now()
        while (
            now() - t0 < 2.3
            and top_state["count_resp"] == 0
            and not no_comment_fast_confirmed["hit"]
        ):
            time.sleep(0.03)

        has_no_comment_dom = False
        try:
            has_no_comment_dom = self.page.locator(SEL_NO_COMMENT_TEXT).count() > 0
        except Exception:
            has_no_comment_dom = False

        if no_comment_fast_confirmed["hit"] or (shown_total == 0) or has_no_comment_dom:
            card_obj = {
                "title": title,
                "name": card_meta["name"],
                "xhs_no": card_meta["xhs_no"],
                "time": card_meta["time"],
                "comments": [],
            }
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
                self.page.remove_listener("response", on_response)
            except Exception:
                pass
            return card_obj, report

        # 拉取顶层评论（依赖 has_more + 计数变化判断）
        empty = 0
        last_resp = top_state["count_resp"]
        while True:
            if top_state["has_more"] is False:
                break

            self.page.mouse.wheel(0, TOP_WHEEL_DELTA)

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

        need_roots = [
            tid for tid, obj in tops.items() if obj.get("_sub_comment_has_more")
        ]

        last_reply_resp = reply_state["resp_count"]
        global_no_growth = 0

        for tid in need_roots:
            if not self.ensure_comment_dom(tid):
                continue

            per_empty = 0
            while True:
                if not self.click_show_more_for_root(tid, active_root_hint):
                    break

                start = now()
                grew = False
                while now() - start < SHOWMORE_WAIT_WINDOW:
                    if reply_state["resp_count"] > last_reply_resp:
                        grew = True
                        last_reply_resp = reply_state["resp_count"]
                        break
                    time.sleep(0.05)

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

                self.page.mouse.move(*COMMENT_SCROLL_POINT)
                self.page.mouse.wheel(0, 420)

            if global_no_growth >= SHOWMORE_GLOBAL_NO_GROWTH_LIMIT:
                break

        flush_pending()

        # 输出结构化 comments
        comments_out = []
        got_top = len(tops)
        got_replies = 0

        for tid, top in tops.items():
            bucket = replies_by_root.get(tid, {})
            replies_list = list(bucket.values())
            self.fill_time_ip_from_dom(top, replies_list)
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

        card_obj = {
            "title": title,
            "name": card_meta["name"],
            "xhs_no": card_meta["xhs_no"],
            "time": card_meta["time"],
            "comments": comments_out,
        }
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
            self.page.remove_listener("response", on_response)
        except Exception:
            pass

        return card_obj, report


# =========================
# 搜索页扫描：找可点击卡片
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
    out: List[dict] = []
    secs = page.locator(SEL_SECTION_ALL)
    n = secs.count()

    for i in range(n):
        sec = secs.nth(i)

        idx_s = loc_attr(sec, "data-index", "")
        if not idx_s.isdigit():
            continue
        idx = int(idx_s)

        if section_is_ad_or_query(sec):
            continue

        a = sec.locator(SEL_ANCHOR).first
        if a.count() == 0:
            continue

        href = loc_attr(a, "href", "")
        nid = extract_note_id_from_href(href)
        if not nid:
            continue

        title = loc_text(sec.locator(SEL_TITLE_IN_SECTION).first, "")

        author_name = loc_text(sec.locator(SEL_CARD_AUTHOR_NAME).first, "")
        publish_time = loc_text(sec.locator(SEL_CARD_PUBLISH_TIME).first, "")

        author_profile = ""
        link = sec.locator(SEL_CARD_AUTHOR_LINK).first
        if link.count():
            profile_href = loc_attr(link, "href", "")
            user_id = extract_user_id_from_profile_href(profile_href)
            author_profile = profile_url(user_id)

        out.append(
            {
                "index": idx,
                "note_id": nid,
                "title": title,
                "anchor": a,
                "name": author_name,
                "xhs_no": author_profile,
                "time": publish_time,
            }
        )

    out.sort(key=lambda x: x["index"])
    return out


# =========================
# Runner：搜索页滚动 -> 逐卡点击 -> 抓评论 -> 写 JSON/Mongo -> 断点续跑
# =========================
class XiaoHongShuRunner:
    def __init__(self):
        self.manager = CheckpointManager(RESULT_PATH)

    def _open_new_page(self, ctx):
        page = ctx.new_page()
        page.goto(SEARCH_URL, wait_until="domcontentloaded")
        page.wait_for_selector(SEL_FEEDS, timeout=30000)
        return page

    def _resume_key_for_card(self, card: dict) -> str:
        return make_card_key(
            card.get("title") or "",
            card.get("name") or "",
            card.get("time") or "",
            fallback="__EMPTY__",
        )

    def _card_meta(self, card: dict) -> Dict[str, str]:
        return {
            "title": card.get("title") or "",
            "name": card.get("name") or "",
            "time": card.get("time") or "",
        }

    def run(self, pause_on_finish: bool = True):
        checkpoint = self.manager.checkpoint_data
        next_min_index = self.manager.get_last_index()

        with sync_playwright() as p:
            ctx = p.chromium.launch_persistent_context(
                USER_DATA_DIR,
                headless=False,
                viewport=VIEWPORT,
                args=["--disable-blink-features=AutomationControlled"],
            )

            page = self._open_new_page(ctx)
            fetcher = CardFetcher(page)

            log_info(
                "请先在浏览器中完成登录/验证（如有），完成后回到控制台按回车开始抓取..."
            )
            input()

            processed = 0
            failed_cards = []
            mismatch_cards = []
            no_progress = 0
            max_seen_clickable = -1

            log_info(
                f"[SEARCH] start need_count={MAX_CARDS_TO_RUN}, already_done={len(self.manager.done_keys)} start_index={next_min_index}"
            )

            while processed < MAX_CARDS_TO_RUN:
                cards = scan_clickable_cards(page)
                if cards:
                    max_seen_clickable = max(max_seen_clickable, cards[-1]["index"])

                target = None
                for c in cards:
                    resume_key = self._resume_key_for_card(c)
                    c["key"] = resume_key
                    self.manager.update_metadata_if_needed(resume_key, c)

                    if c["index"] < next_min_index:
                        continue
                    if self.manager.has_done(resume_key):
                        continue

                    target = c
                    break

                if target is None:
                    before = max_seen_clickable
                    page.mouse.wheel(
                        0, random.randint(*SEARCH_SCROLL_WHEEL_DELTA_RANGE)
                    )

                    cards2 = scan_clickable_cards(page)
                    if cards2:
                        max_seen_clickable = max(
                            max_seen_clickable, cards2[-1]["index"]
                        )

                    if max_seen_clickable <= before:
                        no_progress += 1
                        log_warn(
                            f"[SEARCH] no_progress={no_progress}/{SEARCH_NO_PROGRESS_LIMIT} max_clickable_index={max_seen_clickable}"
                        )
                        if no_progress >= SEARCH_NO_PROGRESS_LIMIT:
                            log_warn("[SEARCH STOP] 多次滚动仍无新增卡片，停止本轮。")
                            break
                    else:
                        no_progress = 0
                    continue

                no_progress = 0
                idx = target["index"]
                nid = target["note_id"]
                title = target.get("title") or ""
                resume_key = target.get("key") or self._resume_key_for_card(target)

                log_info(
                    f"\n===== [CARD {processed+1}] index={idx} note_id={nid} title={title!r} ====="
                )

                try:
                    target["anchor"].click()

                    card_obj, report = fetcher.fetch_card(
                        note_id=nid, title=title, author_meta=target
                    )

                    # 关闭详情页
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

                    mongo_upsert_one(nid, card_obj)

                    self.manager.append_card(
                        resume_key, card_obj, self._card_meta(target)
                    )
                    self.manager.set_last_index(idx + 1)

                    if report.get("diff_total") not in (None, 0):
                        info = {
                            "title": title,
                            "diff_total": report.get("diff_total"),
                            "shown_total": report.get("shown_total"),
                            "got_total": report.get("got_total"),
                        }
                        checkpoint.setdefault("mismatch", []).append(info)
                        mismatch_cards.append(
                            (
                                title,
                                report.get("diff_total"),
                                report.get("shown_total"),
                                report.get("got_total"),
                            )
                        )

                    self.manager.save_all()

                    processed += 1
                    log_info(
                        f"[CARD OK] index={idx} shown={report.get('shown_total')} got={report.get('got_total')} diff={report.get('diff_total')} reply_resp={report.get('reply_resp')}"
                    )
                    next_min_index = idx + 1

                    if REOPEN_PAGE_EVERY and processed % REOPEN_PAGE_EVERY == 0:
                        log_warn(
                            f"[REOPEN PAGE] processed={processed} 关闭并重新打开页面以提升稳定性..."
                        )
                        try:
                            page.close()
                        except Exception:
                            pass
                        page = self._open_new_page(ctx)
                        fetcher = CardFetcher(page)

                except Exception as e:
                    err_text = f"{type(e).__name__}: {e}"
                    log_err(f"[CARD FAIL] index={idx} note_id={nid} {err_text}")
                    log_err(traceback.format_exc())

                    failed_cards.append((title, err_text))
                    checkpoint.setdefault("failed", []).append(
                        {"title": title, "error": err_text}
                    )
                    self.manager.save_checkpoint()

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
            log_info(f"processed={processed}, done_total={len(self.manager.done_keys)}")

            if failed_cards:
                log_warn("[WARN] 存在抓取失败的卡片：")
                for t, err in failed_cards:
                    log_warn(f"  - title={t!r}  {err}")
            else:
                log_info("全部卡片抓取成功。")

            if mismatch_cards:
                log_warn("[WARN] 有卡片评论数量 diff!=0，需要人工复核：")
                for t, diff, shown, got in mismatch_cards:
                    log_warn(f"  - title={t!r}  shown={shown} got={got} diff={diff}")
            else:
                log_info("评论数量与页面展示一致。")

            log_info(f"\n输出结果路径：{RESULT_PATH}")
            log_info(f"断点文件：{CHECKPOINT_PATH}")

            if pause_on_finish:
                log_info("按回车结束本轮抓取")
                input()
            ctx.close()


# =========================
# Profile 抓取：从用户主页解析“小红书号 / IP属地”
# =========================
def extract_user_id(value: str) -> str:
    value = (value or "").strip()
    if not value:
        return ""
    if value.startswith("http"):
        parts = value.split("/user/profile/", 1)
        if len(parts) == 2:
            rest = parts[1]
            for sep in ("?", "#"):
                rest = rest.split(sep, 1)[0]
            return rest
    return value.split("?", 1)[0].split("#", 1)[0]


def normalize_red_id(text: str) -> str:
    cleaned = (text or "").replace("小红书号", "").replace("IP属地", "")
    cleaned = cleaned.replace(":", "").replace("：", "")
    return cleaned.strip()


def normalize_ip(text: str) -> str:
    cleaned = (text or "").replace("IP属地", "")
    cleaned = cleaned.replace(":", "").replace("：", "")
    return cleaned.strip()


def extract_text(html: str, key: str) -> str:
    match = SPAN_PATTERNS[key].search(html)
    if not match:
        return ""
    text = TAG_STRIPPER.sub("", match.group(1) or "")
    return unescape(text).replace("\xa0", " ").strip()


def parse_profile_fields(html: str) -> Tuple[str, str, bool]:
    xhs_no = normalize_red_id(extract_text(html, "user-redId"))
    ip_location = normalize_ip(extract_text(html, "user-IP"))
    fallback = False

    if not xhs_no:
        m = JSON_RED_ID_PATTERN.search(html)
        if m:
            xhs_no = normalize_red_id(m.group(1))
            fallback = True

    if not ip_location:
        m = JSON_IP_PATTERN.search(html)
        if m:
            ip_location = normalize_ip(m.group(1))
            fallback = True

    if not xhs_no or not ip_location:
        marker = "window.__INITIAL_STATE__="
        start = html.find(marker)
        if start != -1:
            end = html.find("</script>", start)
            if end != -1:
                raw = html[start + len(marker) : end]
                cleaned = UNDEFINED_VALUE_PATTERN.sub(":null", raw)
                try:
                    payload = json.loads(cleaned)
                    info = payload.get("user", {}).get("userInfo") or {}
                    if not xhs_no:
                        xhs_no = normalize_red_id(info.get("redId") or "")
                        fallback = fallback or bool(xhs_no)
                    if not ip_location:
                        ip_location = normalize_ip(info.get("ipLocation") or "")
                        fallback = fallback or bool(ip_location)
                except Exception:
                    pass

    return xhs_no, ip_location, fallback


def save_debug_html(name: str, html: str, reason: str) -> str:
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    safe = re.sub(r"[^0-9A-Za-z._-]+", "_", name or "unknown").strip("._") or "unknown"
    filename = f"{safe}_{reason}_{timestamp}.html"
    (DEBUG_HTML_DIR / filename).write_text(html, encoding="utf-8", errors="ignore")
    return filename


@dataclass
class Target:
    target_index: int
    source_type: str
    card_title: str
    profile_url: str
    commenter_name: str
    comment_time: str
    original_ip: str


@dataclass
class FetchResult:
    target: Target
    status: str
    profile_url: str
    xhs_no: str
    ip_location: str
    error: str = ""


class ProfileCheckpoint:
    def __init__(self, store: Optional[PipelineStore] = None):
        self.store = store or get_pipeline_store()
        self.data = self.store.profiles_data
        if not isinstance(self.data, dict):
            self.data = default_profiles_checkpoint()
            self.store.payload["profiles"] = self.data

        entries = self.data.setdefault("entries", [])
        if not isinstance(entries, list):
            entries = []
            self.data["entries"] = entries

        self.entries: List[Dict[str, str]] = entries
        self.by_url: Dict[str, Dict[str, str]] = {}
        for entry in self.entries:
            url = (entry.get("url") or "").strip()
            if url:
                self.by_url[url] = entry

        try:
            self.last_index = int(self.data.get("last_index", 0) or 0)
        except Exception:
            self.last_index = 0

    def is_processed(self, url: str) -> bool:
        entry = self.by_url.get(url)
        return bool(entry and entry.get("xhs_no"))

    def mark(self, target: Target, xhs_no: str, ip: str):
        url = target.profile_url
        entry = self.by_url.get(url)
        updated = False

        if entry is None:
            entry = {
                "name": target.commenter_name,
                "url": url,
                "xhs_no": xhs_no,
                "ip": ip,
            }
            self.by_url[url] = entry
            self.entries.append(entry)
            updated = True
        else:
            if xhs_no and entry.get("xhs_no") != xhs_no:
                entry["xhs_no"] = xhs_no
                updated = True
            if ip and entry.get("ip") != ip:
                entry["ip"] = ip
                updated = True

        if target.target_index + 1 > self.last_index:
            self.last_index = target.target_index + 1
            updated = True

        if updated:
            self.data["last_index"] = self.last_index
            self.store.save()


class PlaywrightClient:
    def __init__(self):
        self._play = None
        self._context = None

    def _ensure(self):
        if self._play is None:
            self._play = sync_playwright().start()
        if self._context is None:
            self._context = self._play.chromium.launch_persistent_context(
                user_data_dir=str(USER_DATA_DIR),
                headless=False,
                user_agent=PLAYWRIGHT_UA,
                viewport={"width": 1280, "height": 720},
                args=["--disable-blink-features=AutomationControlled"],
            )
        return self._context

    def fetch_html(self, url: str) -> str:
        ctx = self._ensure()
        page = ctx.new_page()
        try:
            page.goto(url, wait_until="domcontentloaded", timeout=30000)
            return page.content()
        finally:
            try:
                page.close()
            except Exception:
                pass

    def close(self):
        if self._context is not None:
            try:
                self._context.close()
            except Exception:
                pass
            self._context = None
        if self._play is not None:
            try:
                self._play.stop()
            except Exception:
                pass
            self._play = None


CLIENT = PlaywrightClient()
atexit.register(CLIENT.close)


def load_existing_profiles() -> Dict[str, Dict[str, str]]:
    path = Path(PROFILES_PATH)
    if not path.exists():
        return {}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {}

    items = data.get("profiles") or data.get("records") or []
    mapping = {}
    for item in items:
        url = (item.get("url") or item.get("profile_url") or "").strip()
        if not url:
            continue
        mapping[url] = {
            "name": item.get("name") or item.get("commenter") or "",
            "url": url,
            "xhs_no": item.get("xhs_no") or item.get("fetched_xhs_no") or "",
            "ip": item.get("ip") or item.get("fetched_ip") or "",
        }
    return mapping


def save_profiles(mapping: Dict[str, Dict[str, str]], path: Path = PROFILES_PATH):
    payload = {
        "generated_at": time.strftime("%Y-%m-%d %H:%M:%S"),
        "source_file": RESULT_PATH,
        "profiles": sorted(mapping.values(), key=lambda x: x.get("name", "")),
    }
    atomic_write_json(path, payload)


def load_targets() -> List[Target]:
    result_file = Path(RESULT_PATH)
    if not result_file.exists():
        raise FileNotFoundError(f"result file not found: {result_file}")
    data = json.loads(result_file.read_text(encoding="utf-8"))
    cards = data.get("cards", [])

    targets: List[Target] = []
    seen = set()
    for card in cards:
        title = (card.get("title") or "").strip()
        for comment in card.get("comments", []):
            _collect_target(comment, title, "comment", targets, seen)
            for reply in comment.get("replies", []):
                _collect_target(reply, title, "reply", targets, seen)
    return targets


def _collect_target(
    node: Dict[str, Any], title: str, source_type: str, targets: List[Target], seen: set
) -> None:
    url = (node.get("xhs_no") or "").strip()
    if not url or url in seen:
        return
    targets.append(
        Target(
            target_index=len(targets),
            source_type=source_type,
            card_title=title,
            profile_url=url,
            commenter_name=(node.get("name") or "").strip(),
            comment_time=(node.get("time") or "").strip(),
            original_ip=(node.get("ip") or "").strip(),
        )
    )
    seen.add(url)


def fetch_profile(target: Target) -> FetchResult:
    try:
        html = CLIENT.fetch_html(target.profile_url)
        if not html:
            raise RuntimeError("empty html")
        xhs_no, ip_location, fallback = parse_profile_fields(html)
        notes = []
        if fallback:
            notes.append("regex_or_state")
        if not xhs_no or not ip_location:
            filename = save_debug_html(
                target.commenter_name, html, "playwright_no_fields"
            )
            notes.append(f"playwright_no_fields:{filename}")
        return FetchResult(
            target=target,
            status="ok",
            profile_url=target.profile_url,
            xhs_no=xhs_no,
            ip_location=ip_location,
            error=";".join(notes),
        )
    except Exception as exc:
        filename = save_debug_html(target.commenter_name, str(exc), "playwright_error")
        return FetchResult(
            target=target,
            status="error",
            profile_url=target.profile_url,
            xhs_no="",
            ip_location="",
            error=f"playwright_error:{filename}",
        )


def merge_into_profiles(
    profiles: Dict[str, Dict[str, str]], record: FetchResult
) -> None:
    entry = profiles.get(record.profile_url)
    if entry is None:
        profiles[record.profile_url] = {
            "name": record.target.commenter_name,
            "url": record.profile_url,
            "xhs_no": record.xhs_no,
            "ip": record.ip_location,
        }
        return
    if record.xhs_no and entry.get("xhs_no") != record.xhs_no:
        entry["xhs_no"] = record.xhs_no
    if record.ip_location and entry.get("ip") != record.ip_location:
        entry["ip"] = record.ip_location
    if (
        record.target.commenter_name
        and entry.get("name") != record.target.commenter_name
    ):
        entry["name"] = record.target.commenter_name


def run_profile_fetch(limit: int = 0, output: Path = PROFILES_PATH):
    targets = load_targets()
    checkpoint = ProfileCheckpoint()
    profiles = load_existing_profiles()

    ctx = CLIENT._ensure()
    login_page = ctx.new_page()
    try:
        login_page.goto(
            "https://www.xiaohongshu.com/", wait_until="domcontentloaded", timeout=30000
        )
    except Exception:
        pass
    input("请在浏览器完成登录/验证（如有），完成后回到控制台按回车继续...")
    try:
        login_page.close()
    except Exception:
        pass

    # checkpoint 里已有的直接合并进 profiles
    for url, entry in checkpoint.by_url.items():
        if entry.get("xhs_no"):
            profiles[url] = {
                "name": entry.get("name") or "",
                "url": url,
                "xhs_no": entry.get("xhs_no") or "",
                "ip": entry.get("ip") or "",
            }

    consecutive_failures = 0
    processed_new = 0

    for target in targets:
        if limit and limit > 0 and processed_new >= limit:
            break
        if checkpoint.is_processed(target.profile_url):
            continue

        existing = profiles.get(target.profile_url)
        if existing and existing.get("xhs_no"):
            checkpoint.mark(target, existing.get("xhs_no"), existing.get("ip"))
            continue

        result = fetch_profile(target)
        if result.status == "ok" and result.xhs_no:
            log_info(
                f"[PROFILE OK] {result.target.commenter_name} {result.xhs_no} {result.ip_location}"
            )
            checkpoint.mark(target, result.xhs_no, result.ip_location)
            merge_into_profiles(profiles, result)
            consecutive_failures = 0
            processed_new += 1
        else:
            log_warn(
                f"[PROFILE FAIL] {target.commenter_name} {target.profile_url} -> {result.error}"
            )
            consecutive_failures += 1
            if consecutive_failures >= WIND_CONTROL_LIMIT:
                log_warn("[WARN] 连续多条未获取小红书号，疑似风控/限制，任务中断。")
                break

        # ✅ 已移除所有防风控 sleep（这里不再等待）

    save_profiles(profiles, Path(output))
    log_info(f"Saved profile fetch summary to {output}")


# =========================
# result_comments / Mongo：用 profile 映射把评论里的 xhs_no(主页链接) 替换成小红书号
# =========================
def build_profile_map_from_checkpoint() -> Dict[str, str]:
    store = get_pipeline_store()
    entries = (
        store.profiles_data.get("entries")
        if isinstance(store.profiles_data, dict)
        else []
    )
    mapping: Dict[str, str] = {}
    for entry in entries or []:
        if not isinstance(entry, dict):
            continue
        url = (entry.get("url") or "").strip()
        pid = extract_user_id(url)
        xhs_no = (entry.get("xhs_no") or "").strip()
        if pid and xhs_no:
            mapping[pid] = xhs_no
    return mapping


def update_entry(
    node: Dict[str, Any], mapping: Dict[str, str], missing: Dict[str, int]
) -> Tuple[int, int]:
    raw_value = node.get("xhs_no")
    if not isinstance(raw_value, str):
        return 0, 0
    raw_value = raw_value.strip()
    if not raw_value.startswith("http"):
        return 0, 0

    pid = extract_user_id(raw_value)
    if not pid:
        return 0, 0

    mapped = mapping.get(pid)
    if not mapped:
        missing[raw_value] = missing.get(raw_value, 0) + 1
        return 0, 1

    node["xhs_no"] = mapped
    return 1, 1


def update_comment_nodes(
    comments: Iterable[Dict[str, Any]], mapping: Dict[str, str], missing: Dict[str, int]
) -> Tuple[int, int]:
    if not isinstance(comments, list):
        return 0, 0

    updated_total = 0
    processed_total = 0
    for entry in comments:
        if not isinstance(entry, dict):
            continue
        u, p = update_entry(entry, mapping, missing)
        updated_total += u
        processed_total += p

        replies = entry.get("replies")
        if isinstance(replies, list) and replies:
            cu, cp = update_comment_nodes(replies, mapping, missing)
            updated_total += cu
            processed_total += cp

    return updated_total, processed_total


def update_json_comments_with_profiles(
    mapping: Dict[str, str], missing: Dict[str, int]
) -> Tuple[int, int]:
    result_file = Path(RESULT_PATH)
    if not result_file.exists():
        raise FileNotFoundError(f"result file not found: {result_file}")
    payload = json.loads(result_file.read_text(encoding="utf-8"))

    cards = payload.get("cards") or []
    updated = 0
    processed = 0
    for card in cards:
        u, p = update_comment_nodes(card.get("comments") or [], mapping, missing)
        updated += u
        processed += p

    atomic_write_json(result_file, payload)
    return updated, processed


def update_mongo_comments(
    mapping: Dict[str, str], missing: Dict[str, int]
) -> Dict[str, int]:
    try:
        from pymongo import MongoClient
    except Exception as exc:
        return {
            "docs_total": 0,
            "docs_updated": 0,
            "updated": 0,
            "processed": 0,
            "message": f"pymongo not available: {exc}",
        }

    try:
        client = MongoClient(MONGO_URI)
        collection = client[MONGO_DB][MONGO_COL]
    except Exception as exc:
        return {
            "docs_total": 0,
            "docs_updated": 0,
            "updated": 0,
            "processed": 0,
            "message": f"failed to connect MongoDB: {exc}",
        }

    docs_total = docs_updated = 0
    updated_total = processed_total = 0

    for doc in collection.find({}, {"comments": 1}):
        docs_total += 1
        comments = doc.get("comments")
        if not isinstance(comments, list) or not comments:
            continue

        u, p = update_comment_nodes(comments, mapping, missing)
        if p:
            processed_total += p
        if u:
            collection.update_one({"_id": doc["_id"]}, {"$set": {"comments": comments}})
            docs_updated += 1
            updated_total += u

    return {
        "docs_total": docs_total,
        "docs_updated": docs_updated,
        "updated": updated_total,
        "processed": processed_total,
        "message": "",
    }


def run_xhs_number_update() -> None:
    profile_map = build_profile_map_from_checkpoint()
    if not profile_map:
        raise RuntimeError(
            "profile mapping 为空：请先运行 --mode profiles 获取小红书号映射。"
        )

    missing_links: Dict[str, int] = {}
    json_updated, json_processed = update_json_comments_with_profiles(
        profile_map, missing_links
    )
    log_info(
        f"JSON: updated {json_updated} entries out of {json_processed} comment profiles in {Path(RESULT_PATH).name}."
    )

    mongo_stats = update_mongo_comments(profile_map, missing_links)
    if mongo_stats["message"]:
        log_warn(f"MongoDB update skipped: {mongo_stats['message']}")
    else:
        log_info(
            "MongoDB: updated {updated} entries out of {processed} comment profiles across {docs_updated}/{docs_total} documents.".format(
                **mongo_stats
            )
        )

    if missing_links:
        total_missing = sum(missing_links.values())
        log_warn(
            f"Missing {len(missing_links)} unique profile links (total occurrences: {total_missing})."
        )


def main():
    parser = argparse.ArgumentParser(
        description="XiaoHongShu 评论抓取 / Profile 补全 / 数据更新工具（已移除防风控等待）"
    )
    parser.add_argument(
        "--mode",
        choices=["comments", "profiles", "update", "full"],
        default="comments",
        help="comments=抓评论；profiles=抓主页信息；update=用映射更新结果；full=全流程",
    )
    parser.add_argument(
        "--profile-limit",
        type=int,
        default=0,
        help="profiles 模式最多抓取多少个用户（0 表示不限制）",
    )
    args = parser.parse_args()

    if args.mode in ("comments", "full"):
        runner = XiaoHongShuRunner()
        runner.run(pause_on_finish=(args.mode != "full"))

    if args.mode in ("profiles", "full"):
        run_profile_fetch(limit=args.profile_limit)

    if args.mode in ("update", "full"):
        run_xhs_number_update()


if __name__ == "__main__":
    main()
