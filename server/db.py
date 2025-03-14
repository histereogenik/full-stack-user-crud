import os
from pymongo import MongoClient

def get_database(testing=False):
    uri = os.getenv("MONGO_TEST_URI", "mongodb://localhost:27017/test_database") if testing else os.getenv("MONGO_URI", "mongodb://localhost:27017/mydatabase")
    client = MongoClient(uri)
    db = client.get_default_database()
    return db


db = get_database(testing=False)
users_collection = db["users"]