import requests
from lxml import etree
import re
import base64
import io
from PIL import Image, ImageDraw, ImageFont
from fontTools.ttLib import TTFont
import ddddocr

# 修改报错级别
import onnxruntime as ort

ort.set_default_logger_severity(3)  # 0=VERBOSE,1=INFO,2=WARNING,3=ERROR,4=FATAL

if not hasattr(Image, "ANTIALIAS"):
    Image.ANTIALIAS = Image.Resampling.LANCZOS


class ErShouChe:
    def __init__(self):
        self.html = ""  # 初始html文本
        self.fontName = "sp1702_temp_font.ttf"  # 字体文件路径
        self.ocr = ddddocr.DdddOcr()
        self.font_map = {".": "."}  # 字体映射关系

    # 获取初始html文本
    def get_html(self):
        url = "https://cs.58.com/ershouche/"
        cookies = {
            "f": "n",
            "commontopbar_new_city_info": "414%7C%E9%95%BF%E6%B2%99%7Ccs",
            "userid360_xml": "E533A1CF16FF91B61183B4FE81AC2262",
            "time_create": "1764926563083",
            "fzq_h": "39c73a5c86ead3809a2488c0f1c3b1da_1762334550972_374da42ea2f04f8fa5a6e59e2662a9b7_3681062357",
            "sessionid": "48892391-9c65-4839-983a-c18c75c3b8c9",
            "id58": "ChBPhWkLF1dGl8KBA5d4Ag==",
            "58tj_uuid": "856126c4-7cbe-4927-a2dd-16b539b22329",
            "new_uv": "1",
            "xxzlclientid": "903818ec-b917-45b1-aa2f-1762334559691",
            "wmda_uuid": "c0ff329408bb4433a139607c5d350645",
            "wmda_new_uuid": "1",
            "wmda_visited_projects": "%3B1732038237441",
            "xxzlxxid": "pfmxyyqQx7i9YeaQxTBK2IIUyuG1YOGxebrfMsSR1Olybh88phCkaCRzKnpdg+SvNU7g",
            "als": "0",
            "f": "n",
            "58home": "bj",
            "city": "bj",
            "fzq_js_usdt_infolist_car": "aaaa6ba57d88e8890a7cc80ae92f920a_1762335241125_6",
            "wmda_report_times": "3",
            "xxzlbbid": "pfmbM3wxMDM2OHwxLjExLjB8MTc2MjMzNTI0NDU4MTQxMDkzNHxDUm91b05PeDg1N29RVDVOYllTUzhaNEViYldwQVhKVW1jbmZ2aFdSYUxzPXx8",
        }
        headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "Accept-Language": "ja,en;q=0.9,en-GB;q=0.8,en-US;q=0.7,zh-CN;q=0.6,zh;q=0.5",
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "Pragma": "no-cache",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "none",
            "Sec-Fetch-User": "?1",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36 Edg/141.0.0.0",
            "sec-ch-ua": '"Microsoft Edge";v="141", "Not?A_Brand";v="8", "Chromium";v="141"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            # 'Cookie': 'f=n; commontopbar_new_city_info=414%7C%E9%95%BF%E6%B2%99%7Ccs; userid360_xml=E533A1CF16FF91B61183B4FE81AC2262; time_create=1764926563083; fzq_h=39c73a5c86ead3809a2488c0f1c3b1da_1762334550972_374da42ea2f04f8fa5a6e59e2662a9b7_3681062357; sessionid=48892391-9c65-4839-983a-c18c75c3b8c9; id58=ChBPhWkLF1dGl8KBA5d4Ag==; 58tj_uuid=856126c4-7cbe-4927-a2dd-16b539b22329; new_uv=1; xxzlclientid=903818ec-b917-45b1-aa2f-1762334559691; wmda_uuid=c0ff329408bb4433a139607c5d350645; wmda_new_uuid=1; wmda_visited_projects=%3B1732038237441; xxzlxxid=pfmxyyqQx7i9YeaQxTBK2IIUyuG1YOGxebrfMsSR1Olybh88phCkaCRzKnpdg+SvNU7g; als=0; f=n; 58home=bj; city=bj; fzq_js_usdt_infolist_car=aaaa6ba57d88e8890a7cc80ae92f920a_1762335241125_6; wmda_report_times=3; xxzlbbid=pfmbM3wxMDM2OHwxLjExLjB8MTc2MjMzNTI0NDU4MTQxMDkzNHxDUm91b05PeDg1N29RVDVOYllTUzhaNEViYldwQVhKVW1jbmZ2aFdSYUxzPXx8',
        }
        r = requests.get(url, headers=headers, cookies=cookies)
        self.html = r.text
        print(r)

    # 获取车辆数据信息（标题，信息，价格）
    def get_car_data(self):
        HTML = etree.HTML(self.html)
        lis = HTML.xpath('//div[@id="list"]/ul/li[@class="info"]')
        for li in lis:
            title = li.xpath('.//span[@class="info_link"]/text()')[0].strip()
            price = li.xpath('.//b[@class="info_price fontSecret"]/text()')[0].strip()
            price = self.decode_font(price)
            print(title, price + "万")

    # 字体解密
    def decode_font(self, price):
        # 传过来的三个字符，用for循环挨个解密
        r = ""
        for p in price:
            r += self.font_map[p]
        return r

    # 建立字体映射
    def build_font_map(self):
        keys = self.get_font_cmap()
        for key in keys:
            img = self.draw_img((key))
            res = self.img_ocr(img)
            self.font_map[chr(key)] = res

    # 图片绘制
    def draw_img(self, key):
        img = Image.new("RGB", (100, 100), (255, 255, 255))
        draw = ImageDraw.Draw(img)
        draw.text(
            (20, 20),
            chr(key),
            font=ImageFont.truetype(self.fontName, 60),
            fill=(0, 0, 0),
        )
        buf = io.BytesIO()
        img.save(buf, format="PNG")
        img_bytes = buf.getvalue()
        return img_bytes

    # 获取字体文件的cmap
    def get_font_cmap(self):
        font = TTFont(self.fontName)
        cmap = font.getBestCmap()
        return cmap.keys()

    # 图片识别
    def img_ocr(self, img):
        return self.ocr.classification(img)

    # 字体下载
    def download_font(self):
        p = re.compile(r"data:application/font-ttf;charset=utf-8;base64,(.+?)'")
        font_base64 = p.findall(self.html)[0]
        # print(font_base64)
        data = base64.b64decode(font_base64)
        with open(self.fontName, "wb") as f:
            f.write(data)

    def run(self):
        self.get_html()  # 获取初始html文本
        # print(self.html)
        self.download_font()  # 下载字体
        self.build_font_map()  # 建立字体映射
        self.get_car_data()


if __name__ == "__main__":
    esc58 = ErShouChe()
    esc58.run()
