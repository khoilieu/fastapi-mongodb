import os
from bson import ObjectId
from pymongo import MongoClient
from dotenv import load_dotenv

# Load biến môi trường
load_dotenv()
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")

# Kết nối MongoDB
client = MongoClient(MONGO_URI)
db = client.education_website

# Dữ liệu phi chuẩn hóa (Denormalized Data)
def insert_data():
    # 1. Thêm lớp học với thông tin môn học, giáo viên và học sinh
    classroom = {
        "_id": ObjectId(),
        "name": "Class 2B",
        "subject": {
            "name": "Chemistry",
            "description": "High School Chemistry Course"
        },
        "teacher": {
            "_id": ObjectId(),
            "username": "teacher_chemistry",
            "email": "teacher.chemistry@example.com",
            "password": "hashed_password_teacher",
            "role": "teacher"
        },
        "students": [
            {
                "_id": ObjectId(),
                "username": "student_alex",
                "email": "alex.student@example.com",
                "password": "hashed_password_student",
                "role": "student"
            },
            {
                "_id": ObjectId(),
                "username": "student_jane",
                "email": "jane.student@example.com",
                "password": "hashed_password_student",
                "role": "student"
            }
        ],
        "sections": [
            {
                "_id": ObjectId(),
                "title": "Section 1: Introduction to Chemistry",
                "description": "Basics of Chemistry",
                "files": [
                    {
                        "_id": ObjectId(),
                        "file_name": "chemistry_intro.pdf",
                        "file_url": "http://example.com/chemistry_intro.pdf"
                    }
                ]
            }
        ],
        "submissions": [
            {
                "_id": ObjectId(),
                "title": "Chemistry Assignment 1",
                "description": "Solve the given chemistry problems",
                "files": [
                    {
                        "_id": ObjectId(),
                        "file_name": "chemistry_assignment.pdf",
                        "file_url": "http://example.com/chemistry_assignment.pdf"
                    }
                ]
            }
        ],
        "test_questions": [
            {
                "_id": ObjectId(),
                "title": "Chemistry Test - Basics",
                "questions": [
                    {
                        "_id": ObjectId(),
                        "content": "What is the chemical symbol for water?",
                        "answers": [
                            {
                                "_id": ObjectId(),
                                "content": "H2O",
                                "is_correct": True
                            },
                            {
                                "_id": ObjectId(),
                                "content": "O2",
                                "is_correct": False
                            }
                        ]
                    },
                    {
                        "_id": ObjectId(),
                        "content": "What is the atomic number of carbon?",
                        "answers": [
                            {
                                "_id": ObjectId(),
                                "content": "6",
                                "is_correct": True
                            },
                            {
                                "_id": ObjectId(),
                                "content": "12",
                                "is_correct": False
                            }
                        ]
                    }
                ]
            }
        ],
        "forum_posts": [
            {
                "_id": ObjectId(),
                "user_id": ObjectId(),  # ID của học sinh
                "title": "Discussion on Chemistry",
                "content": "Let's discuss chemical reactions",
                "comments": [
                    {
                        "_id": ObjectId(),
                        "user_id": ObjectId(),  # ID của học sinh
                        "content": "I think chemistry is fascinating!"
                    }
                ]
            }
        ]
    }

    # Chèn tài liệu vào bộ sưu tập `classroom`
    db.classroom.insert_one(classroom)

if __name__ == "__main__":
    insert_data()
    print("✅ Denormalized data inserted successfully!")
