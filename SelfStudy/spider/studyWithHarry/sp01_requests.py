# 服务器，浏览器 http常见状态码
# 1xx:消息已被接受，需要继续处理
# 2xx:成功（200ok）
# 3xx:重定向(302临时转移至新url)
# 4xx:请求错误(404 not found , 可能原因服务器没有这个页面)
# 5xx:服务器错误（502 bad gateway）

import requests

print("hello spider")

url = "https://www.google.com/"
requests.get(url)  # requests.get(url, params=None, **kwargs)       # GET 请求

# referer https://www.google.com/
# user-agent Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36

headers = {
    "referer": "https://www.google.com/",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36",
}

requests.get(url, headers=headers)
