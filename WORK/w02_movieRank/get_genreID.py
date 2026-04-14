import json
import csv
import re
from pathlib import Path

import requests
from bs4 import BeautifulSoup


BASE_URL = "https://filmarks.com"
PAGE_URL = "https://filmarks.com/list/genre/8"

# 你给的结构里，分类链接大致在这个区域
SELECTOR = "div.p-sidebar nav ul li h3 a"

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/135.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "ja,en-US;q=0.9,en;q=0.8",
}


def extract_genre_id(href: str) -> str:
    """
    从 /list/genre/61 这种 href 中提取 61
    """
    match = re.search(r"/list/genre/(\d+)", href)
    return match.group(1) if match else ""


def fetch_html(url: str) -> str:
    """
    请求页面并返回 HTML
    """
    resp = requests.get(url, headers=HEADERS, timeout=20)
    resp.raise_for_status()
    return resp.text


def parse_genres(html: str) -> list[dict]:
    """
    解析分类信息
    """
    soup = BeautifulSoup(html, "html.parser")
    items = []

    for a in soup.select(SELECTOR):
        name = a.get_text(strip=True)
        href = a.get("href", "").strip()

        if not href:
            continue

        # 拼接完整链接
        full_url = href if href.startswith("http") else BASE_URL + href
        genre_id = extract_genre_id(href)

        items.append(
            {
                "name": name,
                "genre_id": genre_id,
                "href": href,
                "url": full_url,
            }
        )

    # 去重，防止重复抓到
    deduped = []
    seen = set()
    for item in items:
        key = (item["genre_id"], item["name"], item["href"])
        if key not in seen:
            seen.add(key)
            deduped.append(item)

    return deduped


def save_json(data: list[dict], file_path: Path) -> None:
    with file_path.open("w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def save_csv(data: list[dict], file_path: Path) -> None:
    with file_path.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["name", "genre_id", "href", "url"])
        writer.writeheader()
        writer.writerows(data)


def main() -> None:
    html = fetch_html(PAGE_URL)
    genres = parse_genres(html)

    if not genres:
        print("没有抓到分类数据，请检查页面结构或选择器。")
        return

    save_json(genres, Path("filmarks_genres.json"))
    save_csv(genres, Path("filmarks_genres.csv"))

    print(f"抓取完成，共 {len(genres)} 条分类。")
    for item in genres:
        print(item)


if __name__ == "__main__":
    main()
