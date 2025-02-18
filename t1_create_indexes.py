import os
from pymongo import MongoClient
from dotenv import load_dotenv

# Load biến môi trường
load_dotenv()

# Kết nối MongoDB
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
client = MongoClient(MONGO_URI)
db = client.education_website  # Chọn database

def create_indexes():
    # Tạo chỉ mục cho trường "email" trong collection "users"
    db.users.create_index([("email", 1)])

    # Tạo chỉ mục cho trường "teacher_id" trong collection "classrooms"
    db.classrooms.create_index([("teacher_id", 1)])

    # Tạo chỉ mục cho trường "section_id" trong collection "sectionFiles"
    db.sectionFiles.create_index([("section_id", 1)])

    # Tạo chỉ mục cho trường "type" trong collection "forumPosts"
    db.forumPosts.create_index([("type", 1)])

    print("Indexes created successfully!")

if __name__ == "__main__":
    create_indexes()
