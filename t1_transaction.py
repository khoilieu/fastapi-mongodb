import os
from pymongo import MongoClient
from bson import ObjectId
from dotenv import load_dotenv

# Load biến môi trường từ file .env
load_dotenv()

# Kết nối MongoDB
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
client = MongoClient(MONGO_URI)

# Chọn database
db = client.education_website

def run_transaction():
    """Thực hiện transaction để insert dữ liệu vào nhiều collection trong MongoDB."""
    with client.start_session() as session:
        with session.start_transaction():
            try:
                # 1️⃣ Thêm môn học (Subject Collection)
                subject = {
                    "_id": ObjectId(),
                    "name": "Physics",
                    "description": "High School Physics Course"
                }
                subject_id = db.subject.insert_one(subject, session=session).inserted_id

                # 2️⃣ Thêm người dùng (User Collection)
                users = [
                    {
                        "_id": ObjectId(),
                        "username": "teacher_physics",
                        "email": "teacher.physics@example.com",
                        "password": "hashed_password_teacher",
                        "role": "teacher"
                    },
                    {
                        "_id": ObjectId(),
                        "username": "student_ken",
                        "email": "ken.student@example.com",
                        "password": "hashed_password_student",
                        "role": "student"
                    }
                ]
                user_ids = [db.user.insert_one(user, session=session).inserted_id for user in users]

                # 3️⃣ Thêm lớp học (Classroom Collection)
                classroom = {
                    "_id": ObjectId(),
                    "name": "Physics 101",
                    "teacher_id": user_ids[0],  # Liên kết với giáo viên
                    "subject_id": subject_id
                }
                classroom_id = db.classroom.insert_one(classroom, session=session).inserted_id

                # 4️⃣ Thêm chương học (Section Collection)
                section = {
                    "_id": ObjectId(),
                    "title": "Newton’s Laws",
                    "description": "Introduction to Newton's Laws of Motion",
                    "classroom_id": classroom_id
                }
                section_id = db.section.insert_one(section, session=session).inserted_id

                # 5️⃣ Thêm tài liệu của chương học (SectionFile Collection)
                section_file = {
                    "_id": ObjectId(),
                    "file_name": "newtons_laws.pdf",
                    "file_url": "https://example.com/newtons_laws.pdf",
                    "section_id": section_id
                }
                db.sectionFile.insert_one(section_file, session=session)

                # 6️⃣ Thêm bài nộp (Submission Collection)
                submission = {
                    "_id": ObjectId(),
                    "title": "Newton’s Laws Homework",
                    "description": "Solve the given physics problems",
                    "classroom_id": classroom_id
                }
                submission_id = db.submission.insert_one(submission, session=session).inserted_id

                # 7️⃣ Thêm bài kiểm tra (TestQuestion Collection)
                test_question = {
                    "_id": ObjectId(),
                    "title": "Physics Test - Newton’s Laws",
                    "submission_id": submission_id
                }
                test_question_id = db.testQuestion.insert_one(test_question, session=session).inserted_id

                # 8️⃣ Thêm câu hỏi (Question Collection)
                question = {
                    "_id": ObjectId(),
                    "content": "What is Newton's First Law?",
                    "testQuestion_id": test_question_id
                }
                question_id = db.question.insert_one(question, session=session).inserted_id

                # 9️⃣ Thêm đáp án (Answer Collection)
                answer = {
                    "_id": ObjectId(),
                    "content": "An object at rest stays at rest, and an object in motion stays in motion unless acted upon by an external force.",
                    "is_correct": True,
                    "question_id": question_id
                }
                db.answer.insert_one(answer, session=session)

                # 🔟 Thêm bài đăng trên diễn đàn (ForumPost Collection)
                forum_post = {
                    "_id": ObjectId(),
                    "user_id": user_ids[1],  # Student là người đăng bài
                    "title": "Understanding Newton’s First Law",
                    "content": "Can someone explain the real-world applications of Newton’s First Law?",
                    "type": "discuss"
                }
                forum_post_id = db.forumPost.insert_one(forum_post, session=session).inserted_id

                # 1️⃣1️⃣ Thêm bình luận vào bài viết (ForumComment Collection)
                forum_comment = {
                    "_id": ObjectId(),
                    "post_id": forum_post_id,
                    "user_id": user_ids[1],
                    "text": "I think seatbelts in cars are a good example!"
                }
                db.forumComment.insert_one(forum_comment, session=session)

                # 1️⃣2️⃣ Thêm thành viên vào lớp học (Participant Collection)
                participant = {
                    "_id": ObjectId(),
                    "classroom_id": classroom_id,
                    "user_id": user_ids[1],  # Student tham gia lớp
                    "role": "student"
                }
                db.participant.insert_one(participant, session=session)

                # ✅ Nếu mọi thao tác thành công, commit transaction
                session.commit_transaction()
                print("✅ Transaction committed successfully!")

            except Exception as e:
                # ❌ Nếu có lỗi, rollback transaction
                session.abort_transaction()
                print(f"❌ Transaction aborted due to error: {e}")

if __name__ == "__main__":
    run_transaction()
