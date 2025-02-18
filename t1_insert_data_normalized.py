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

# Dữ liệu chuẩn hóa (Normalized Data)
def insert_data():
    # 1. Subject Collection
    subject = {
        "_id": ObjectId(),
        "name": "Mathematics"
    }
    subject_id = db.subject.insert_one(subject).inserted_id

    # 2. User Collection
    users = [
        {
            "_id": ObjectId(),
            "username": "teacher_1",
            "email": "teacher1@example.com",
            "password": "password1",
            "role": "teacher"
        },
        {
            "_id": ObjectId(),
            "username": "student_1",
            "email": "student1@example.com",
            "password": "password1",
            "role": "student"
        }
    ]
    user_ids = [db.user.insert_one(user).inserted_id for user in users]

    # 3. Classroom Collection
    classroom = {
        "_id": ObjectId(),
        "name": "Class 1A",
        "teacher_id": user_ids[0],  # Giáo viên của lớp học
        "subject_id": subject_id
    }
    classroom_id = db.classroom.insert_one(classroom).inserted_id

    # 4. Section Collection
    section = {
        "_id": ObjectId(),
        "title": "Section 1: Algebra",
        "description": "Introduction to Algebra",
        "classroom_id": classroom_id
    }
    section_id = db.section.insert_one(section).inserted_id

    # 5. SectionFile Collection
    section_file = {
        "_id": ObjectId(),
        "file_name": "algebra_notes.pdf",
        "file_url": "http://example.com/algebra_notes.pdf",
        "section_id": section_id
    }
    db.sectionFile.insert_one(section_file)

    # 6. Submission Collection
    submission = {
        "_id": ObjectId(),
        "title": "Algebra Assignment 1",
        "description": "Solve the given algebra problems",
        "classroom_id": classroom_id
    }
    submission_id = db.submission.insert_one(submission).inserted_id

    # 7. SubmissionFile Collection
    submission_file = {
        "_id": ObjectId(),
        "file_name": "algebra_assignment.pdf",
        "file_url": "http://example.com/algebra_assignment.pdf",
        "submission_id": submission_id
    }
    db.submissionFile.insert_one(submission_file)

    # 8. Participant Collection
    participant = {
        "_id": ObjectId(),
        "classroom_id": classroom_id,
        "user_id": user_ids[1]  # Student tham gia lớp học
    }
    db.participant.insert_one(participant)

    # 9. TestQuestion Collection
    test_question = {
        "_id": ObjectId(),
        "title": "Math Test - Algebra Basics",
        "submission_id": submission_id
    }
    test_question_id = db.testQuestion.insert_one(test_question).inserted_id

    # 10. Question Collection
    questions = [
        {
            "_id": ObjectId(),
            "content": "What is x in the equation 2x + 3 = 7?",
            "testQuestion_id": test_question_id
        },
        {
            "_id": ObjectId(),
            "content": "Solve for y: 3y - 5 = 10",
            "testQuestion_id": test_question_id
        }
    ]
    question_ids = [db.question.insert_one(q).inserted_id for q in questions]

    # 11. Answer Collection
    answers = [
        {
            "_id": ObjectId(),
            "content": "x = 2",
            "is_correct": True,
            "question_id": question_ids[0]
        },
        {
            "_id": ObjectId(),
            "content": "x = 3",
            "is_correct": False,
            "question_id": question_ids[0]
        }
    ]
    db.answer.insert_many(answers)

    # 12. ForumPost Collection (✅ **Cập nhật: thêm `user_id` cho bài đăng**)
    forum_post = {
        "_id": ObjectId(),
        "user_id": user_ids[1],  # 🛠 Người post bài là học sinh
        "title": "Discussion on Algebra",
        "content": "Let's discuss algebraic equations",
        "type": "discuss"
    }
    forum_post_id = db.forumPost.insert_one(forum_post).inserted_id

    # 13. ForumComment Collection
    forum_comment = {
        "_id": ObjectId(),
        "content": "I think algebra is fun!",
        "forumPost_id": forum_post_id,
        "user_id": user_ids[1]  # Học sinh bình luận
    }
    db.forumComment.insert_one(forum_comment)

if __name__ == "__main__":
    insert_data()
    print("✅ Data inserted successfully!")
