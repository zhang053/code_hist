import json
import os
import re
import time
import requests
from bs4 import BeautifulSoup


class MovieRank:
    def __init__(self):
        self.cookies = {}
        self.headers = {}

        self.base_url = "https://filmarks.com"
        self.genres_file = "filmarks_genres.json"
        self.checkpoint_file = "checkpoint.json"

        # ジャンル別保存フォルダ
        self.output_dir = "genre_movies"
        os.makedirs(self.output_dir, exist_ok=True)

        # None の場合は全ページ取得
        self.max_pages_per_genre = None

        # リクエスト間隔
        self.sleep_seconds = 1

        self.response = None
        self.completed_urls = set()

        self.load_checkpoint()

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

    def save_checkpoint(self):
        """
        checkpoint を保存する
        """
        data = {"completed_urls": sorted(self.completed_urls)}
        with open(self.checkpoint_file, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

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

    def load_genre_results(self, genre_info):
        """
        対象ジャンルの既存結果を読み込む
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

    def save_genre_results(self, genre_info, results):
        """
        対象ジャンルの結果を保存する
        """
        path = self.get_genre_output_path(genre_info)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(results, f, ensure_ascii=False, indent=2)

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

    # =========================
    # リクエスト
    # =========================
    def fetch_url(self, url):
        """
        単一ページを取得する
        """
        self.response = requests.get(
            url=url,
            cookies=self.cookies,
            headers=self.headers,
            timeout=20,
        )
        self.response.raise_for_status()

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

    def parse_current_page(self, genre_info, page_url, page_no):
        """
        現在の response からページ内のカードをすべて解析する
        """
        if self.response is None:
            return []

        soup = BeautifulSoup(self.response.text, "html.parser")

        grid = soup.select_one("div.p-contents-grid")
        if grid is None:
            return []

        cards = grid.find_all("div", class_="js-cassette", recursive=False)

        page_results = []
        for idx, card in enumerate(cards, start=1):
            item = self.parse_one_card(card, genre_info, page_url, page_no, idx)
            page_results.append(item)

        return page_results

    def get_next_page_url(self):
        """
        次ページ URL を取得する
        次ページがない場合は None を返す
        """
        if self.response is None:
            return None

        soup = BeautifulSoup(self.response.text, "html.parser")

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
    def crawl_one_genre(self, genre_info):
        """
        単一ジャンルの全ページを取得する
        ジャンルごとに別ファイルへ保存する
        """
        genre_id = genre_info.get("genre_id")
        genre_name = genre_info.get("name")
        genre_url = genre_info.get("url")

        output_path = self.get_genre_output_path(genre_info)

        print(
            f"\n========== ジャンル開始: {genre_name} | genre_id={genre_id} =========="
        )
        print(f"[FILE] {output_path}")

        # 既存のジャンルファイルを読み込む
        genre_results = self.load_genre_results(genre_info)
        existing_keys = self.build_existing_keys_for_genre(genre_results)

        print(f"[INFO] 既存件数: {len(genre_results)}")

        current_url = f"{genre_url}?page=1"
        page_no = 1

        while current_url:
            if (
                self.max_pages_per_genre is not None
                and page_no > self.max_pages_per_genre
            ):
                break

            if current_url in self.completed_urls:
                print(f"[SKIP] genre_id={genre_id} page={page_no} | {current_url}")

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
                print(f"[GET ] genre_id={genre_id} page={page_no}")
                self.fetch_url(current_url)
            except Exception as e:
                print(f"[ERROR] リクエスト失敗 | {current_url} | {e}")
                break

            try:
                page_results = self.parse_current_page(genre_info, current_url, page_no)
            except Exception as e:
                print(f"[ERROR] 解析失敗 | {current_url} | {e}")
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

            # 1ページ完了ごとに保存
            self.completed_urls.add(current_url)
            self.save_checkpoint()
            self.save_genre_results(genre_info, genre_results)

            print(f"[DONE] genre_id={genre_id} page={page_no} | 追加 {new_count} 件")

            next_url = self.get_next_page_url()
            if not next_url:
                break

            current_url = next_url
            page_no += 1
            time.sleep(self.sleep_seconds)

        declared_count = self.extract_declared_count(genre_name)
        actual_count = len(genre_results)

        print(
            f"[CHECK] {genre_name} | JSON件数={declared_count} | 取得件数={actual_count}"
        )

    # =========================
    # 全ジャンルクロール
    # =========================
    def crawl_all_genres(self):
        """
        filmarks_genres.json の順番で全ジャンルを取得する
        """
        genres = self.load_genres()

        print(f"ジャンル総数: {len(genres)}")
        print(f"checkpoint 件数: {len(self.completed_urls)}")

        for idx, genre_info in enumerate(genres, start=1):
            genre_name = genre_info.get("name")
            genre_id = genre_info.get("genre_id")
            print(
                f"\n##### {idx}/{len(genres)} | {genre_name} | genre_id={genre_id} #####"
            )
            self.crawl_one_genre(genre_info)

        print("\n========== 全ジャンル取得完了 ==========")
        print(f"checkpoint 記録数: {len(self.completed_urls)}")


if __name__ == "__main__":
    mr = MovieRank()
    mr.crawl_all_genres()
