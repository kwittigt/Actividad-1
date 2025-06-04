from pymongo import MongoClient
import os

def get_client():
    uri = os.getenv("MONGO_URI", "mongodb://localhost:27017")
    return MongoClient(uri)
