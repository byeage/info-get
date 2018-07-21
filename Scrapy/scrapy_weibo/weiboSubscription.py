# 获取用户关注人物信息
import requests
from bson import json_util
import json
import math
import time
from db import mdb
# dbInstance = mdb.dbInstance()
sinceErrorId = []
since_id = ''
cookies =  {"_T_WM":"fdbf8bc44c795c5cda57655e31c304de","ALF":"1526014941","SCF":"ApRKvktpAcri8KRFdlfeaR8dMo-GQd5NxTEoaTuNtdjmAq-3_higwpSMdrV72mrVn3LFqgAfSSwbcYrXvRQwm1Q.","SUB":"_2A253ydKODeRhGeRO4lQQ8yjMzTiIHXVVNf7GrDV6PUJbktAKLUugkW1NUErsJnvjJSKp6jEcynkOR6rIDOZFDDjS","SUBP":"0033WrSXqPxfM725Ws9jqgMF55529P9D9WFB2S6d3gIMp73iO8nSlZep5JpX5K-hUgL.Foz71Kqpe0q7SoB2dJLoI7pFdGHLKg8.qgY_C-.t","SUHB":"0y0YEigCc5VM7u","H5_INDEX":"3","H5_INDEX_TITLE":"BlueMadao-II","WEIBOCN_FROM":"1110006030","M_WEIBOCN_PARAMS":"luicode%3D10000012%26lfid%3D1005052096136064_-_FANS%26fid%3D1076031918106382%26uicode%3D10000011"}
def weiboSubcriptionScrapy(id, sid):
    """ 抓取微博评论
    :param id: 微博ID
    :param page: 评论翻页页数
    :return:
    """
    url = 'https://m.weibo.cn/api/container/getIndex'
    params= {
        'containerid': id
    }
    if sid != '':
        params = {
            'containerid': id,
            'since_id': sid
        }
    try:
        print(params)
        res = requests.get(url, params=params, cookies=cookies)
        content = res.content
        fileHandle = 'followers.json'
        resJson = json.loads(content)
        print(url)
        print(resJson)
        data = processJSON(resJson, sid)
        with open(fileHandle, 'wt', encoding='utf-8') as f:
            json.dump(resJson, f, indent=4, ensure_ascii=False, default=json_util.default)
        since_id = data['sid']
        hasNext = data['hasNext']
        if hasNext:
            time.sleep(3)
            weiboSubcriptionScrapy(id, since_id)
        else:
            print('completed')
    except BaseException as err:
        print('error page process' + str(err))





def processJSON(res, id):
    print(res)
    followersList = []
    if res['ok'] == 1:
        followersList = res['data']['cards']
        hasNext = True
        sid = res['data']['cardlistInfo']['since_id']
        return {
            'list': followersList,
            'hasNext': hasNext,
            'sid': sid
        }
    else:
        return {
            'list': [],
            'hasNext': False,
            'sid': ''
        }



if __name__ == '__main__':
    id = '231051_-_followersrecomm_-_1662766362'
    weiboSubcriptionScrapy(id, since_id)
    print('sinceErrorId', sinceErrorId)
