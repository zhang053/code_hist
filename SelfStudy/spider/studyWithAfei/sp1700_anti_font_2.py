# 多次刷新发现，每次的base64加密链接不一样，得到的字体文件不一样，得到的映射关系不一样
# 需要在代码中实现
# 通过外部第三方库进行图像识别，来获得图像和源码的映射关系
# 绘画的库是根据Unicode编码进行绘图

# 图片识别,需要使用第三方库,如ddddocr
# pip install ddddocr
import io
from PIL import Image, ImageDraw, ImageFont
from fontTools.ttLib import TTFont
import ddddocr

# 修改报错级别
import onnxruntime as ort

ort.set_default_logger_severity(3)  # 0=VERBOSE,1=INFO,2=WARNING,3=ERROR,4=FATAL

if not hasattr(Image, "ANTIALIAS"):
    Image.ANTIALIAS = Image.Resampling.LANCZOS

ocr = ddddocr.DdddOcr()


def draw_img(k):
    img = Image.new("RGB", (100, 100), (255, 255, 255))
    draw = ImageDraw.Draw(img)
    draw.text(
        (20, 20),
        chr(k),
        font=ImageFont.truetype("sp1604_58_font.ttf", 60),
        fill=(0, 0, 0),
    )
    # 不需要保存，因为可以直接把字节数据丢给ocr识别
    # img.save(f"sp1701_img_{k}.png")
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    img_bytes = buf.getvalue()

    res = ocr.classification(img_bytes)
    print(chr(k), res)


font = TTFont("sp1604_58_font.ttf")
cmap = font.getBestCmap()
# print(cmap.keys())
for k in cmap.keys():
    draw_img(k)

"""
import ddddocr
from PIL import Image, ImageDraw, ImageFont

if not hasattr(Image, "ANTIALIAS"):
    Image.ANTIALIAS = Image.Resampling.LANCZOS

# 创建ocr对象
ocr = ddddocr.DdddOcr()
# 打开图片，进行识别
with open("sp1701_img_37.png", "rb") as f:
    # 读取图片bytes数据
    img_bytes = f.read()
    # 调用识别方法进行识别
    res = ocr.classification(img_bytes)
    print(res)
"""
