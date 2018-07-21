import csv
import pymongo
DATABASE = 'weiboScrapy'

client = pymongo.MongoClient()
db = client[DATABASE]
collection = db['weiboMusic']

result = collection.find().sort([('user.followers_count', -1)]).limit(500)

def getUser(item):
    return item['user']

users =  list(map(getUser, list(result)))


userKeys = users[0].keys()
header = ('name', 'avatar', 'home', 'followers_count', 'id')
userKeys = ('screen_name', 'profile_image_url', 'profile_url', 'followers_count', 'id')
with open('music.csv', 'wt') as f:
    writer = csv.writer(f)
    writer.writerow(header)
    for user in users:
        val = (user[k] for k in userKeys)
        writer.writerow(val)



# with open('./event.csv', 'rU', encoding='utf-8') as f:
#     reader = csv.reader(f, dialect=csv.excel_tab)
#     print('Data from the CSV', list(reader))


#
# with open('./event.csv', 'rU', encoding='utf-8') as f:
#     reader = csv.DictReader(f, dialect=csv.excel_tab)
#     print('fieldnames:', reader.fieldnames)
#     print('dialect:', reader.dialect)
#     print('line_num:', reader.line_num)
#     for row in reader:
#         print(row)
#     print('Data from the CSV', list(reader))

# print('Available Dialects:' , csv.list_dialects())
# names = ["John", "Eve", "Fate", "Jadon"]
# grades = ["C", "A+", "A", "B-"]
# with open('new.csv', 'wt') as f:
#     writer = csv.writer(f, delimiter='\t', lineterminator='\n\n' )
#     writer.writerow(('Sr.', 'Names', 'Grades'))
#     for i in range(4):
#         writer.writerow((i+1, names[i], grades[i]))




# print('Available Dialects:' , csv.list_dialects())





