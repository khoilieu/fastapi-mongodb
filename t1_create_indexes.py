import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
client = MongoClient(MONGO_URI)
db = client.education_website 

def create_indexes():
    db.users.create_index([("email", 1)])

    db.classrooms.create_index([("teacher_id", 1)])

    db.sectionFiles.create_index([("section_id", 1)])

    db.forumPosts.create_index([("type", 1)])

    print("Indexes created successfully!")

if __name__ == "__main__":
    create_indexes()
