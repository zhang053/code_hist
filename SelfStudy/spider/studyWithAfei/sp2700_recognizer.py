"""
验证码
    字母
    数字
    图片
    汉字
    按顺序点击图片
    拖拽-拼图
    找图片

    大部分大厂的验证码都不好通过代码过
        最好还是手动, 然后通过cookie解决

    通过代码好解决的:
        英文 数字 拼图 滑动 汉字(部分)

解决验证码最基本的原理是 图像识别
    1.免费方案: ddddocr
        精确度不高 (90%), 支持的验证码类型比较少
    2.付费方案
        精确度高
"""

from ddddocr import DdddOcr
from PIL import Image

if not hasattr(Image, "ANTIALIAS"):
    Image.ANTIALIAS = Image.Resampling.LANCZOS

ocr = DdddOcr()
# 读取图片内容
with open("sp2701_temp_image.png", "rb") as f:
    img_bytes = f.read()
    text = ocr.classification(img_bytes)
    print(text)
