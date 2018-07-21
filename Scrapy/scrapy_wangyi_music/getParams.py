# -*- coding: utf-8 -*-
from Crypto.Cipher import AES
import base64
import requests
import json
from bson import json_util
import math
import random
from  Crypto.Util import Padding
from bs4 import BeautifulSoup
import re
import demjson
session = requests.Session()
cookies = {"_ntes_nnid":"4fcbee495bb8db3955e8bc502ca06cd8,1523241152144",
           "_ntes_nuid":"4fcbee495bb8db3955e8bc502ca06cd8",
           "_ga":"GA1.2.1172943924.1523241152",
           "__remember_me":"true",
           "_iuqxldmzr_":"32",
           "__utmz":"94650624.1524903675.5.4.utmcsr",
           "WM_TID":"CRmWjxzlaA7xGPoLcGZHfrL7q%2BRT%2BOkf",
           "JSESSIONID-WYYY":"VksYCGKGx8enzgJGGaCY%2B6MkDfWmG%2B40dFHy1%2FKa%2FdVf2AV4Pc0eODnNG1uJwSwOdGJPXuBGS86AEc%2FIkcm9U4RA0%5CP%2FTaThccP%5CV5U1Qqh%2FOXuRQT9acX1r6x8kxq3VCnJO752mpPD%5CB5WEvDoMgg3U5eeqq8Dk%2B5RzqewbEdGAZReB%3A1525412914964",
           "__utma":"94650624.1172943924.1523241152.1525401846.1525411115.16",
           "__utmc":"94650624",
           "MUSIC_U":"27a2c72cf84108f27cffb8fda658b19567a973ccbf3eb9bd6eb8ea763a7e4dbb100942e10e6b517bed6b48ff86694589a70b41177f9edcea",
           "__csrf":"0ebfad7806ac1d0f802d3b9f22660064",
           "__utmb":"94650624.11.10.1525411115"
           }


def getRandomKey(num):
    b = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
    c= ''
    for d in range(0, num, 1):
        e = math.floor(random.random() * len(b))
        c += b[e]
    common = '9KGbCUsYK9j1gWei'
    return common


def getEncryptText(message, key):
    messageEncode = bytes(message, encoding='utf-8')
    keyEncode = bytes(key, encoding="utf8")
    iv = '0102030405060708'
    ivEncode = bytes(iv, encoding="utf8")
    encryptor = AES.new(keyEncode, AES.MODE_CBC, ivEncode)
    text = encryptor.encrypt(Padding.pad(messageEncode, 16))
    return base64.b64encode(text).decode("utf-8")


# 如果 getRandomKey 值相同，则encryKey 的值也是相同的


def getEncryptKey():
    key = 'a69812c37ae62f6af952127fef38f9def7deeb68f93c8a228bd33566b8ab9d83ada2a9cbf8f48c0db6c4ea9aafe6646c1b2197a9dccaa61ec2bbfa24ca72c8f4e0adc1a79d74405eb384ddf2827938b4197492463b176d1ea8af44d882e77e568a6cfabcc508174fbe47e6c2abbc947cdbf4cd0fe38f3cdde40df2eddf7508c8'
    return key







def getSearchParams(keyword, offset, type):
    '''

    :param keyword: 关键词
    :param offset: 偏移
    :param type: 类型
        1 单曲
        100 歌手
        10 专辑
        1014 视频
        1006 歌词
        1000 歌单
        1009 主播电台
        9627  用户
    :return:
    '''
    types= {
        '单曲': 1,
        '歌手': 100,
        '专辑': 10,
        '视频': 1014,
        '歌词': 1006,
        '歌单': 1000,
        '主播电台': 1009,
        '用户': 1002
    }
    randomKey = getRandomKey(16)
    key = '0CoJUm6Qyw8W8jud'
    message = {
        "hlpretag": "<span class=\"s-fc7\">",
        "hlposttag": "</span>",
        "s": keyword,
        "type": types[type],
        "offset": offset,
        "total": "true",
        "limit": "90",
        "csrf_token": "a4e9abe6368c3cc17ad8c3e0183f3310"
    }
    message = json.dumps(message, ensure_ascii=False, separators=(',', ':'))
    tmp = getEncryptText(message, key)
    encText = getEncryptText(tmp, randomKey)
    encSecKey = getEncryptKey()
    data = {
        'params': encText,
        'encSecKey': encSecKey
    }
    url = 'http://music.163.com/weapi/cloudsearch/get/web?csrf_token=7b5b7d4c2124cea3d5ae211552ee4b61'
    res = requests.post(url, data=data)
    return {
        'type': type,
        'result': json.loads(res.content.decode('utf-8'))
    }





def getMySongList(uid, offset):
    '''
    获取我的歌单
    :param uid:  用户UID
    :param offset:  偏移
    :return:
    '''
    randomKey = getRandomKey(16)
    key = '0CoJUm6Qyw8W8jud'
    message = {
        "uid": uid,
        "wordwrap": "7",
        "offset": offset,
        "total": "true",
        "limit": "36",
        "csrf_token": "0ebfad7806ac1d0f802d3b9f22660064"
    }
    message = json.dumps(message, ensure_ascii=False, separators=(',', ':'))
    tmp = getEncryptText(message, key)
    encText = getEncryptText(tmp, randomKey)
    encSecKey = getEncryptKey()
    data = {
        'params': encText,
        'encSecKey': encSecKey
    }
    print(data)
    headers = {
        'Host': 'music.163.com',
        'Origin': 'http://music.163.com',
        'Referer': 'http://music.163.com/user/home?id=56484378',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'
    }
    url = 'http://music.163.com/weapi/user/playlist?csrf_token=0ebfad7806ac1d0f802d3b9f22660064'
    res = requests.post(url, data=data, headers=headers, cookies=cookies)

    return {
        'type': '歌单',
        'result': res.content.decode('utf-8')
    }


