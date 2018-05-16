# https://www.joinc.co.kr/w/Site/Python/pymongo
# 출처: http://ngee.tistory.com/335 [ngee]

import pymongo

import pymongo
connection = pymongo.MongoClient("localhost", 27017)

db = connection.testDB
collectionInfo = db.collection_names()
print(collectionInfo)
collection  = db.testCollection
#collection.insert({"number":0})

collection.remove({"student_id": {"$gt":-1}})
#collection.remove({"student_id": {"$gt":90}})

for i in range(0, 100):
  collection.insert({"student_id":i})

docs = collection.find()
for doc in docs:
    print(doc)
print("=====================================================")
docs = collection.find({"student_id": {"$gt":90}}) #less than(lt) great than(gt)
for doc in docs:
    print(doc)
#collection.update({"number":0}, {"number":9999})