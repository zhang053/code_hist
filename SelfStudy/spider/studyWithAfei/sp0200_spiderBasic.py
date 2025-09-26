"""
爬虫的基本工作流程 (简明+深入讲解):

1. 发起请求
   - 引入包 (常用 requests / httpx)
   - 定义 url (目标网站地址)
   - 定义请求头 headers (伪装浏览器, 防止被识别为爬虫)
   - 使用 get/post 发起请求 (取数据 or 提交表单)
   - 验证 http 状态码 (200=成功, 403=拒绝, 404=不存在)

   👉 深入: 有些网站需要 cookies / session / 代理(ip池) 才能正常访问。

2. 获取原始数据
   - 可能是 HTML 文档 / 纯文本 / JSON / XML / 图片 / 视频 / 音频
   - 响应体 response.text / response.content

   👉 深入: 如果是 JSON，可以直接解析成字典；如果是二进制文件(图片/视频)，要用 .content 保存。

3. 提取数据 (解析想要的内容)
   - 正则 (快速匹配, 但不适合复杂 HTML)
   - xpath (强大, 定位精准, 类似文件路径)
   - BeautifulSoup(bs4) (语法简单, 适合新手)
   - 其他: PyQuery, lxml, 正则+DOM混用

   👉 深入: 大型网站可能有动态加载数据 → 需要 selenium / playwright 来模拟浏览器。

4. 存储数据
   - 存入数据库 (MySQL, MongoDB, SQLite)
   - 存成本地文件 (.txt, .csv, .xlsx, .json)
   - 图片/视频: 二进制保存

   👉 深入: 数据量小时用本地文件，大规模数据建议数据库 + 分布式存储。
"""
