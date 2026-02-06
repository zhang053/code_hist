"""
版本要求大于3.8

pip install scrapy


# 创建文件
    在要放置的项目文件夹中，打开终端，输入
    scrapy startproject 项目名 (如：sp3003_Mytest)

!!! 注意 scrapy是单独的一个项目，不能通过打开父级来进行修改，一定要确保打开的scrapy文件夹在最外层

# 创建爬虫
    在项目文件夹中，打开终端，输入
    scrapy genspider 爬虫名 网站名
    比如： scrapy genspider douban https://movie.douban.com/top250
    在创建的scrapy文件夹中的spider文件夹中，会生成一个douban.py文件，里面就是爬虫的代码

scrapy的目录结构
Mytest/                 -- 项目文件
    Mytest/           -- scrapy文件夹, 与项目同名
        - spider/           -- 存储具体的爬虫文件
            - __init__.py       -- 初始化文件,包表示
            - douban.py         -- 具体的爬虫文件
        - __init__.py       -- 初始化文件,包表示
        - items.py          -- 定义爬取的数据结构，需要爬取哪些字段，提前在这里定义好
        - middlewares.py    -- 中间件，定义请求的中间处理，比如代理，请求头等，在请求响应开始前结束后额外要执行，通常不需要手动修改
        - pipelines.py      -- 管道，定义数据处理的中间处理，比如数据清洗，数据存储等
        - settings.py       -- 配置文件，定义一些配置，比如请求头，请求间隔，并发，延迟
    scrapy.cfg        -- 项目默认的配置文件，一般不需要修改

编写代码前需要手动配置 settings.py 文件
# ua
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36 Edg/139.0.0.0"
# 机器人协议
ROBOTSTXT_OBEY = False

运行爬虫 -- 在项目中点击运行没有用，需要打开终端，进入项目文件夹，再运行

scrapy crawl 爬虫名  比如：scrapy crawl douban
    scrapy 输出自带日志，打印的内容比较多，可以指定日志等级
    scrapy crawl 爬虫名 --nolog
"""
