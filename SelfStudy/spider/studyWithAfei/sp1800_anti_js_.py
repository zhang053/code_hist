"""
js逆向
正常查找内容,发现内容不在初始html里,寻找ajax
点击翻页查找ajax链接

通过响应发现,数据被加密了

第二个例子 https://www.qtfm.cn/
点击每一个音频,查看请求发现,每个音频链接的 playroad 中有sign值 --> js加密

查找加密的java script

请求ajax,不通过curl方式
正常请求
拿到一串加密之后的数据,浏览器拿到的也是加密的,通过html寻找解密js的代码
# ajax里面的值有一个V的值

查找方式
html页面本身对加密数据进行解密,解密之后得到的是json数据
json数据是一串字符
在python中,会对json字符串进行处理,转换成字典使用(json.loads)

js同样会把json转换成字典, 转换方法: (JSON.parse)
寻找JSON.parse

javascript断点, 停在JSON.parse后一行, 就是执行过之后带入好数值之后

鼠标移动到解密函数上, 点击 functionLocation 可以跳转到解密函数的位置

把函数复制到程序里想办法运行js函数, 无法通过html程序运行, 因为没有意义

---> 需要安装好nodejs

然后运行js文件, 一个一个找用到的函数, 去补全

加密方法有几种方法,
例子中 使用的是AES加密
特点是需要 iv mode padding
nodejs中针对AES加密解密的, 使用crypto-js模块
"""
