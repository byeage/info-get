import requests
from bson import json_util
import json
import math
import time



# tab_name: "综合",
# tab_id: 1,
# tab_name: "视频",
# tab_id: 2,
# tab_name: "图集",
# tab_id: 3,
# tab_name: "用户",
# tab_id: 4,
# tab_name: "问答",
# tab_id: 5


offset = 0
count = 20
errorsOffset = []

def getToutiaoSearch(keyword, offset, tab_id):
    url = 'https://www.toutiao.com/search_content'
    params = {
        "offset": offset,
        "format": "json",
        "keyword": keyword,
        "autoload": "true",
        "count": count,
        "cur_tab": tab_id,
        "from": "search_tab",
    }
    print('offset', params['offset'])
    try:
        res = requests.get(url, params= params)
        content = res.content
        resJson = json.loads(content)
        data = processJSON(resJson)
        print(data)
        if data['hasNext']:
            offset = offset + count
            time.sleep(3)
            getToutiaoSearch(keyword, offset, tab_id)
        else:
            print('scrapy end')
    except BaseException as err:
        print(err)
        errorsOffset.append(offset)

def getToutiaoSearchErrorOffset(keyword, offset, tab_id):
    url = 'https://www.toutiao.com/search_content'
    params = {
        "offset": offset,
        "format": "json",
        "keyword": keyword,
        "autoload": "true",
        "count": count,
        "cur_tab": tab_id,
        "from": "search_tab",
    }
    print('offset', params['offset'])
    res = requests.get(url, params=params)
    content = res.content
    resJson = json.loads(content)
    data = processJSON(resJson)
    print(data)

def processJSON(res):
    list = res['data']
    hasNext = True
    if len(list) == 0:
        hasNext = False
        return {
            'list': list,
            'hasNext': hasNext
        }
    else:
        return {
            'list': list,
            'hasNext': hasNext
        }



if __name__ == '__main__':
    keyword = '马化腾'
    offset = 0
    tab_id = 1
    getToutiaoSearch(keyword, offset, tab_id)
    for deviate in errorsOffset:
        getToutiaoSearchErrorOffset(keyword, deviate, tab_id)