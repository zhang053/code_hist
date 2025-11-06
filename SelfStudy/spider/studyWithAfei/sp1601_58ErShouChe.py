from lxml import etree
import requests

cookies = {
    "f": "n",
    "commontopbar_new_city_info": "414%7C%E9%95%BF%E6%B2%99%7Ccs",
    "userid360_xml": "E533A1CF16FF91B61183B4FE81AC2262",
    "time_create": "1764926563083",
    "fzq_h": "39c73a5c86ead3809a2488c0f1c3b1da_1762334550972_374da42ea2f04f8fa5a6e59e2662a9b7_3681062357",
    "sessionid": "48892391-9c65-4839-983a-c18c75c3b8c9",
    "id58": "ChBPhWkLF1dGl8KBA5d4Ag==",
    "fzq_js_usdt_infolist_car": "9fe17e2507bacd17de30f50c29967203_1762334552046_6",
    "58tj_uuid": "856126c4-7cbe-4927-a2dd-16b539b22329",
    "new_session": "1",
    "new_uv": "1",
    "utm_source": "",
    "spm": "",
    "init_refer": "",
    "xxzlclientid": "903818ec-b917-45b1-aa2f-1762334559691",
    "wmda_uuid": "c0ff329408bb4433a139607c5d350645",
    "wmda_new_uuid": "1",
    "wmda_report_times": "1",
    "wmda_session_id_1732038237441": "1762334561278-4e3b880a-eb89-4c05-a219-9e0c4c569d8f",
    "wmda_visited_projects": "%3B1732038237441",
    "xxzlxxid": "pfmxyyqQx7i9YeaQxTBK2IIUyuG1YOGxebrfMsSR1Olybh88phCkaCRzKnpdg+SvNU7g",
    "xxzlbbid": "pfmbM3wxMDM2OHwxLjExLjB8MTc2MjMzNDU2MTMzNDI2MjY2OXwxamZCZjZZSW5MbTV4TDl3S0I1MEt6OXhvQnhCSXBLMDJubUl2blNvbHcwPXx8",
    "als": "0",
    "f": "n",
}

headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Accept-Language": "ja,en;q=0.9,en-GB;q=0.8,en-US;q=0.7,zh-CN;q=0.6,zh;q=0.5",
    "Cache-Control": "no-cache",
    "Connection": "keep-alive",
    "Pragma": "no-cache",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "none",
    "Sec-Fetch-User": "?1",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36 Edg/141.0.0.0",
    "sec-ch-ua": '"Microsoft Edge";v="141", "Not?A_Brand";v="8", "Chromium";v="141"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Windows"',
    # 'Cookie': 'f=n; commontopbar_new_city_info=414%7C%E9%95%BF%E6%B2%99%7Ccs; userid360_xml=E533A1CF16FF91B61183B4FE81AC2262; time_create=1764926563083; fzq_h=39c73a5c86ead3809a2488c0f1c3b1da_1762334550972_374da42ea2f04f8fa5a6e59e2662a9b7_3681062357; sessionid=48892391-9c65-4839-983a-c18c75c3b8c9; id58=ChBPhWkLF1dGl8KBA5d4Ag==; fzq_js_usdt_infolist_car=9fe17e2507bacd17de30f50c29967203_1762334552046_6; 58tj_uuid=856126c4-7cbe-4927-a2dd-16b539b22329; new_session=1; new_uv=1; utm_source=; spm=; init_refer=; xxzlclientid=903818ec-b917-45b1-aa2f-1762334559691; wmda_uuid=c0ff329408bb4433a139607c5d350645; wmda_new_uuid=1; wmda_report_times=1; wmda_session_id_1732038237441=1762334561278-4e3b880a-eb89-4c05-a219-9e0c4c569d8f; wmda_visited_projects=%3B1732038237441; xxzlxxid=pfmxyyqQx7i9YeaQxTBK2IIUyuG1YOGxebrfMsSR1Olybh88phCkaCRzKnpdg+SvNU7g; xxzlbbid=pfmbM3wxMDM2OHwxLjExLjB8MTc2MjMzNDU2MTMzNDI2MjY2OXwxamZCZjZZSW5MbTV4TDl3S0I1MEt6OXhvQnhCSXBLMDJubUl2blNvbHcwPXx8; als=0; f=n',
}

response = requests.get(
    "https://cs.58.com/ershouche/", cookies=cookies, headers=headers
)

HTML = etree.HTML(response.text)
lis = HTML.xpath('//div[@id="list"]/ul/li[@class="info"]')

for li in lis:
    title = li.xpath('.//span[@class="info_link"]/text()')[0].strip()
    # print(title)
    # 想要获取其他相关信息，比如价格的时候，发现字体被加密了，显示不是网页字体内容->sp1600
    # 找到对应的字体文件 (font-family , font-face)
