from lxml import etree

## 解析文件
# 定义一个解析器
parser = etree.HTMLParser()
# 解析html文件
HTML = etree.parse("0202-1_douban.html", parser)

# 通过xpath语法进行定位
# 找元素，标签，节点
# ele = HTML.xpath("//h1")  # 位置的双斜杠 // 的意思是，在任意层级。意思：所有层级下寻找h1
#  单斜杠 /h1 的意思是，在html总层级下去寻找
# ele = HTML.xpath("//a/span")  # 在所有层级寻找a标签，然后在a标签的子层级寻找span

## 找标签的文本内容
# ele = HTML.xpath("//a/span/text()")
# el1 = HTML.xpath("//h1/text()")
# print(el1)

## 通过各种属性进行定位
# ele = HTML.xpath('//span[@class="title"][.....]/text()')  # 要找的是span
# # [@...] ...写标签名里面的其他筛选条件,还可以写多种属性
# print(ele)

# 找属性的值
# 获取img的src（图片的链接）
# <img width="100" alt="肖申克的救赎" src="https://img3.doubanio.com/view/photo/s_ratio_poster/public/p480747492.jpg">
# fmt: off
ele = HTML.xpath("//img[@alt='肖申克的救赎']/@src")  # 因为不是进行属性的额外描述，要寻找该属性，所以不需要方括号，要找的是src
# element = HTML.xpath("//*[@id = '....']")  # 星号 * 代表寻找任意元素，本身没有意义，在后面通过添加限定条件来寻找

# <a href="https://accounts.douban.com/passport/login?source=movie" class="nav-login" rel="nofollow">登录/注册</a>
# 如果有很多层，很复杂的时候，可以通过id来寻找，因为在html里，id是唯一的
element = HTML.xpath("//div[@id='db-global-nav']/div[@class='bd']/div[@class='top-nav-info']/a/@href")
# print(element)
# fmt: on

# 只想要取一堆中的一个，列表。但是此处的列表的方括号内是顺序，不是下标，所以从1开始
ele2 = HTML.xpath("//div[@class='bd']/div[2]/a/@href")
ele2 = HTML.xpath("//div[@class='bd']/div[last]/a/@href")
ele2 = HTML.xpath('//div[@class="global-nav-items"]/ul/li[last()]/a/text()')
# 获取最后一个 列表方括号里写last（）
# fmt: off

## 只获取其中几个的方法，列表的方括号里写position（）</> 小于/大于， 之间用and 。 这些是xpath里的函数
ele2 = HTML.xpath('//div[@class="global-nav-items"]/ul/li[position()<4]/a/text()') # 第一个到第四个
ele2 = HTML.xpath('//div[@class="global-nav-items"]/ul/li[position()>5]/a/text()') # 从第六个开始获取
ele2 = HTML.xpath('//div[@class="global-nav-items"]/ul/li[position()>2 and position()<8]/a/text()') # 和获取第三个到第七个
# [@。。。] 是严格比对，必须一致

# div[contains(@claa,'....')]  这个是包含选项 , 判断包含的是字符，不是标签名，比如contains来找a，会找到a，aa，aaa等

print(ele2)
