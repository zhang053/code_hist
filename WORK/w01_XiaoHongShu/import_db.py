import json
from pymongo import MongoClient

# ===== 配置（按你自己的情况改）=====
MONGO_URI = "mongodb://localhost:27017"
DB = "xhs"
COL = "result_comments"

# 你的 JSON 文件路径（你也可以写绝对路径）
SRC_JSON = "result_comments.json"


# 你发的 note_id 列表：按顺序对应 cards[0], cards[1], ...
NOTE_IDS = [
    "66216cbd00000000040196c2",
    "672ca467000000001a035b4d",
    "67320d87000000001b012eb0",
    "67531298000000000702b0ab",
    "6756f5de0000000002026c42",
    "67d6af19000000001203dc9c",
    "67d9515a000000001a00670d",
    "67e13159000000001d01dc08",
    "67e68a65000000001203cf71",
    "6810ad19000000000b014ad8",
    "682f190b000000002202a738",
    "6837fa240000000021018cb6",
    "68415ff6000000000303f1a4",
    "684239a7000000002101bd9d",
    "68553cb4000000001c032058",
    "685a5b1d00000000100113d9",
    "68719b8a000000001703767e",
    "68745160000000001c0305f3",
    "68761a1e0000000011003d5d",
    "688320be00000000170370d9",
    "6891b3810000000025017b2d",
    "68c8d2bf000000001b01cc7a",
    "68dc8a2400000000040076de",
    "68e2860b0000000003020fe9",
    "68ee456c0000000007032a91",
    "68f352bc000000000301e81a",
    "690de11400000000050022a3",
    "69170963000000000703a539",
    "69269085000000001e033d2d",
    "6926b80700000000190261fe",
    "692701f8000000000d0361a9",
    "6948dcdd000000001e03afcc",
    "694e4aa9000000001e00dd18",
    "696a0fc0000000000e03ef7b",
    "697f414e00000000210308b0",
]


def main():
    # 读 JSON
    with open(SRC_JSON, "r", encoding="utf-8") as f:
        data = json.load(f)

    cards = data.get("cards", [])
    print(f"[1] cards 数量 = {len(cards)}")
    print(f"[2] note_id 数量 = {len(NOTE_IDS)}")

    if len(cards) != len(NOTE_IDS):
        print("⚠️ 数量不一致：将只导入前 min(len(cards), len(note_ids)) 条")
    n = min(len(cards), len(NOTE_IDS))

    # 连接 Mongo
    client = MongoClient(MONGO_URI)
    col = client[DB][COL]

    # （可选但推荐）你现在库里只剩 _id 了，建议先清空再导入，避免残留
    # 如果你不想清空，把下一行注释掉即可
    col.delete_many({})
    print("[3] 已清空目标集合，开始导入...")

    ok = 0
    skipped = 0

    for i in range(n):
        note_id = NOTE_IDS[i]
        card = cards[i] or {}

        title = card.get("title")
        comments = card.get("comments", [])

        # 防止写入空卡片（可按你需求调整）
        if not title and not comments:
            skipped += 1
            continue

        # ✅ Mongo 扁平结构：不要 cards 外壳
        doc = {
            "_id": note_id,
            "title": title,
            "comments": comments,
        }

        col.replace_one({"_id": note_id}, doc, upsert=True)
        ok += 1

    print(f"[done] 导入成功 {ok} 条，跳过空数据 {skipped} 条")


if __name__ == "__main__":
    main()
