import requests
import json
from db import mdb
import time
dbInstance = mdb.dbInstance()
# cookies = {"q_c1":"bad4c8b01e4c4977b1a9fab360c89260|1525686821000|1504749306000","_zap":"ea173538-687f-42ff-b91d-63c913002aff","aliyungf_tc":"AQAAADHaTCn2cgEA6tbnc6pjKCjoJOvN","_xsrf":"8c076352-3489-421c-9170-58ed910b100c","d_c0":"\"AICuQ9Jnjg2PTj-xtGEfQFZXAqFDQl8Qg7w","tgw_l7_route":"156dfd931a77f9586c0da07030f2df36","capsion_ticket":"\"2|1:0|10:1525686817|14:capsion_ticket|44:OWQ4ZDA2NzU5ODE3NDQyOWJhZGZiNWE2MGIyNjUzMzI","l_n_c":"1","r_cap_id":"\"ZTRiNjY1ZmQ3Zjc3NDMyMjllODU2MGNiMDM2OGIwN2Y","cap_id":"\"Y2JhOTlkOTI4ZDA4NGM4ZmI3YjgzMThiZGJhNzU4ZDg","l_cap_id":"\"ZTBkMDBmMWM0YmU1NGU5NjgyM2Y2OWNhMTc1YTk1MDA","n_c":"1","__utma":"51854390.293167018.1525686826.1525686826.1525686826.1","__utmb":"51854390.0.10.1525686826","__utmc":"51854390","__utmz":"51854390.1525686826.1.1.utmcsr","__utmv":"51854390.000--|3"}
cookies= {}
startPos = 0




def getFollowing(cursor, uid, startPos):
    try:
        back = requests.get('http://localhost:3000/toutiao/signature/' + str(uid))
    except BaseException :
        print(BaseException)
    _signature = str(back.content)
    print(_signature)
    url = 'https://www.toutiao.com/c/user/following/'
    params = {
        'user_id': uid,
        'cursor': cursor,
        'count': 200,
        '_signature': 'DE3FQQAAVrrzsjq-SjKthQxNxV'
    }

    headers = {
        'authority': 'www.toutiao.com',
        'path': '/c/user/following/?user_id=' + str(uid) + '&cursor=0&count=20&_signature=DE3FQQAAVrrzsjq-SjKthQxNxV',
        'if-none-match': 'b658298d0ebb1b6c23c37ea7c7db20a5b518992f',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3410.2 Safari/537.36',
        'referer': 'https://www.toutiao.com/c/user/relation/' + str(uid) + '/?tab=followed',
        'x-udid': 'AICuQ9Jnjg2PTj-xtGEfQFZXAqFDQl8Qg7w='
    }

    res = requests.get(url, params=params, headers=headers)
    backData = json.loads(res.content)
    message = backData['message']
    if message == 'exception':
        # try again
        print('出错了 再试一次')
        time.sleep(5)
        print(cursor, uid, startPos)
        try:
            getFollowing(cursor, uid, startPos)
        except BaseException:
            print(BaseException)
    else:
        print(backData)
        list = backData['data']
        if len(list):
            dbInstance.add_toutiaousers(list)
        pos = backData['cursor']
        hasMore = backData['has_more']

        if hasMore:
            time.sleep(5)
            print('subIndex', startPos)
            try:
                getFollowing(pos, uid, startPos)
            except BaseException:
                print(BaseException)
            print('还没有取完继续')
            print('subIndex',startPos)
        else:
            print('这个人的用户的following列表已经爬完')
#             继续下个人
            subIndex = startPos + 1
            result = dbInstance.query_toutiao_user(subIndex)
            print(result.count())
            if result.count() >= subIndex:
                user = result[0]
                uid = user['user_id']
                cursor = 0
                time.sleep(5)
                print('subIndex', subIndex)
                print(user)
                getFollowing(cursor, uid, subIndex)




if __name__ == '__main__':
    uid = 3249088303
    cursor = 0
    startPos = 0
    getFollowing(cursor, uid, startPos)

