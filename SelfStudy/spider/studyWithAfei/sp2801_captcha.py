"""
    验证码付费平台
# # http://ttshitu.com/user/index.html
# fei53498870
# Fei53498870


https://www.geetest.com/adaptive-captcha

滑动验证码
    一个是需要拖动的图片
    还有一个有缺口的背景图

    # 四、缺口识别
    # 18 : 缺口识别（需要2张图 一张目标图一张缺口图）

    使用id = 18 的方法

"""

# # 付费平台 接入api
"""

# 一、图片文字类型(默认 3 数英混合)：
# 1 : 纯数字
# 1001：纯数字2
# 2 : 纯英文
# 1002：纯英文2
# 3 : 数英混合
# 1003：数英混合2
#  4 : 闪动GIF
# 7 : 无感学习(独家)
# 11 : 计算题
# 1005:  快速计算题
# 16 : 汉字
# 32 : 通用文字识别(证件、单据)
# 66:  问答题
# 49 :recaptcha图片识别
# 二、图片旋转角度类型：
# 29 :  旋转类型
# 1029 :  背景匹配旋转类型 注意：中间小图传到image中，背景图传到imageback 中 imageback模仿image 添加
# 2029 :  背景匹配双旋转类型 注意：中间小图传到image中，背景图传到imageback 中  imageback模仿image 添加
#
# 三、图片坐标点选类型：
# 19 :  1个坐标
# 20 :  3个坐标
# 21 :  3 ~ 5个坐标
# 22 :  5 ~ 8个坐标
# 27 :  1 ~ 4个坐标
# 48 : 轨迹类型
#
# 四、缺口识别
# 18 : 缺口识别（需要2张图 一张目标图一张缺口图）
# 33 : 单缺口识别（返回X轴坐标 只需要1张图）
# 34 : 缺口识别2（返回X轴坐标 只需要1张图）
# 五、拼图识别
# 53：拼图识别
"""
from playwright.sync_api import sync_playwright
import base64
import json
import requests
import re

# def base64_api(uname, pwd, img, typeid):
#     with open(img, "rb") as f:
#         base64_data = base64.b64encode(f.read())
#         b64 = base64_data.decode()
#     data = {"username": uname, "password": pwd, "typeid": typeid, "image": b64}
#     result = json.loads(requests.post("http://api.ttshitu.com/predict", json=data).text)
#     if result["success"]:
#         return result["data"]["result"]
#     else:
#         # ！！！！！！！注意：返回 人工不足等 错误情况 请加逻辑处理防止脚本卡死 继续重新 识别
#         return result["message"]
#     return ""


# if __name__ == "__main__":
#     img_path = "C:/Users/Administrator/Desktop/file.jpg"
#     result = base64_api(uname="fei53498870", pwd="Fei53498870", img=img_path, typeid=18)
#     print(result)

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.set_viewport_size({"width": 1100, "height": 620})

    page.goto("https://www.geetest.com/adaptive-captcha")
    page.click(".tab-item-1")
    page.click(".geetest_btn_click")

    # 可以发现点击后不是立刻出现，需要加几秒延迟等待加载
    page.wait_for_timeout(1500)

    # 获取缺口背景图
    ele_bg = page.locator(".geetest_bg")
    # 会截图到有缺口图案的照片，会导致识别错误
    # 需要一张只有缺口的，还有另一张滑块的图案
    # ele_bg.screenshot(path="sp2802_captchaImg.png")

    # # 使用另一种方法： 发送有背景图片的地址的请求，获取背景图片
    # 获取元素 background-img属性的值
    bg_img = ele_bg.get_attribute("style")
    # print(bg_img)
    # 使用正则获取url, 或者使用引号进行切割，找到第二个
    img_url = re.compile(r'url\("(.*?)"\)')
    img_url = img_url.findall(bg_img)[0]
    print(img_url)
    response = requests.get(img_url)
    with open("sp2802_captchaImg.png", "wb") as f:
        f.write(response.content)

    # 成功获取到图片，使用打码平台api进行识别

    page.wait_for_timeout(7000000)
