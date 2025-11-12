"""
嵌套iframe的处理
    html中一个元素的名字
    是起到框架的作用
        在一个网页中插入(嵌套)另一个网页
        <iframe src="https://xui.ptlogin2.qq.com/cgi-bin/xlogin?proxy_url=https%3A//qzs.qq.com/qzone/v6/portal/proxy.html&amp;daid=5&amp;&amp;>
        </iframe>

使用PW来处理嵌套
"""

from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browse = p.chromium.launch(headless=False)
    page = browse.new_page()
    page.set_viewport_size({"width": 1000, "height": 600})
    page.goto("https://qzone.qq.com/")

    # 先找到iframe标签
    iframe = page.frame_locator("#login_frame")
    # 再找元素进行点击
    iframe.locator("#switcher_plogin").click()
    #
    page.wait_for_timeout(10000000)
