from playwright.sync_api import sync_playwright
import base64
import json
import requests
import re
import time
import random
from ddddocr import DdddOcr
from PIL import Image

if not hasattr(Image, "ANTIALIAS"):
    Image.ANTIALIAS = Image.Resampling.LANCZOS


# 打码平台api 因为不需要每次都创建，所以放在class的外面
def base64_api(uname, pwd, img, typeid):
    with open(img, "rb") as f:
        base64_data = base64.b64encode(f.read())
        b64 = base64_data.decode()
    data = {"username": uname, "password": pwd, "typeid": typeid, "image": b64}
    result = json.loads(requests.post("http://api.ttshitu.com/predict", json=data).text)
    if result["success"]:
        return result["data"]["result"]
    else:
        # ！！！！！！！注意：返回 人工不足等 错误情况 请加逻辑处理防止脚本卡死 继续重新 识别
        return result["message"]
    return ""


class Geetest:
    def __init__(self):
        self.page = None
        self.bg_img = "sp2804_temp_captcha.png"
        # 只需要进行测量，不需要ocr识别，比如识别文字之类的
        self.det = DdddOcr()

    # 点击滑块验证部分的按钮
    def click_slider_btn(self):
        page = self.page
        # 点击滑块部分的按钮
        page.click(".tab-item-1")
        page.click(".geetest_btn_click")
        page.wait_for_timeout(1500)

    # # 打码平台方案
    def get_offset_DamaPingtai(self):
        page = self.page
        bg_img = page.locator(".geetest_bg").get_attribute("style")
        p = re.compile(r'url\("(.*?)"\)')
        img_url = p.findall(bg_img)[0]
        resp = requests.get(img_url)
        with open(self.bg_img, "wb") as f:
            f.write(resp.content)
        result = base64_api(
            uname="fei53498870", pwd="Fei53498870", img=self.bg_img, typeid=33
        )
        return result

    # 使用ddddocr的方案
    def get_offset_ddddocr(self):
        # 需要两个图片参数，缺口图和背景图
        page = self.page
        bg_img = page.locator(".geetest_bg").get_attribute("style")
        target_img = page.locator(".geetest_slice_bg").get_attribute("style")
        p = re.compile(r'url\("(.*?)"\)')
        bg_img_url = p.findall(bg_img)[0]
        target_img_url = p.findall(target_img)[0]
        bg_img_bytes = requests.get(bg_img_url).content
        target_img_bytes = requests.get(target_img_url).content

        # 目标图片，背景图片
        result = self.det.slide_match(target_img_bytes, bg_img_bytes)

        return result

    # 拖拽滑块
    def drag_slider(self, offset):
        page = self.page
        slider = page.locator(".geetest_btn")
        # 获取滑块位置
        location = slider.bounding_box()
        # 初始位置
        start_x = location["x"] + 10
        start_y = location["y"] + 10
        # 因为图片左上角并不是真正的图形的起始，有间距
        offset -= 13
        # 位移值
        x_ = 0
        # 移动到位置
        page.mouse.move(x=start_x, y=start_y)
        # 按下左键
        page.mouse.down()
        # 移动
        while 1:
            x_ += random.randint(3, 8)
            x_ = min(x_, offset)
            x = start_x + x_
            y = start_y
            page.mouse.move(x=x, y=y)
            if x_ == offset:
                break
            time.sleep(0.05)
        # 抬起
        page.mouse.up()

    def run(self):
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=False)
            context = browser.new_context()
            page = context.new_page()
            self.page = page
            page.set_viewport_size({"width": 1100, "height": 620})
            page.goto("https://www.geetest.com/adaptive-captcha")

            page.wait_for_timeout(1000)

            self.click_slider_btn()
            # 寻找缺口位置
            offset = self.get_offset_ddddocr()
            print(offset)
            # 根据获取到的位置，拖拽滑块
            # self.drag_slider(int(offset))

            page.wait_for_timeout(137204)


if __name__ == "__main__":
    gt = Geetest()
    gt.run()
