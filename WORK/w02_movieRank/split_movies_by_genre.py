import json
import os
from collections import defaultdict

# 入力ファイル
MOVIES_FILE = "movies_data.json"

# 出力フォルダ
OUTPUT_DIR = "output_genres"

os.makedirs(OUTPUT_DIR, exist_ok=True)


def split_movies_by_source_genre():
    print("映画データ読み込み中...")

    with open(MOVIES_FILE, "r", encoding="utf-8") as f:
        movies = json.load(f)

    print(f"総映画件数: {len(movies)}")

    # genreごとに分類
    grouped_movies = defaultdict(list)

    for movie in movies:
        genre_id = movie.get("source_genre_id")

        if genre_id:
            grouped_movies[str(genre_id)].append(movie)

    print(f"分類数: {len(grouped_movies)}")

    # 保存
    for genre_id, movie_list in grouped_movies.items():
        output_path = os.path.join(OUTPUT_DIR, f"{genre_id}.json")

        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(movie_list, f, ensure_ascii=False, indent=2)

        print(f"保存完了: {genre_id}.json ({len(movie_list)}件)")

    print("すべて完了しました。")


if __name__ == "__main__":
    split_movies_by_source_genre()
