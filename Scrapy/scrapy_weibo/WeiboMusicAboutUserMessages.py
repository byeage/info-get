import requests
from bson import json_util
import json
import math
import time
from db import mdb
dbInstance = mdb.dbInstance()
result = dbInstance.query_weibo_all_user()
users = iter(result)

# usersGenerate =

# while True:
#     try:
#         item = users.next()
#     except StopIteration:
#         break




class WeiboList(object):
    def __init__(self, user):
        self.page = 1
        self.user = user
        self.errorPages = []
        self.pageHistory = []
        self.url = 'https://m.weibo.cn/api/container/getIndex'
    def getParams(self):
            return {
            # 'type': 'all',
            # 'uid': self.user['id'],
            'containerid': '107603' + str(self.user['id']),
            'page': self.page
        }

    def setPage(self):
        self.page += 1


    def getData(self):
        # 请求数据
        params = self.getParams()
        url = self.url
        try:
            res = requests.get(url, params=params)
            content = res.content
            resJson = json.loads(content)
            data = self.processJSON(resJson)
            # data = self.processJSONToday(resJson)
            hasNext = data['hasNext']
            if len(data['list']):
                # dbInstance.add_weibo_music_info(data['list'])
                dbInstance.add_weibo_music_infoAll(data['list'])
            if hasNext:
                time.sleep(6)
                if len(self.errorPages) < 10:
                    self.setPage()
                    time.sleep(6)
                    self.getData()
            else:
                print('no more 有请下一位')
                # 下一位
                time.sleep(3)
                getWeiboUserMusicStart()
                # print('error page process' + str(self.page))
                # if self.page not in self.errorPages:
                #     self.errorPages.append(self.page)

        except BaseException:
            print('error page process' + str(self.page))
            self.errorPages.append(self.page)

    def processJSON(self, res):
        # 处理请求返回的结果
        if res['ok'] == 1:
            weiboList = res['data']['cards']
            weiboList = filter(lambda x: x['card_type'] == 9, weiboList)
            weiboList = list(weiboList)
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
    def processJSONToday(self, res):
        # 处理请求返回的结果 今天为止
        if res['ok'] == 1:
            weiboList = res['data']['cards']
            weiboList = filter(lambda x: x['card_type'] == 9, weiboList)
            weiboList = list(weiboList)
            for item in weiboList:
                print(item['mblog']['text'])
            hasNext = all(self.checkDate(item['mblog']['created_at']) for item in weiboList)
            weiboList = filter(lambda x: self.checkDate(x['mblog']['created_at']), weiboList)
            weiboList = list(weiboList)
            print(hasNext)
            print(weiboList)
            return {
                'list': weiboList,
                'hasNext': hasNext
            }
        else:
            return {
                'list': [],
                'hasNext': False
            }

    def checkDate(self, time):
        if str(time).find('前') != -1:
            return True
        else:
            return False


def getWeiboUserMusicStart():
    try:
        user = users.next()
        user = user['user']
        print(user)
        weibo = WeiboList(user)
        weibo.getData()
    except StopIteration:
        print('爬取END')


getWeiboUserMusicStart()