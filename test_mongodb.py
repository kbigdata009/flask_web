from pymongo import MongoClient
import json

# 방법1 - URI
mongodb_URI = "mongodb+srv://root:1234@ubion9.fcwrafy.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(mongodb_URI)

# 방법2 - HOST, PORT
# client = MongoClient(host='localhost', port=27017)

db = client.ubion
data = db.mydata
# print(client.list_database_names())

# data.insert_one({
#     "username":"park",
#     "password":"5678"
# })

cursor = data.find({"username":"kimk"})
print(list(cursor))

cursor_1 = data.find_one({"username":"kimk"})
print(cursor_1)
