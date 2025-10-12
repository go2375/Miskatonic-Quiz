from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client.miskatonic

def get_user_collection():
    return db.users

def get_quiz_collection():
    return db.questionnaire