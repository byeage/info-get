from scrapy_wangyi_music import getParams
from db import mdb
import time
dbInstance = mdb.dbInstance()




def getComments(id, offset):
    res = getParams.getSongComments(id, offset)
    obj = process(res)
    dbInstance.add_wangyi_comment(obj['list'])
    offset += 20
    if obj['more']:
        time.sleep(3)
        getComments(id, offset)

def process(res):
    list = res['result']['comments']
    more = res['result']['more']
    return {
        'more': more,
        'list': list
    }



searchSongList = getParams.getSearchParams('Chasing Pavements', 0, '单曲')
print(searchSongList)
firstSong = searchSongList['result']['result']['songs'][0]
print(firstSong)
offset = 0
getComments(firstSong['id'], offset)
