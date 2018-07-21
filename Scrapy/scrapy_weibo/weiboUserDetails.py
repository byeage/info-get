# 获取用户信息及详情
import requests
from bson import json_util
import json
import math
import time

def getUsereDetails(uid):
    url = 'https://m.weibo.cn/api/container/getIndex'
    containerid = '230283' + uid
    params = {
        'containerid': containerid,
        'lfid': containerid,
        'type': 'all'
    }
    try:
        res = requests.get(url, params=params)
        content = res.content
        resJson = json.loads(content)
        userDetails = processJSONDetails(resJson)
        print(resJson)
        return userDetails

    except BaseException as err:
        print(str(err))
        print('get user details information error')



def getCommonInformation(uid):
    url = 'https://m.weibo.cn/api/container/getIndex'
    params = {
            'containerid':     '100505'+ uid
        }
    print(params)
    try:
        res = requests.get(url, params=params)
        content = res.content
        resJson = json.loads(content)
        userInfo = processJSONCommon(resJson)
        # print(resJson)
        return userInfo
    except BaseException as err:
        print(err)
        print('get user details information error')


def processJSONDetails(res):
    if res['ok'] == 1:
        return res['data']['cards']
    else:
        return []



def processJSONCommon(res):
    if res['ok'] == 1:
        return res['data']['userInfo']
    else:
        return {}




def getUserInfo(containerid):
    userInfo = getCommonInformation(containerid)
    userDetails = getUsereDetails(containerid)
    userInfo['userDetails'] = userDetails
    print(userInfo)



if __name__ == '__main__':


    uid = '1560906700'
    getUserInfo(uid)
