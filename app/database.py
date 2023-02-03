from pymongo import mongo_client
import pymongo
from app.config import settings

client = mongo_client.MongoClient(settings.DATABASE_URL)
print('Connected to MongoDB...')

db = client[settings.MONGO_INITDB_DATABASE]
User = db.users
Candidate= db.candidates

User.create_index([("email", pymongo.ASCENDING)], unique=True)
Candidate.create_index([("email", pymongo.ASCENDING)], unique=True)
