import pymongo
DATABASE = 'weiboScrapy'

class DBHelper:
    def __init__(self):
        client = pymongo.MongoClient()
        print('instance db')
        self.db = client[DATABASE]
    def add_user(self, email, name):
        self.db.users.insert({
            name: name,
            email: email
        })
    def add_search_card(self, name, keyword):
        self.db.search_cards.insert({
            name: name,
            keyword: keyword
        })
    def add_weiboUserInformation(self, info):
        self.db.userInformation.insert(info)
    def add_weibo(self, weibo):
        self.db.xuke.insert(weibo)
    def add_weiboComment(self, comment):
        self.db.xukeComment.insert(comment)
    def add_weiboForward(self, forward):
        self.db.liuchunForward.insert(forward)
    def add_weiboPraise(self, praise):
        self.db.liucunPraise.insert(praise)

    def add_fans(self, fans):
        self.db.fans.insert(fans)

    def add_wangyi_comment(self, list):
        self.db.wangyiComment.insert(list)
    def add_toutiaousers(self, list):
        self.db.toutiaoUser1.insert_many(list)
    def query_toutiao_user(self, pos):
        return self.db.toutiaoUser1.find().limit(1).skip(pos)


    def create_weibo_musicCreateIndex(self):
        self.db.weiboMusic.create_index('user.id', unique=True)
    def add_weibo_music(self, list):
        for item in list:
            uid = item['user']['id']
            result = self.find_one_weibo_music(uid)
            if result is None:
                # 插入
                print(uid, '还未存在')
                self.db.weiboMusic.insert(item)
            else:
                pass
                print(uid, '已经存在')


    def find_one_weibo_music(self, id):
        result = self.db.weiboMusic.find_one({'user.id': id})
        return  result

    def query_weibo_music_user(self, pos):
        return self.db.weiboMusic.find().limit(1).skip(pos)

    def query_weibo_all_user(self):
        return self.db.weiboMusic.find().sort([('user.followers_count', -1)])

    def add_weibo_music_info(self, list):
        self.db.weiboMusicInfoNews.insert_many(list)
    def add_weibo_music_infoAll(self, list):
        self.db.weiboMusicInfoNewsAll.insert_many(list)
def dbInstance():
    return DBHelper()


if __name__ == '__main__':
    dbHelper = DBHelper()
    # dbHelper.create_weibo_musicCreateIndex()


    dbHelper.find_one_weibo_music(178487791157)

