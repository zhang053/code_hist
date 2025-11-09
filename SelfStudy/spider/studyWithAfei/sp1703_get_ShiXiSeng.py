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

# 版本兼容垫片
if not hasattr(Image, "ANTIALIAS"):
    Image.ANTIALIAS = Image.Resampling.LANCZOS


class ShiXiSeng:
    def __init__(self):
        self.html = ""
        self.HTML = ""  # 解析过的html文件
        self.font_file = "sp1705_font.woff"
        self.font_map = {}  # 加密文字对照

    def get_html(self):
        cookies = {
            "__jsluid_s": "ece4385b49ba4f94742a99da50ed0db8",
            "utm_source_first": "PC",
            "utm_source": "PC",
            "utm_campaign": "PC",
            "adClose": "true",
            "Hm_lvt_03465902f492a43ee3eb3543d81eba55": "1762436793",
            "HMACCOUNT": "42F592952044B1A2",
            "adCloseOpen": "true",
            "position": "pc_search_flss",
            "Hm_lpvt_03465902f492a43ee3eb3543d81eba55": "1762436839",
        }
        headers = {
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "accept-language": "ja,en;q=0.9,en-GB;q=0.8,en-US;q=0.7,zh-CN;q=0.6,zh;q=0.5",
            "cache-control": "no-cache",
            "pragma": "no-cache",
            "priority": "u=0, i",
            "referer": "https://www.shixiseng.com/",
            "sec-ch-ua": '"Microsoft Edge";v="141", "Not?A_Brand";v="8", "Chromium";v="141"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "sec-fetch-dest": "document",
            "sec-fetch-mode": "navigate",
            "sec-fetch-site": "same-origin",
            "sec-fetch-user": "?1",
            "upgrade-insecure-requests": "1",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36 Edg/141.0.0.0",
            # 'cookie': '__jsluid_s=ece4385b49ba4f94742a99da50ed0db8; utm_source_first=PC; utm_source=PC; utm_campaign=PC; adClose=true; Hm_lvt_03465902f492a43ee3eb3543d81eba55=1762436793; HMACCOUNT=42F592952044B1A2; adCloseOpen=true; position=pc_search_flss; Hm_lpvt_03465902f492a43ee3eb3543d81eba55=1762436839',
        }
        params = {
            "keyword": "互联网IT",
            "city": "全国",
            "type": "intern",
            "from": "menu",
        }
        response = requests.get(
            "https://www.shixiseng.com/interns",
            params=params,
            cookies=cookies,
            headers=headers,
        )
        print(response)
        self.html = response.text
        self.HTML = etree.HTML(self.html)

    def get_font_file(self):
        p = re.compile(r"\((/interns/iconfonts/file\?rand=.+?)\)")
        font_url = p.findall(self.html)[0]
        font_url = f"https://www.shixiseng.com{font_url}"
        cookies = {
            "__jsluid_s": "ece4385b49ba4f94742a99da50ed0db8",
            "utm_source_first": "PC",
            "utm_source": "PC",
            "utm_campaign": "PC",
            "adClose": "true",
            "Hm_lvt_03465902f492a43ee3eb3543d81eba55": "1762436793",
            "HMACCOUNT": "42F592952044B1A2",
            "adCloseOpen": "true",
            "position": "pc_search_flss",
            "Hm_lpvt_03465902f492a43ee3eb3543d81eba55": "1762436839",
        }
        headers = {
            "accept": "*/*",
            "accept-language": "ja,en;q=0.9,en-GB;q=0.8,en-US;q=0.7,zh-CN;q=0.6,zh;q=0.5",
            "cache-control": "no-cache",
            "origin": "https://www.shixiseng.com",
            "pragma": "no-cache",
            "priority": "u=0",
            "referer": "https://www.shixiseng.com/interns?keyword=%E4%BA%92%E8%81%94%E7%BD%91IT&city=%E5%85%A8%E5%9B%BD&type=intern&from=menu",
            "sec-ch-ua": '"Microsoft Edge";v="141", "Not?A_Brand";v="8", "Chromium";v="141"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "sec-fetch-dest": "font",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36 Edg/141.0.0.0",
            # 'cookie': '__jsluid_s=ece4385b49ba4f94742a99da50ed0db8; utm_source_first=PC; utm_source=PC; utm_campaign=PC; adClose=true; Hm_lvt_03465902f492a43ee3eb3543d81eba55=1762436793; HMACCOUNT=42F592952044B1A2; adCloseOpen=true; position=pc_search_flss; Hm_lpvt_03465902f492a43ee3eb3543d81eba55=1762436839',
        }
        params = {
            "rand": "0.45480785495423737",
        }
        response = requests.get(font_url, cookies=cookies, headers=headers)
        with open(self.font_file, "wb") as f:
            f.write(response.content)

    def decode_font(self):
        font = TTFont(self.font_file)
        cmap = font.getBestCmap()
        # 从字体文件中获得映射关系
        keys = cmap.keys()
        # 通过源码绘制对应的文字
        for key in keys:
            img = Image.new("RGB", (100, 100), (255, 255, 255))
            draw = ImageDraw.Draw(img)
            draw.text(
                (10, 10),
                chr(key),
                font=ImageFont.truetype(self.font_file, 50),
                fill=(0, 0, 0),
            )
            # img.save(f"sp1706_{key}.png")
            buf = io.BytesIO()
            img.save(buf, format="PNG")
            img_bytes = buf.getvalue()
            ocr = ddddocr.DdddOcr()
            result = ocr.classification(img_bytes)
            # print(chr(key), result)
            self.font_map[chr(key)] = result

    def change_word(self, text):
        for w, s in self.font_map.items():
            text = text.replace(w, s)
        return text

    def get_data(self):
        outers = self.HTML.xpath(
            '//*[@id="__layout"]/div/div[2]/div[2]/div[1]/div[1]/div[1]/div'
        )
        for outer in outers:
            title = outer.xpath("./div[1]/div[1]/p[1]/a[1]/text()")[0]
            company = outer.xpath("./div[1]/div[2]/p[1]/a[1]/text()")[0]
            salary = outer.xpath("./div[1]/div[1]/p[1]/span[1]/text()")[0]
            title = self.change_word(title)
            company = self.change_word(company)
            salary = self.change_word(salary)
            print(title, company, salary)

    def run(self):
        self.get_html()  # 获得初始html并解析
        self.get_font_file()  # 获得字体文件
        self.decode_font()  # 解析字体文件
        self.get_data()


if __name__ == "__main__":
    sxs = ShiXiSeng()
    sxs.run()
