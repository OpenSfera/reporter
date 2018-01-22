from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client.sfera

def getConfig(key, defaultValue):
    result = db.config.find_one({"key": key})
    if result == None:
        return defaultValue
    else:
        return result["value"]

def addDefaultConfig():
    default = [
        {
            "key": "reporter_sample_time",
            "value": 600 # a sample every 10 minutes ~ 144 per day
        }
    ]
    for doc in default:
        db.config.update_one({"key": doc["key"]}, {"$set": doc}, upsert=True)
