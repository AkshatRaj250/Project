from pymongo import MongoClient

# Connection to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["gymDB"]
collection = db["progress"]

def insert_entry(data):
    collection.insert_one(data)

def fetch_all_entries():
    return list(collection.find())

def delete_entry(entry_id):
    from bson.objectid import ObjectId
    collection.delete_one({"_id": ObjectId(entry_id)})  