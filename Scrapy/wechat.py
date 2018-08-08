
import requests
from bs4 import  BeautifulSoup

def getHeader():
    header= {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,image/wxpic,image/sharpp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip,deflate',
        'Accept-Language': 'zh-CN,zh;q=0.8',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Host': 'mp.weixin.qq.com',
        'Origin': 'http://mp.weixin.qq.com',
        'User-Agent': 'Mozilla/5.0 (Linux; Android 5.0.2; Lenovo A3580 Build/LRX22G) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/37.0.0.0 Mobile Safari/537.36 MicroMessenger/6.3.25.861 NetType/WIFI Language/zh_CN'
    }
    return header

urlPage = 'https://mp.weixin.qq.com/s?__biz=MzA5MDM1MTcyNQ==&mid=2657245284&idx=1&sn=74c47fbb4de49162da869abf760b34f8&chksm=8b9a0966bced80707433ef108969d5ba9dcd4b67534233315f5dcac733c00cbcb997f8028f73&scene=0&ascene=7&devicetype=android-21&version=26051034&nettype=WIFI&abtest_cookie=AwABAAoACwAMAAMAPoseACSXHgDDmB4AAAA%3D&lang=zh_CN&pass_ticket=5TxsxtXFP26Y56fD%2B91sPLAXUHOTQEy7w0ulO4%2B5bqfLtBsHaMRTgm8svZsUELFp&wx_header=1'





header1 = getHeader()
header1['x-wechat-key'] = 'c730fdc5d91bc1217d465e1b2b9fe875ce7c20cbec939880b6ca96e06fee6eabe6c32f9600fe4e5e01dce4b75eeabb8e606e3237c5ccec7560d9aa2b1c15b7a3f7c6ebd3f3b641adf08f667579f45d99'
header1['x-wechat-uin '] = 'NDAxNTA1NzM4Nw%3D%3D'
header1['Q-UA2'] = 'QV=3&PL=ADR&PR=WX&PP=com.tencent.mm&PPVN=6.5.16&TBSVC=43601&CO=BK&COVC=043927&PB=GE&VE=GA&DE=PHONE&CHID=0&LCID=9422&MO= LenovoA3580 &RL=720*1280&OS=5.0.2&API=21'
header1['Q-Auth'] = '31045b957cf33acf31e40be2f3e71c5217597676a9729f1b'
header1['Q-GUID'] = 'ae6501cd41ee76452a7e046013b788cb'


def parseCookies(str):
    strs = str.split(';')
    obj = {}
    keyList= [str.split('=') for str in strs]
    for [key, val] in keyList:
        obj[key.strip()] = val.strip()
    print(obj)
    return obj

cookies2 = 'pgv_pvi=6375831552; pgv_si=s805576704; rewardsn=; wxtokenkey=777; wxuin=4015057387; devicetype=android-21; version=26051034; lang=zh_CN; pass_ticket=5TxsxtXFP26Y56fD+91sPLAXUHOTQEy7w0ulO4+5bqfLtBsHaMRTgm8svZsUELFp; wap_sid2=COvTw/oOEnBsTThEdl9ZRXhpT055bW54MklmTUZ1QkFLSnJxTmhnTkVyN2tyb1F6QUV2N2JxOTd4THlVLXNIeHJRTGlkOUROay1YYmJhXzFCdTJiaHNUVEtSaXRuZ2dRQnRHM2FtTVgtN3U1Q3lQWUxBN0hBd0FBMKaE5doFOA1AAQ'
cookies2 = parseCookies(cookies2)

res = requests.get(urlPage, headers=header1, cookies=cookies2)

html = BeautifulSoup(res.content, 'html')

cookies = res.cookies

# print(requests.utils)

print(res.cookies.get_dict())
# aaa = requests.utils.dict_from_cookiejar(res.cookies)
# print(aaa)
# help(requests.utils.dict_from_cookiejar)

# print(html)