# from Crypto.Cipher import AES
# import base64
# import requests
# import json
# import math
# import random
#
#
#
# #cloud search API
#
# # http://music.163.com/weapi/cloudsearch/get/web?csrf_token=e7bc06adf05e442034b44d40bde7a0d3
# #csrf_token: e7bc06adf05e442034b44d40bde7a0d3
# #params: plgWgKsNparYybzITfaaoep93+7PtYqiku1LucQH5Q5PqYIsEuclY3N13BK/p6mrgHq5sBqrAIpTuqtn8fKk9TWUjGmH6MDheBhWfZhGunxi7dXpmdZF/1UZds7L6UypCHiUFR7OciURbununP/uSTl1KPfTOce89IVMbf9jNRQq+IB3CbYF+X4G1COrOoEvnrLZ6IgRYQc1kFpMiCF9GcH33YLXTJWEhEnvLrjuxg2SoS0c+/+9ZE9xMk5h2mGjZfuPeFpS5fvFv4h5NDkTxGAl4WK128JDyA7KY8q79AuBrZ+Z+CfR6yAZgkx3q6qL
# #encSecKey: 2a3b72ab4168d0c19b6ff6287af4ba293ce6ecff431653f00f2097a10f7736048854b9bbec82251f30fd487d55b77035de13cc52b61ee7104f4bc975335f76be3ec5354bd08af4726f3aef6f62c5ad19cd733b85b7c072fdc18ec1974cd9ffe85e5149cb89942b01eb9a096824356d0628936e11ed4b9f0441af5079a1c7db55
#
#
#
#
# # hlposttag:"</span>"
# # hlpretag:"<span class="s-fc7">"
# # limit:90
# # offset:0
# # s:"王菲"
# # total:true
# # type:"100"
#
#
#
#
# url = 'http://music.163.com/weapi/cloudsearch/get/web?csrf_token=71b537daad3b8e5e986ab5759cd2d0f3'
# params = 'gRn9iuqdiKxrLQsW+L6L33cb6FFCeYDuH4n1+C0DeJaMXKS2KvfB/0Qhe80BTkaSW06yfPuV97mDFW5RAy+NXfiSVNPLRSvogjWIM2XtfY5qXoAVYKz4fuKFQcha8gsXURQU6oxMK3fWOqzTdlvhTjwj4c2cgsrvO6fx6wQIVSwFKQmfEaWLY8S1TbetW4aXHivOpa39kAg1Nrvc9Tygryflbw1PaftHujwWbdMG/l0VzXP0E/hrP3OD01+/9Re918iRgj5Nl7gUO6neGyBow3iuX6jr1txNIutbPtsFMY9KUQKDpT6vDMHgceA/IhPe'
# encSecKey = '6cf027ade068bd9144975b918edbe87098e840fd7bd5c083d19787aaf96033850a1b861ae7bff85f761b1054a27a36cab654371e075795250c7a629f85e586f51c6039d5a7d8434a10a42e7f2e3195864ec7fe809e3b5fbe214a67d2cf1625aae27b86ccf284e6939db523ed9cb6b6ca9ce024fc252be815b0f4b2f68843601c'
# # params=  'cyDAGxrta+t6z0lHXHRQKCS9X5f8ytV+Zh+s9W15WJrKV6jhu22JGQV/gjaWzrxfY2BDoWrU09Qq1yaI38Vn91JLD1vtHJJbWzx9x+Hmi30aGoX9g0AVhO8T/+eHThOjTtM1DMugqQSC0KgAkiAfMTDulcykUnPx5TDojYSLQ8bGPEQClG0sPkwNvsbemr0ba3y2eDxUM0I1nrAhqeiscce0x50xVCon5aUG7qDcH3glckvRKQ4yIsdDotK8kvdZyoUpbdBCtxD8sDxtkuGJ1p6uEOOor20AIsPnuvfhBcdxAqikerO+q/xnnqMMq/9T'
# data = {
#     'params': params,
#     'encSecKey': encSecKey
# }
# res = requests.post(url, data=data)
#
# print(res.content)
#
#
#
#
#
#
#
# #
# #
# #
# #
# #
# # p1 = '{"hlpretag":"<span class=\"s-fc7\">","hlposttag":"</span>","s":"王菲","type":"100","offset":"0","total":"true","limit":"90","csrf_token":"3dc1681c21c355c33b789def49e3d189"}'
# # p2 = '010001'
# # p3 = '00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7b725152b3ab17a876aea8a5aa76d2e417629ec4ee341f56135fccf695280104e0312ecbda92557c93870114af6c9d05c4f7f0c3685b7a46bee255932575cce10b424d813cfe4875d3e82047b97ddef52741d546b8e289dc6935b3ece0462db0a22b8e7'
# # p4 = '0CoJUm6Qyw8W8jud'
# #
# #
# #
# # #
# # # function a(a) {
# # #         var d, e, \
# # #             b = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789",
# # #             c = "";
# # #         for (d = 0; a > d; d += 1) e = Math.random() * b.length, e = Math.floor(e), c += b.charAt(e);
# # #         return c
# # #     }
# # #
# # def a(a):
# #     b = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
# #     c = ''
# #     d = 0
# #     while a > d:
# #         d += 1
# #         e = random.random() * len(b)
# #         e = math.floor(e)
# #         c += b[e]
# #     return c
# #
# #
# # #
# # #
# # # function b(a, b) {
# # #     var c = CryptoJS.enc.Utf8.parse(b),
# # #         d = CryptoJS.enc.Utf8.parse("0102030405060708"),
# # #         e = CryptoJS.enc.Utf8.parse(a),
# # #         f = CryptoJS.AES.encrypt(e, c, { iv: d, mode: CryptoJS.mode.CBC });
# # #     console.group('==========b start==========')
# # #     	console.log('c', c)
# # #     	console.log('d', d)
# # #     	console.log('e', e)
# # #     	console.log('f', f.toString())
# # #     console.groupEnd()
# # #     return f.toString()
# # # }
# #
# # def b(a,b):
# #     pass
#
# # function c(a, b, c) { var d, e; return setMaxDigits(131), d = new RSAKeyPair(b, "", c), e = encryptedString(d, a) }
# #
# # function d(d, e, f, g) {
# # 	console.group('======d start======')
# # 	console.log('d', d)
# # 	console.log('e', e)
# # 	console.log('f', f)
# # 	console.log('g', g)
#     # console.log('====d end========')
# #     var h = {},
#     # i = a(16);
#     # h.encText = b(d, g),
#     # h.encText = b(h.encText, i),
#     # h.encSecKey = c(i, e, f)
#     # console.log('result:', h)
#     # console.groupEnd()
# #     return h
# #
# # }
# #
# # function e(a, b, d, e) {
#  # 	console.group('======e start======')
# # 	console.log('a', a)
# # 	console.log('b', b)
# # 	console.log('d', d)
# # 	console.log('e', e)
#     # console.log('=====e end=======')
# #     var f = {};
# #     f.encText = c(a + e, b, d)
# #     console.log('result:', f)
# #     console.groupEnd()
# #     return f
# # }
