import requests
import json
import json
from Crypto.Cipher import AES
import base64
# params = {
#     'params': '5G/g/XDaDjcj0KIHW4a9dsKubkHhEeGI2hMa0rnA/Dv2WTR3PBkegCnd/NKg8R/STtoGzsZMOPKMwKaQlnIHDR7bJVQmI/vhynin1Pzgn7Q6adzso/P7nFfexL8gKY2yPlxp/272Z69zPmLSPIdKDQ==',
#     'encSecKey': 'a7c708ac650f34b5794c737e53814f522031d894529d6ade15e992252b934a552648322e211a96681eefc6cf3d0aba8bf6e39e1cb32c6322c940804e0d1c000a5d4c039003d88425cca2da14200dba18044f63cc4630c6808d4dc219fb22252823b3d0e0c9217175482b0cf354e5b486cae50caaa2166d4f2d61b8aa681166c5'
# }
#
# url = 'https://music.163.com/weapi/search/suggest/web?csrf_token=ef7a88f2683d4c954c36be93fe306756'
#
#
# res = requests.post(url, params)
# print(res.content)



first_param = {
    'csrf_token': '',
    'hlposttag': '</span>',
    'hlpretag': '<span class="s-fc7">',
    'limit': '90',
    'offset': '0',
    's': '王菲',
    'total': 'true',
    'type': '100'
}
first_param = json.dumps(first_param)
# print(first_param)
# first_param = str({"rid":"R_SO_4_1807794","offset":"0","total":"true","limit":"20","csrf_token":"5514a29b40426202083c432bd3cea74f"})
second_param = "010001"
third_param = "00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7b725152b3ab17a876aea8a5aa76d2e417629ec4ee341f56135fccf695280104e0312ecbda92557c93870114af6c9d05c4f7f0c3685b7a46bee255932575cce10b424d813cfe4875d3e82047b97ddef52741d546b8e289dc6935b3ece0462db0a22b8e7"
forth_param = "0CoJUm6Qyw8W8jud"





def get_params():
    iv = "0102030405060708"
    first_key = forth_param
    second_key = 16 * 'F'
    h_encText = AES_encrypt(first_param, first_key, iv)
    h_encText = AES_encrypt(h_encText, second_key, iv)
    return h_encText


def get_encSecKey():
    encSecKey = "61e00f79c1636ef41bd25fc75600b8950e3405524d1f317a12c25d26a02fc1c68f943b0b3de1a698de46a45bc3e655e237bc6814aeed78444ad92b18ef1d184e9d17ee71ec811ead107a8b178445da3dd2feed7c23e3c03eb0eb4203be8b7e5ab5f53b8892a7ee2fdbf2962c52bbb1da0cfdd3d12d9160e3c35d8f14c5039df3"
    return encSecKey


def AES_encrypt(text, key, iv):
    pad = 16 - len(text) % 16
    text = text + pad * chr(pad)
    text = bytes(text, encoding="utf8")
    key = bytes(key, encoding="utf8")
    iv = bytes(iv, encoding="utf8")
    encryptor = AES.new(key, AES.MODE_CBC, iv)
    encrypt_text = encryptor.encrypt(text)
    encrypt_text = base64.b64encode(encrypt_text)


    return bytes.decode(encrypt_text)




headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Host': 'music.163.com',
    'Pragma': 'no-cache',
    'Referer': 'http://music.163.com/',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_4) AppleWebKit/537.36 (KHTML, like Gecko Chrome/59.0.3071.115 Safari/537.36',
    'Cookie': 'vjuids=-33e8afa29.15bc8b7b3ac.0.638abfc0f72cb; _ntes_nnid=386e7746411a5a1fa7b76398ce3be3bf,1493721134014; _ntes_nuid=386e7746411a5a1fa7b76398ce3be3bf; UM_distinctid=15c02114a3a65-06b2423bb27e9a-396a7807-fa000-15c02114a3bd05; __gads=ID=90a50081a25ea422:T=1494999622:S=ALNI_MbGuS0y_mKJ5KMiPGw0vWUgvrjRsQ; _ga=GA1.2.1429244608.1496386112; Province=010; City=010; __s_=1; vjlast=1493721134.1498659391.21; vinfo_n_f_l_n3=e8b2123fb5aea85b.1.1.1494683308646.1494683334950.1498659417706; JSESSIONID-WYYY=E%5CVtEfsCBr0m1gOKSE6hI4J2rhUAY7OlVBa36VMzz83kbY3KdBhGEhvRtV%2FkMddndlAQF1sC%5CKAAfp3xf92mdgeKFa9PE%5Cw%5Cjar%5CQBb5cXsVaCD69YaBPxooxkzrC0%2FKcZjj%2BG5EFxIwwNpPQq%5C9qYJYz2JRmdZY0Vh6nwjKlJ0Xjfqq%3A1499428220638; _iuqxldmzr_=32; __utma=94650624.1429244608.1496386112.1499356470.1499426421.16; __utmb=94650624.3.10.1499426421; __utmc=94650624; __utmz=94650624.1499426421.16.13.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided)'
}

p =  get_params()
params = {
    # 'params': 'GlOTOJIwJybtIKfYm2utw1uP1MiStw47p7nqKLSbuDEFR0Ex9CwvzKAX02qEtBPDUIY1SyUjmA9KsmfyReytoYGpJ2j1Fyc0O5+d3Xmx7f0OQ6+XEGGK6eTKXcnSqCrkkZ/xiZUeepeij2ePEW6poWbWjsfpE6RqG1nifGcp/cqxOh1QL56HppLfikhZJIBFv++OwjDpRU13uXpDIlP9vZKs98dvw7PrKrz+ixcZjcc=',
    'params': 'i77S9ciqV9sW/C9tBuOodDPuJONjJPKRmFod6g7oEYtLSeqB0+HxNAZfabgKTpuQZ6beBgDOERWAq30BXXI1cMEYUdhwk0vOB1H6rgB+3re3GmA11dh+Kt2fIK4ggUx9beyzqa344HJZpfX3CJpACQ==',
    # 'params': p,
    'encSecKey': '72d9761b4a013a3bf713fa9dc0cc41db663c811b9fa785b027b1935dd2ecf077a49330863519ae122dbf1886a9869156a732fb89690adcaf950168e6319189abc0951cda0530e8a243fdbd2878a197e81058365094591d97fbad676a82288c175a1b52ed79449655028f29000505c18fc828e359555498bb8645bd8809feee1b'
}

# url = 'https://music.163.com/weapi/v1/resource/comments/R_SO_4_29713754?csrf_token=ef7a88f2683d4c954c36be93fe306756'
url = 'https://music.163.com/weapi/search/suggest/web?csrf_token=0e588fdea59cf8a96d8e71a5ea9bc301'
res = requests.post(url, data=params, headers = headers)
print(res.content)



