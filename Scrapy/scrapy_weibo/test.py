# import json
# from functools import reduce
# with open('1.json','r', encoding='utf-8') as f:
#     obj = json.loads(f.read())
#     cardGroups = obj['data']['cards']
#     cardGroupList = []
#     for group in cardGroups:
#         cardGroupList.extend(group['card_group'])
#     cardGroupList = filter(lambda x: x['card_type'] == 9, cardGroupList)
#     cardGroupList = list(cardGroupList)
#
#
#
# def processJSON(res):
#     cardGroups = res['data']['cards']
#     cardGroupList = []
#     for group in cardGroups:
#         cardGroupList.extend(group['card_group'])
#     cardGroupList = filter(lambda x: x['card_type'] == 9, cardGroupList)
#     cardGroupList = list(cardGroupList)
#
#     extraInfo = res['data']['cardlistInfo']
#     extra = {
#         'total': extraInfo['total'],
#         'pageSize': extraInfo['page_size'],
#         'page': extraInfo['page']
#     }
#     return {
#         list: cardGroupList,
#         extra: extra
#     }


from db import mdb


dbInstance = mdb.dbInstance()