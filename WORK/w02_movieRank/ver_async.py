import asyncio
import json
import os
import re
from typing import Optional

import aiohttp
from bs4 import BeautifulSoup


class MovieRankAsync:
    def __init__(self):
        self.cookies = {}
        self.headers = {}

        self.base_url = "https://filmarks.com"
        self.genres_file = "filmarks_genres.json"
        self.checkpoint_file = "checkpoint.json"

        # ジャンル別保存フォルダ
        self.output_dir = "genre_movies"
        os.makedirs(self.output_dir, exist_ok=True)

        # None の場合は各ジャンルを最後のページまで取得
        self.max_pages_per_genre = None

        # 同時実行数
        self.max_concurrent_genres = 15

        # リクエスト間隔（必要なら調整）
        self.sleep_seconds = 0.1

        # checkpoint
        self.completed_urls = set()
        self.load_checkpoint()

        # 非同期ロック
        self.checkpoint_lock = asyncio.Lock()
        self.file_lock = asyncio.Lock()
        self.print_lock = asyncio.Lock()

    # =========================
    # ファイル読み書き
    # =========================
    def load_genres(self):
        with open(self.genres_file, "r", encoding="utf-8") as f:
            return json.load(f)

    def load_checkpoint(self):
        """
        checkpoint を読み込む
        """
        if os.path.exists(self.checkpoint_file):
            try:
                with open(self.checkpoint_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                self.completed_urls = set(data.get("completed_urls", []))
            except Exception as e:
                print(f"checkpoint の読み込み失敗: {e}")
                self.completed_urls = set()
        else:
            self.completed_urls = set()

    def save_checkpoint_sync(self):
        """
        checkpoint を保存する（同期処理）
        """
        data = {"completed_urls": sorted(self.completed_urls)}
        with open(self.checkpoint_file, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    async def save_checkpoint(self):
        """
        checkpoint を保存する（非同期ラッパー）
        """
        async with self.checkpoint_lock:
            await asyncio.to_thread(self.save_checkpoint_sync)

    def sanitize_filename(self, name):
        """
        ファイル名に使えない文字を置換する
        """
        if not name:
            return "unknown"
        name = re.sub(r"\(\d+件\)", "", name).strip()
        name = re.sub(r'[\\/:*?"<>|]', "_", name)
        name = re.sub(r"\s+", "_", name)
        return name

    def get_genre_output_path(self, genre_info):
        """
        ジャンルごとの保存先ファイルパスを返す
        例: 44_戦争.json
        """
        genre_id = str(genre_info.get("genre_id", "unknown"))
        genre_name = self.sanitize_filename(genre_info.get("name", "unknown"))
        return os.path.join(self.output_dir, f"{genre_id}_{genre_name}.json")

    def load_genre_results_sync(self, genre_info):
        """
        対象ジャンルの既存結果を読み込む（同期処理）
        """
        path = self.get_genre_output_path(genre_info)

        if os.path.exists(path):
            try:
                with open(path, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception as e:
                print(f"ジャンルファイルの読み込み失敗: {path} | {e}")
                return []
        return []

    async def load_genre_results(self, genre_info):
        """
        対象ジャンルの既存結果を読み込む（非同期ラッパー）
        """
        return await asyncio.to_thread(self.load_genre_results_sync, genre_info)

    def save_genre_results_sync(self, genre_info, results):
        """
        対象ジャンルの結果を保存する（同期処理）
        """
        path = self.get_genre_output_path(genre_info)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(results, f, ensure_ascii=False, indent=2)

    async def save_genre_results(self, genre_info, results):
        """
        対象ジャンルの結果を保存する（非同期ラッパー）
        """
        async with self.file_lock:
            await asyncio.to_thread(self.save_genre_results_sync, genre_info, results)

    # =========================
    # ユーティリティ
    # =========================
    def extract_declared_count(self, genre_name):
        """
        例: 'アニメ(5836件)' から 5836 を抽出する
        """
        if not genre_name:
            return None

        match = re.search(r"\((\d+)件\)", genre_name)
        if match:
            return int(match.group(1))
        return None

    def build_existing_keys_for_genre(self, genre_results):
        """
        既存データの重複判定用キー集合を作成する
        同一映画が別ジャンルに出る可能性があるため、
        movie_id と source_genre_id と page_url の組で管理する
        """
        existing = set()
        for item in genre_results:
            key = (
                item.get("movie_id"),
                item.get("source_genre_id"),
                item.get("page_url"),
            )
            existing.add(key)
        return existing

    async def safe_print(self, message: str):
        """
        複数タスクが同時に print して表示が崩れないようにする
        """
        async with self.print_lock:
            print(message)

    # =========================
    # リクエスト
    # =========================
    async def fetch_html(self, session: aiohttp.ClientSession, url: str) -> str:
        """
        単一ページの HTML を取得する
        """
        async with session.get(
            url,
            headers=self.headers,
            cookies=self.cookies,
            timeout=aiohttp.ClientTimeout(total=30),
        ) as resp:
            resp.raise_for_status()
            return await resp.text()

    # =========================
    # 解析
    # =========================
    def parse_meta_json(self, attr_text):
        """
        data-clip / data-mark の JSON を解析する
        """
        if not attr_text:
            return {}

        try:
            return json.loads(attr_text)
        except json.JSONDecodeError:
            return {}

    def parse_rating(self, card):
        """
        評価スコアを取得する
        """
        rating_tag = card.select_one("div.c-rating__score")
        if rating_tag is None:
            return None

        text = rating_tag.get_text(strip=True)
        if not text:
            return None

        try:
            return float(text)
        except ValueError:
            return None

    def parse_genres(self, card):
        """
        作品自身のジャンル一覧を取得する
        ul.genres の中に複数の li がある可能性がある
        """
        genres = []
        genre_links = card.select("ul.genres li a")

        for a in genre_links:
            name = a.get_text(strip=True)
            if name:
                genres.append(name)

        return genres

    def parse_one_card(self, card, genre_info, page_url, page_no, index_in_page):
        """
        単一カードを解析する
        """
        title_tag = card.select_one("h3.p-content-cassette__title")
        title = title_tag.get_text(strip=True) if title_tag else None

        clip_meta = self.parse_meta_json(card.get("data-clip"))
        mark_meta = self.parse_meta_json(card.get("data-mark"))

        rating = self.parse_rating(card)
        genres = self.parse_genres(card)

        return {
            "movie_id": clip_meta.get("movie_id") or mark_meta.get("movie_id"),
            "title": title,
            "rating": rating,
            "clip_count": clip_meta.get("count"),
            "mark_count": mark_meta.get("count"),
            "genres": genres,
            "source_genre_id": genre_info.get("genre_id"),
            "source_genre_name": genre_info.get("name"),
            "source_genre_url": genre_info.get("url"),
            "page_url": page_url,
            "page_no": page_no,
            "index_in_page": index_in_page,
        }

    def parse_current_page(self, html, genre_info, page_url, page_no):
        """
        HTML からページ内のカードをすべて解析する
        """
        soup = BeautifulSoup(html, "html.parser")

        grid = soup.select_one("div.p-contents-grid")
        if grid is None:
            return []

        cards = grid.find_all("div", class_="js-cassette", recursive=False)

        page_results = []
        for idx, card in enumerate(cards, start=1):
            item = self.parse_one_card(card, genre_info, page_url, page_no, idx)
            page_results.append(item)

        return page_results

    def get_next_page_url_from_html(self, html) -> Optional[str]:
        """
        HTML から次ページ URL を取得する
        次ページがない場合は None を返す
        """
        soup = BeautifulSoup(html, "html.parser")

        next_tag = soup.select_one("a[rel='next']")
        if next_tag is None:
            return None

        href = next_tag.get("href")
        if not href:
            return None

        href = str(href)
        if href.startswith("/"):
            href = self.base_url + href

        return href

    # =========================
    # ジャンル単位クロール
    # =========================
    async def crawl_one_genre(self, session: aiohttp.ClientSession, genre_info):
        """
        単一ジャンルの全ページを取得する
        ジャンルごとに別ファイルへ保存する
        """
        genre_id = genre_info.get("genre_id")
        genre_name = genre_info.get("name")
        genre_url = genre_info.get("url")

        output_path = self.get_genre_output_path(genre_info)

        await self.safe_print(
            f"\n========== ジャンル開始: {genre_name} | genre_id={genre_id} =========="
        )
        await self.safe_print(f"[FILE] {output_path}")

        genre_results = await self.load_genre_results(genre_info)
        existing_keys = self.build_existing_keys_for_genre(genre_results)

        await self.safe_print(f"[INFO] 既存件数: {len(genre_results)}")

        current_url = f"{genre_url}?page=1"
        page_no = 1

        while current_url:
            if (
                self.max_pages_per_genre is not None
                and page_no > self.max_pages_per_genre
            ):
                break

            if current_url in self.completed_urls:
                await self.safe_print(
                    f"[SKIP] genre_id={genre_id} page={page_no} | {current_url}"
                )

                next_page_no = page_no + 1
                if (
                    self.max_pages_per_genre is not None
                    and next_page_no > self.max_pages_per_genre
                ):
                    break

                current_url = f"{genre_url}?page={next_page_no}"
                page_no = next_page_no
                continue

            try:
                await self.safe_print(f"[GET ] genre_id={genre_id} page={page_no}")
                html = await self.fetch_html(session, current_url)
            except Exception as e:
                await self.safe_print(f"[ERROR] リクエスト失敗 | {current_url} | {e}")
                break

            try:
                page_results = self.parse_current_page(
                    html, genre_info, current_url, page_no
                )
            except Exception as e:
                await self.safe_print(f"[ERROR] 解析失敗 | {current_url} | {e}")
                break

            new_count = 0
            for item in page_results:
                key = (
                    item.get("movie_id"),
                    item.get("source_genre_id"),
                    item.get("page_url"),
                )
                if key not in existing_keys:
                    genre_results.append(item)
                    existing_keys.add(key)
                    new_count += 1

            # 1ページ完了ごとに checkpoint とファイルを保存する
            self.completed_urls.add(current_url)
            await self.save_checkpoint()
            await self.save_genre_results(genre_info, genre_results)

            await self.safe_print(
                f"[DONE] genre_id={genre_id} page={page_no} | 追加 {new_count} 件"
            )

            next_url = self.get_next_page_url_from_html(html)
            if not next_url:
                break

            current_url = next_url
            page_no += 1

            if self.sleep_seconds > 0:
                await asyncio.sleep(self.sleep_seconds)

        declared_count = self.extract_declared_count(genre_name)
        actual_count = len(genre_results)

        await self.safe_print(
            f"[CHECK] {genre_name} | JSON件数={declared_count} | 取得件数={actual_count}"
        )

    # =========================
    # 全ジャンルクロール
    # =========================
    async def crawl_all_genres(self):
        """
        filmarks_genres.json の順番で全ジャンルを取得する
        ジャンル単位で非同期実行する
        """
        genres = self.load_genres()

        await self.safe_print(f"ジャンル総数: {len(genres)}")
        await self.safe_print(f"checkpoint 件数: {len(self.completed_urls)}")
        await self.safe_print(f"同時実行数: {self.max_concurrent_genres}")

        connector = aiohttp.TCPConnector(limit=20, ssl=False)

        semaphore = asyncio.Semaphore(self.max_concurrent_genres)

        async with aiohttp.ClientSession(connector=connector) as session:

            async def worker(idx, genre_info):
                genre_name = genre_info.get("name")
                genre_id = genre_info.get("genre_id")

                async with semaphore:
                    await self.safe_print(
                        f"\n##### {idx}/{len(genres)} | {genre_name} | genre_id={genre_id} #####"
                    )
                    await self.crawl_one_genre(session, genre_info)

            tasks = [
                asyncio.create_task(worker(idx, genre_info))
                for idx, genre_info in enumerate(genres, start=1)
            ]

            await asyncio.gather(*tasks)

        await self.safe_print("\n========== 全ジャンル取得完了 ==========")
        await self.safe_print(f"checkpoint 記録数: {len(self.completed_urls)}")


if __name__ == "__main__":
    mr = MovieRankAsync()
    asyncio.run(mr.crawl_all_genres())
