# 目标图片地址：
# https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTwx1LCSDn-9_D7ZEnibEtEATgFO6f_asr_J0suM8YyoWmdU4Z-EnUn5bX_WmvLLpG5wHM&usqp=CAU
import requests

url = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTwx1LCSDn-9_D7ZEnibEtEATgFO6f_asr_J0suM8YyoWmdU4Z-EnUn5bX_WmvLLpG5wHM&usqp=CAU"
headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36 Edg/139.0.0.0"
}

response = requests.get(url, headers=headers)
print(response)

# 直接保存图片

with open("sp0702_DLpicture.png", "wb") as f:  # 保存的图片是视频都是 "wb"
    f.write(response.content)
