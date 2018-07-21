# 获取某一条微博的评论
import requests
from bson import json_util
import json
import math
import time
from db import mdb
dbInstance = mdb.dbInstance()
pageHistory = []
errorPages = []
def weiboCommentScrapy(id, page):
    """ 抓取微博评论
    :param id: 微博ID
    :param page: 评论翻页页数
    :return:
    """
    url = 'https://m.weibo.cn/api/comments/show'
    params= {
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
        fileHandle = str(page) + '-comment.json'
        resJson = json.loads(content)
        data = processJSON(resJson)
        with open(fileHandle, 'wt', encoding='utf-8') as f:
            json.dump(resJson, f, indent=4, ensure_ascii=False, default=json_util.default)
        hasNext = data['hasNext']
        print(data['list'])
        dbInstance.add_weiboComment(data['list'])
        if hasNext:
            time.sleep(6)
            if len(errorPages) < 10:
                weiboCommentScrapy(id, nextPage)
        else:
            print('error page process' + str(page))
    except BaseException:
        print('error page process' + str(page))




def weiboCommentProcessErrorPages(id, page):
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
        fileHandle = str(page) + '-comment.json'
        resJson = json.loads(content)
        data = processJSON(resJson)
        with open(fileHandle, 'wt', encoding='utf-8') as f:
            json.dump(resJson, f, indent=4, ensure_ascii=False, default=json_util.default)
        hasNext = data['hasNext']
        print(data['list'])
        dbInstance.add_weiboComment(data['list'])
        if hasNext:
            print('retrive back')
        else:
            print('error page process' + str(page))
    except BaseException:
        print('error page process' + str(page))



def processJSON(res):
    if res['ok'] == 1:
        commentList = res['data']['data']
        hasNext = True
        return {
            'list': commentList,
            'hasNext': hasNext
        }
    else:
        return {
            'list': [],
            'hasNext': False
        }



if __name__ == '__main__':
    id = 4229227957987705
    page = 1
    weiboCommentScrapy(id, page)
    for p in errorPages:
        weiboCommentProcessErrorPages(id, p)
