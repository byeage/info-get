# 微博搜索
# -*- coding: utf-8 -*-
import requests
from bson import json_util
import json
import math
import time

from db import mdb
dbInstance = mdb.dbInstance()
pageHistory = []
errorPages = []
def weiboSearch(keyword, type, page):
    url = 'https://m.weibo.cn/api/container/getIndex'
    params = {
        'containerid': '100103type='+str(type)+'&q='+keyword,
        'page': page
    }

    try:
        res = requests.get(url, params=params)
        pageHistory.append(page)
        print('pageHistory', pageHistory)
        print('errorPages', errorPages)
        page = page + 1
        content = res.content
        resJson = json.loads(content)
        fileHandle = str(page) + '.json'
        data = processJSON(resJson)
        hasNext = data['hasNext']
        dbInstance.add_weibo(data['list'])
        with open(fileHandle, 'wt', encoding='utf-8') as f:
            json.dump(data['list'], f, indent=4, ensure_ascii=False, default=json_util.default)
        if hasNext:
            time.sleep(6)
            if len(errorPages) < 10:
                weiboSearch(keyword, type, page)
        else:
            errorPages.append(page)

    except BaseException:
        print('error page' + str(page))
        errorPages.append(page)


def weiboSearchProcessErrorPages(keyword, type, page):
    print('pageHistory', pageHistory)
    print('errorPages', errorPages)
    url = 'https://m.weibo.cn/api/container/getIndex'
    params = {
        'containerid': '100103type='+str(type)+'&q='+keyword,
        'page': page
    }
    try:
        res = requests.get(url, params=params)
        pageHistory.append(page)
        page = page + 1
        content = res.content
        resJson = json.loads(content)
        fileHandle = str(page) + '.json'
        data = processJSON(resJson)
        hasNext = data['hasNext']
        dbInstance.add_weibo(data['list'])
        with open(fileHandle, 'wt', encoding='utf-8') as f:
            json.dump(data['list'], f, indent=4, ensure_ascii=False, default=json_util.default)
        if hasNext:
            print('retrive back')
        else:
            print('error page process' + str(page))
    except BaseException:
        print('error page process' + str(page))




def processJSON(res):
    cardGroups = res['data']['cards']
    cardGroupList = []
    for group in cardGroups:
        cardGroupList.extend(group['card_group'])
    cardGroupList = filter(lambda x: x['card_type'] == 9, cardGroupList)
    cardGroupList = list(cardGroupList)
    hasNext = bool(len(res['data']['cards']))
    return {
        'list': cardGroupList,
        'hasNext': hasNext
    }


if __name__ == '__main__':
    keyword = '徐克'
    type = 1
    page = 1
    weiboSearch(keyword, type, 1)
    for p in errorPages:
        weiboSearchProcessErrorPages(keyword, type, p)


