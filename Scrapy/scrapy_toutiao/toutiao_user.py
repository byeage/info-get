import requests
import json
from bs4 import BeautifulSoup
import re
import demjson

# cookies = {"q_c1":"bad4c8b01e4c4977b1a9fab360c89260|1525686821000|1504749306000","_zap":"ea173538-687f-42ff-b91d-63c913002aff","aliyungf_tc":"AQAAADHaTCn2cgEA6tbnc6pjKCjoJOvN","_xsrf":"8c076352-3489-421c-9170-58ed910b100c","d_c0":"\"AICuQ9Jnjg2PTj-xtGEfQFZXAqFDQl8Qg7w","tgw_l7_route":"156dfd931a77f9586c0da07030f2df36","capsion_ticket":"\"2|1:0|10:1525686817|14:capsion_ticket|44:OWQ4ZDA2NzU5ODE3NDQyOWJhZGZiNWE2MGIyNjUzMzI","l_n_c":"1","r_cap_id":"\"ZTRiNjY1ZmQ3Zjc3NDMyMjllODU2MGNiMDM2OGIwN2Y","cap_id":"\"Y2JhOTlkOTI4ZDA4NGM4ZmI3YjgzMThiZGJhNzU4ZDg","l_cap_id":"\"ZTBkMDBmMWM0YmU1NGU5NjgyM2Y2OWNhMTc1YTk1MDA","n_c":"1","__utma":"51854390.293167018.1525686826.1525686826.1525686826.1","__utmb":"51854390.0.10.1525686826","__utmc":"51854390","__utmz":"51854390.1525686826.1.1.utmcsr","__utmv":"51854390.000--|3"}
cookies= {}
uid = 3249088303

url = 'https://www.toutiao.com/c/user/relation/' +str(uid) + '/'

headers= {
    'authority': 'www.toutiao.com',
    'path':'/c/user/following/?user_id='+str(uid) + '/',
    'if-none-match':'b658298d0ebb1b6c23c37ea7c7db20a5b518992f',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3410.2 Safari/537.36'
}

res = requests.get(url, headers=headers)
soup = BeautifulSoup(res.content, 'html.parser')
scripts = soup.find_all('script')

# userInfo = {
#     id: 3249088303,
#     name: '创业邦',
#     avatarUrl: '//p1.pstatp.com/thumb/1bf3001cb167a60693ce',
#     isPgc: true,
#     isBanned: false,
#     isOwner: false,
#     mediaId: 3249151846,
#     type: '1'
# };

#
# riot.mount('statistics', {
#     guanzhu: '276',
#     fensi: '700238',
#     base_url: '/c/user/relation/3249088303/'
# });

#
# var header = {
#     bg_img: '//s3.pstatp.com/site/tt_mfsroot/pc_img/bg_profile.png' | | '//s3.pstatp.com/site/tt_mfsroot/pc_img/bg_profile.png',
#     avtar_img: '//p1.pstatp.com/thumb/1bf3001cb167a60693ce',
#     name: '创业邦',
#     dv: true,
#     pgc: true,
#     abstract: '每天读一读创业邦，了解与创业有关的人、钱、事儿。',
#     media_id: '3249088303',
#     like: media.like,
#     liked: false,
#     isSelf: userInfo.isOwner,
#     home_url: '/c/user/3249088303/',
#     right_knight_sign_status: '',
#     kbanquan_sign_status: ''
# };

userInfo = r'userInfo = ({.*?});'
follow = r'\'statistics\',\s*({.*?})\);'
header = r'var\s*header\s*=\s*({.*?});'

for script in scripts:
    text = script.get_text()
    user = re.search(userInfo, text,  re.S)
    fans = re.search(follow, text, re.S)
    head = re.search(header, text, re.S)
    if user:
        userlast = user.group(1)
    if fans:
        fanslast = fans.group(1)

    if head:
        headlast= head.group(1)


headlast = headlast.replace('\'||\'', ',')

headlast = headlast.replace('userInfo.isOwner', 'false')
headlast = headlast.replace('media.like', 'false')
infoHead =demjson.decode(headlast)
infoUser = demjson.decode(userlast)
infoFans= demjson.decode(fanslast)
infoHead = demjson.decode(headlast)



# print(infoHead)
#
info = {
    **infoUser,
    **infoFans,
    **infoHead
}
print(info)



