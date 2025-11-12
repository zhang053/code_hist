"""
大部分PW的内容 会有内置等待
    比如加载页面的时候，会等待页面加载的完成，再执行代码
    等待加载完后在寻找元素
    page.wait_for_selector("#login")

等待元素的各种状态
page.wait_for_selector("#login", state='visible')  # 可见
page.wait_for_selector("#login", state='hidden')  # 不可见
page.wait_for_selector("#login", state='attached')  # 存在
page.wait_for_selector("#login", state='detached')  # 不存在

等待网络空闲
page.wait_for_load_state('networkidle')
    当请求在5秒内没有新的网络连接时,认为页面加载完成,然后再执行代码

其他页面等待（不常见）
page.wait_for_load_state('domContentLoaded')  # dom加载完成
    等待页面html的标签加载完成(不等待css/js/图片等资源)
page.wait_for_load_state('load')  # 页面全部加载完成，比如截图的时候用到
"""
