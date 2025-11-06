import requests

headers = {
    "Accept": "*/*",
    "Accept-Language": "ja,en;q=0.9,en-GB;q=0.8,en-US;q=0.7,zh-CN;q=0.6,zh;q=0.5",
    "Cache-Control": "no-cache",
    "Connection": "keep-alive",
    "Origin": "https://www.acfun.cn",
    "Pragma": "no-cache",
    "Referer": "https://www.acfun.cn/",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-site",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36 Edg/141.0.0.0",
    "sec-ch-ua": '"Microsoft Edge";v="141", "Not?A_Brand";v="8", "Chromium";v="141"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Windows"',
}

params = {
    "pkey": "ABDDc3CONZKz2YKxpagZOZ1J4UcgbnyMeaQeuNvFTM4X17ir_jq2A7DZ-Mrin_nG49hlEa3qPJO3AP0eY_ptY4ZC7HR-YJsFeQiDMe4yiiGudZyNkpKaCvAZ6oSu2ZGLVnQ4YpCw9RL_4qL2fAQyBSi5ffMbSGFi5sBuCxNJdxQ5VoS7D4wr6IlnuMrJ4y3ZbOMtxwvHvS_IST1hJsbnz6xvABPgezwQr_J_bVifNq5ZiI1_AYdxwSeYFY0V1LgD_54",
    "safety_id": "AAIcFoRjyJws7q73Pl1MwxBQ",
}

response = requests.get(
    "https://tx-safety-video.acfun.cn/mediacloud/acfun/acfun_video/9e0ab2abd5c038ec-ee859ae7e3a73dca02bfd8ef6a786c1a-hls_720p_2.00036.ts",
    params=params,
    headers=headers,
)
print(response)

with open("sp1403_TryToDLts.ts", "wb") as f:
    f.write(response.content)