def getRecentSongRank(uid, offset):
    '''
    获取最近播放歌曲
    :param uid:  用户UID
    :param offset:  偏移
    :return:
    '''
    randomKey = getRandomKey(16)
    key = '0CoJUm6Qyw8W8jud'
    message = {
         "uid": uid,
         "type": "-1",
         "limit": "1000",
         "offset":offset,
         "total": "true",
         "csrf_token": "0ebfad7806ac1d0f802d3b9f22660064"
         }

    message = json.dumps(message, ensure_ascii=False, separators=(',', ':'))
    tmp = getEncryptText(message, key)
    encText = getEncryptText(tmp, randomKey)
    encSecKey = getEncryptKey()
    data = {
        'params': encText,
        'encSecKey': encSecKey
    }
    print(data)
    headers = {
        'Host': 'music.163.com',
        'Origin': 'http://music.163.com',
        'Referer': 'http://music.163.com/user/home?id=56484378',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'
    }
    url = 'http://music.163.com/weapi/v1/play/record?csrf_token=0ebfad7806ac1d0f802d3b9f22660064'
    res = requests.post(url, data=data, headers=headers, cookies=cookies)

    return {
        'type': '听歌排行',
        'result': res.content.decode('utf-8')
    }



def getSongLyric(id):
    '''
    获取歌词
    :param id:
    :return:
    '''
    randomKey = getRandomKey(16)
    key = '0CoJUm6Qyw8W8jud'
    message = {
            "id": id,
            "lv": -1,
            "tv": -1,
            "csrf_token": "5220fc5dd205b7c92c315ac85581877a"
            }

    message = json.dumps(message, ensure_ascii=False, separators=(',', ':'))
    tmp = getEncryptText(message, key)
    encText = getEncryptText(tmp, randomKey)
    encSecKey = getEncryptKey()
    data = {
        'params': encText,
        'encSecKey': encSecKey
    }
    print(data)
    headers = {
        'Host': 'music.163.com',
        'Origin': 'http://music.163.com',
        'Referer': 'http://music.163.com/user/home?id=56484378',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'
    }
    url = 'http://music.163.com/weapi/song/lyric?csrf_token=7a87e54c1df1ec0855b851d371db0781'
    res = requests.post(url, data=data, headers=headers, cookies=cookies)

    return {
        'type': '歌曲歌词',
        'result': res.content.decode('utf-8')
    }


def getSongComments(id, offset):
    '''
    获取歌曲评论
    :param id:  歌曲ID
    :param offset: 偏移量
    :return:
    '''
    randomKey = getRandomKey(16)
    key = '0CoJUm6Qyw8W8jud'
    message = {
            "rid":"R_SO_4_" + str(id),
            "offset": offset,
            "total":"false",
            "limit":"20",
            "csrf_token":"7a87e54c1df1ec0855b851d371db0781"
            }

    message = json.dumps(message, ensure_ascii=False, separators=(',', ':'))
    tmp = getEncryptText(message, key)
    encText = getEncryptText(tmp, randomKey)
    encSecKey = getEncryptKey()
    data = {
        'params': encText,
        'encSecKey': encSecKey
    }
    headers = {
        'Host': 'music.163.com',
        'Origin': 'http://music.163.com',
        'Referer': 'http://music.163.com/user/home?id=56484378',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'
    }
    url = 'http://music.163.com/weapi/v1/resource/comments/R_SO_4_'+str(id)+'?csrf_token=7a87e54c1df1ec0855b851d371db0781'
    res = requests.post(url, data=data, headers=headers, cookies=cookies)

    return {
        'type': '歌曲评论',
        'result': json.loads(res.content.decode('utf-8'))
    }





def getUserInformation ():
    '''
    获取用户相关信息
    :return:
    '''
    url = 'http://music.163.com'
    headers = {
        'Host': 'music.163.com',
        'Origin': 'http://music.163.com',
        'Referer': 'http://music.163.com',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'
    }
    res = requests.get(url, headers=headers, cookies=cookies)
    soup = BeautifulSoup(res.content, 'html.parser')
    script = soup.find('script')
    scriptText = script.get_text()
    searchText = re.search(r'GUser=({.*});', scriptText)
    userInfo = searchText.group(1)
    userInfo = demjson.decode(userInfo)
    print(userInfo)





if __name__ == '__main__':
    pass
    # resContent = getSearchParams('王菲', 0, '歌手')
    # resContent = getSearchParams('王菲', 0, '歌单')
    # resContent = getSearchParams('王菲', 0, '歌词')
    # resContent = getSearchParams('王菲', 0, '用户')
    # resContent = getMySongList('56484378', 0)
    # print(resContent)
    # resContent= getRecentSongRank('56484378', 0)
    # print(resContent)

    # resContent= getSongLyric('5201782')
    # print(resContent)

    # resContent= getSongComments('5201782', 0)
    # print(resContent)
    # getUserInformation()
