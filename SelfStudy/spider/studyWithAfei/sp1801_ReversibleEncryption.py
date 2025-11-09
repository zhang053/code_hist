"""
不可逆加密:
    md5, sha1,sha256,sha512

作用：不管内容多少几个字，几个GB，用md5 加密都是32位
    用来验证文件包的完整，如果有误差，加密后的md5值会不一样，如果一样就是完整


"""

import hashlib

s = "你好啊"  # 准备加密的字符串

# md5 加密 --> 128为二进制数据(转换成16进制)
md5 = hashlib.md5(s.encode()).hexdigest()
print(md5)

# sha1 加密，160位二进制
sha1 = hashlib.sha1(s.encode()).hexdigest()
print(md5)

# sha256, 256位二进制
sha256 = hashlib.sha1(s.encode()).hexdigest()
print(sha256)

# sha512, 512位二进制
sha512 = hashlib.sha1(s.encode()).hexdigest()
print(sha512)
