# 获取某一个用户的全部微博
# https://m.weibo.cn/api/container/getIndex?uid=1662766362&luicode=10000011&lfid=100103type%3D1%26q%3D%E5%88%98%E6%98%A5&type=all&containerid=1076031662766362&page=3
import requests
from bson import json_util
import json
import math
import time
from db import mdb
dbInstance = mdb.dbInstance()
pageHistory = []
errorPages = []
def weiboListScrapy(uid, containerid,  page):
    """ 抓取微博评论
    :param id: 微博ID
    :param page: 评论翻页页数
    :return:
    """
    url = 'https://m.weibo.cn/api/container/getIndex'
    params= {
        'type': 'all',
        'uid': uid,
        'containerid':containerid,
        'page': page
    }
    try:
        res = requests.get(url, params=params)
        pageHistory.append(page)
        print('pageHistory', pageHistory)
        print('errorPages', errorPages)
        nextPage = page + 1
        content = res.content
        fileHandle = str(page) + '-weiboList.json'
        resJson = json.loads(content)
        data = processJSON(resJson)
        with open(fileHandle, 'wt', encoding='utf-8') as f:
            json.dump(resJson, f, indent=4, ensure_ascii=False, default=json_util.default)
        hasNext = data['hasNext']
        print(data['list'])
        # dbInstance.add_weiboComment(data['list'])
        if hasNext:
            time.sleep(6)
            if len(errorPages) < 10:
                weiboListScrapy(id, nextPage)
        else:
            print('error page process' + str(page))
    except BaseException:
        print('error page process' + str(page))




def weiboListProcessErrorPages(id, page):
    """ 抓取微博评论
        :param id: 微博ID
        :param page: 评论翻页页数
        :return:
        """
    url = 'https://m.weibo.cn/api/comments/show'
    params = {
        'id': id,
        'page': page
    }
    try:
        res = requests.get(url, params=params)
        pageHistory.append(page)
        print('pageHistory', pageHistory)
        print('errorPages', errorPages)
        nextPage = page + 1
        content = res.content
        fileHandle = str(page) + '-weiboList.json'
        resJson = json.loads(content)
        data = processJSON(resJson)
        with open(fileHandle, 'wt', encoding='utf-8') as f:
            json.dump(resJson, f, indent=4, ensure_ascii=False, default=json_util.default)
        hasNext = data['hasNext']
        print(data['list'])
        # dbInstance.add_weiboComment(data['list'])
        if hasNext:
            print('retrive back')
        else:
            print('error page process' + str(page))
    except BaseException:
        print('error page process' + str(page))



def processJSON(res):
    if res['ok'] == 1:
        weiboList = res['data']['cards']
        hasNext = True
        return {
            'list': weiboList,
            'hasNext': hasNext
        }
    else:
        return {
            'list': [],
            'hasNext': False
        }



if __name__ == '__main__':
    uid = '1662766362'
    containerid = '1076031662766362'
    page = 1
    weiboListScrapy(uid, containerid, page)
    for p in errorPages:
        weiboListProcessErrorPages(uid, containerid, p)
