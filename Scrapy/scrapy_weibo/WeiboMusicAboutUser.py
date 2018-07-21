
import requests
from bson import json_util
import json
import math
import time
from db import mdb
dbInstance = mdb.dbInstance()


# {
# ok: 0,
# msg: "这里还没有内容",
# data: - {
# cards:[]
# }
# }
def parseCookies(str):
    strs = str.split(';')
    obj = {}
    keyList= [str.split('=') for str in strs]
    for [key, val] in keyList:
        obj[key.strip()] = val.strip()
    print(obj)
    return obj

cookies = 'ALF=1529038963; SCF=ApRKvktpAcri8KRFdlfeaR8dMo-GQd5NxTEoaTuNtdjmTUAkkMkYogqDYmCdVCQ3NdK8nrm2z9VqU56yocBCcDc.; SUB=_2A253_8-DDeRhGeRO4lQQ8yjMzTiIHXVVA9HLrDV6PUJbktAKLUP_kW1NUErsJkUsJu3fdbAmJjY0cwFrev9ZXHoF; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WFB2S6d3gIMp73iO8nSlZep5JpX5K-hUgL.Foz71Kqpe0q7SoB2dJLoI7LFdGHLKg8.qgYt; SUHB=0P1NNoRf-VnZzm; SSOLoginState=1526448083; _T_WM=7be6d5c0c635271532f1d43f2a368796; WEIBOCN_FROM=1110006030; MLOGIN=1; M_WEIBOCN_PARAMS=luicode%3D10000011%26lfid%3D231051_-_followers_-_1358023322%26fid%3D231051_-_followerstagrecomm_-_1358023322_-_1042015%253AtagCategory_046%26uicode%3D10000011'
cookies = parseCookies(cookies)
headers= {
    'Host': 'm.weibo.cn',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3410.2 Safari/537.36',
    'referer':'https://m.weibo.cn/p/index?containerid=231051_-_followerstagrecomm_-_1358023322_-_1042015%253AtagCategory_046&luicode=10000011&lfid=231051_-_followers_-_1358023322',
    'X-Requested-With': 'XMLHttpRequest'
}

def getMusicFollow(uid, page, userPos):
    url = 'https://m.weibo.cn/api/container/getIndex'
    params = {
        'containerid': '231051_-_followerstagrecomm_-_'+str(uid)+'_-_1042015%3AtagCategory_046',
        'luicode': '10000011',
        'lfid': '231051_-_followers_-_'+str(uid),
        'since_id': page
    }

    res = requests.get(url, headers=headers, params=params, cookies=cookies)
    data = process(res.content)
    print(data)
    userList = data['list']
    if len(userList):
        dbInstance.add_weibo_music(userList)
    if data['next']:
        print('继续下一页内容')
        p = page + 1
        time.sleep(3)
        getMusicFollow(uid, p, userPos)
    else:
        print('这个人已经爬取完了,换一个新人')
        pos = userPos
        result = dbInstance.query_weibo_music_user(pos)
        print(result.count())
        if result.count() >= pos:
            user = result[0]
            userid = user['user']['id']
            time.sleep(3)
            getMusicFollow(userid, 0, pos + 1)
        else:
            print('爬完了')



def is_typeUser(n):
    return n['card_type'] == 10


def process(content):
    data = json.loads(content)
    if 'msg' in data and data['msg'] == '这里还没有内容':
        return {
            'list': [],
            'next': 0
        }
    else:
        listUser = data['data']['cards'][0]['card_group']
        listUser = list(filter(is_typeUser, listUser))
        print(listUser)
        hasNext = len(listUser)
        return {
            'list': listUser,
            'next': hasNext
        }





#
if __name__ == '__main__':
    # dbInstance.create_weibo_misic_DB()
    getMusicFollow(1358023322, 0, 0)
