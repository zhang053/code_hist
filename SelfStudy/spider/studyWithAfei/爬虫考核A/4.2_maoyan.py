# https://www.maoyan.com/
# https://piaofang.maoyan.com/dashboard

from playwright.sync_api import sync_playwright
from fontTools.ttLib import TTFont
from PIL import Image, ImageDraw, ImageFont
from openpyxl import Workbook
import io
import ddddocr

# 版本兼容垫片
if not hasattr(Image, "ANTIALIAS"):
    Image.ANTIALIAS = Image.Resampling.LANCZOS


class MaoYan:
    def __init__(self):
        self.url = "https://piaofang.maoyan.com/dashboard"
        self.page = None
        self.font_file = "4.2_maoyan_font.woff"
        self.font_map = {".": ".", "万": "万"}
        self.ocr = ddddocr.DdddOcr()
        self.timeStamp = None
        self.index = None
        self.font_url = None
        self.rows = []

    def get_font_cmap(self):
        font = TTFont(self.font_file)
        cmap = font.getBestCmap()
        return cmap.keys()

    def build_font_map(self):
        keys = self.get_font_cmap()
        for key in keys:
            img = self.draw_img((key))
            res = self.img_ocr(img)
            self.font_map[chr(key)] = res

    def draw_img(self, key):
        img = Image.new("RGB", (100, 100), (255, 255, 255))
        draw = ImageDraw.Draw(img)
        draw.text(
            (20, 20),
            chr(key),
            font=ImageFont.truetype(self.font_file, 60),
            fill=(0, 0, 0),
        )
        buf = io.BytesIO()
        img.save(buf, format="PNG")
        img_bytes = buf.getvalue()
        return img_bytes

    def img_ocr(self, img):
        return self.ocr.classification(img)

    def decode_font(self, price):
        r = ""
        for p in price:
            r += self.font_map[p]
        return r

    def get_data(self):
        content = self.page.locator(".movielist > table > tbody > tr")
        for i in content.all():
            # 电影名称
            movie_name = i.locator(".moviename-name")
            # print(movie_name.text_content())
            # 电影票房
            movie_num = i.locator(".mtsi-num")
            movie_num = self.decode_font(movie_num.text_content())
            # print(movie_num)
            # 票房占比
            rate = i.locator("td:nth-child(3)")
            # print(rate.text_content())
            # 排片场数
            session = i.locator(".last-col")
            # print(session.text_content())

            self.rows.append(
                [
                    movie_name.text_content(),
                    movie_num,
                    rate.text_content(),
                    session.text_content(),
                ]
            )

    def save_to_excel(self):
        filename = "4.2_maoyan_result.xlsx"
        wb = Workbook()
        ws = wb.active
        ws.title = "票房数据"

        # 表头
        ws.append(["电影名称", "综合票房", "票房占比", "排片场次"])

        # 数据行
        for row in self.rows:
            ws.append(row)

        wb.save(filename)
        print(f"数据已保存到 {filename}")

    def run(self):
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=False)
            self.page = browser.new_page()
            # self.page.goto(self.url)
            # self.page.wait_for_timeout(5000)

            with self.page.expect_response(lambda r: ".woff" in r.url) as font_info:
                self.page.goto(self.url)
            resp = font_info.value
            self.font_url = resp.url
            font_bytes = resp.body()
            with open(self.font_file, "wb") as f:
                f.write(font_bytes)
            print("字体下载成功:", self.font_url)

            # self.download_font()  # 获取加密字体文件
            self.build_font_map()
            self.get_data()
            self.save_to_excel()

            self.page.wait_for_timeout(500320)


if __name__ == "__main__":
    maoyan = MaoYan()
    maoyan.run()
