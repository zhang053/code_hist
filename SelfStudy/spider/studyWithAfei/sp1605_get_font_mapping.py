"""
# % --> 1       源码 --> 所对应的数字
# + --> 2

获得每个字体的源码

# 绘制对应的字体图片，用于字体识别

计算机无法识别字形的数字内容

需要把字形绘制成图片
然后识别图片,获取图片中的数字内容
"""

# 获取字体的映射关系
# 绘制工具
# pip install fonttools
from fontTools.ttLib import TTFont

# 解析字体
font = TTFont("sp1604_58_font.ttf")
cmap = font.getBestCmap()
# print(cmap)
for key in cmap.keys():
    print(chr(key))

# 1.绘制图片 pip install pillow
from PIL import Image, ImageDraw, ImageFont

# 创建一个图片对象
img = Image.new("RGB", (100, 100), "white")  # 色彩模式 ，图片大小 ， 背景颜色
img.save("sp1606_temp.png")

# 绘制 -- 创建一个画笔
draw = ImageDraw.Draw(img)
# 画什么？画 文字(源码中展示的) 对应的 字形
draw.text(
    (10, 10),  # 位置
    "%",  # 源码中展示的文字
    fill="black",  # 绘制的字体 颜色
    font=ImageFont.truetype("sp1604_58_font.ttf", 50),  # 映射的字形
)
img.save("sp1606_temp.png")
