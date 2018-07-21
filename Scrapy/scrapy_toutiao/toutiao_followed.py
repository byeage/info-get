import requests
import json

# cookies = {"q_c1":"bad4c8b01e4c4977b1a9fab360c89260|1525686821000|1504749306000","_zap":"ea173538-687f-42ff-b91d-63c913002aff","aliyungf_tc":"AQAAADHaTCn2cgEA6tbnc6pjKCjoJOvN","_xsrf":"8c076352-3489-421c-9170-58ed910b100c","d_c0":"\"AICuQ9Jnjg2PTj-xtGEfQFZXAqFDQl8Qg7w","tgw_l7_route":"156dfd931a77f9586c0da07030f2df36","capsion_ticket":"\"2|1:0|10:1525686817|14:capsion_ticket|44:OWQ4ZDA2NzU5ODE3NDQyOWJhZGZiNWE2MGIyNjUzMzI","l_n_c":"1","r_cap_id":"\"ZTRiNjY1ZmQ3Zjc3NDMyMjllODU2MGNiMDM2OGIwN2Y","cap_id":"\"Y2JhOTlkOTI4ZDA4NGM4ZmI3YjgzMThiZGJhNzU4ZDg","l_cap_id":"\"ZTBkMDBmMWM0YmU1NGU5NjgyM2Y2OWNhMTc1YTk1MDA","n_c":"1","__utma":"51854390.293167018.1525686826.1525686826.1525686826.1","__utmb":"51854390.0.10.1525686826","__utmc":"51854390","__utmz":"51854390.1525686826.1.1.utmcsr","__utmv":"51854390.000--|3"}
cookies= {}
uid = 3249088303
back = requests.get('http://localhost:3000/toutiao/signature/'+str(uid))
_signature = str(back.content)
print(_signature)
url = 'https://www.toutiao.com/c/user/followed/'
params = {
    'user_id': uid,
    'cursor': 0,
    'count': 20,
    '_signature': 'DE3FQQAAVrrzsjq-SjKthQxNxV'
}

headers= {
    'authority': 'www.toutiao.com',
    'path':'/c/user/followed/?user_id='+str(uid)+'&cursor=0&count=20&_signature=DE3FQQAAVrrzsjq-SjKthQxNxV',
    'if-none-match':'b658298d0ebb1b6c23c37ea7c7db20a5b518992f',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3410.2 Safari/537.36',
    'referer':'https://www.toutiao.com/c/user/relation/'+str(uid)+'/?tab=followed',
    'x-udid':'AICuQ9Jnjg2PTj-xtGEfQFZXAqFDQl8Qg7w='
}

res = requests.get(url, params=params, headers=headers)
print(json.loads(res.content))