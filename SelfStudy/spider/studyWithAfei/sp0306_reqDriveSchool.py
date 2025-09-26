import requests
from lxml import etree

url = "https://www.jsyks.com/kmy-mnks"

headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36 Edg/139.0.0.0"
}

resp = requests.get(url=url, headers=headers)
resp.encoding = "utf-8"  # 如果编码出现问题，手动修改

# print(resp)
html = etree.HTML(resp.text)

# 想要获取这些习题
# 习题的几大板块：题目，选项，有些题目有图片，正确答案


elem_list = html.xpath("//ul[@class='Content']/li")
for ele in elem_list:
    # 题目
    title = ele.xpath("./strong/text()")[0]

    # 选项
    option = ele.xpath("./b/text()")

    # 有些题目有图片  # strong下的u标签
    # fmt: off
    img = ele.xpath(".//img/@src")  # 获取当前层级中所有的img标签，想要获取标签属性用@
    # fmt: on
    if len(img) > 0:
        img = "https:" + img[0]
    else:
        img = None

    # 这个网页，答案在k选项里边，R代表正确 right， E代表错误 error , 多选题是"A"
    answer = ele.xpath("./@k")[0]

    print(f"题目:{title}")
    print(f"选项:{option}")
    print(f"图片:{img}")
    print(f"答案:{answer}")
    print("-" * 70)
