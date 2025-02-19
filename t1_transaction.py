import os
from pymongo import MongoClient
from bson import ObjectId
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
client = MongoClient(MONGO_URI)

db = client.education_website

def run_transaction():
    with client.start_session() as session:
        with session.start_transaction():
            try:
                subject = {
                    "_id": ObjectId(),
                    "name": "Physics",
                    "description": "High School Physics Course"
                }
                subject_id = db.subject.insert_one(subject, session=session).inserted_id

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

                classroom = {
                    "_id": ObjectId(),
                    "name": "Physics 101",
                    "teacher_id": user_ids[0], 
                    "subject_id": subject_id
                }
                classroom_id = db.classroom.insert_one(classroom, session=session).inserted_id

                section = {
                    "_id": ObjectId(),
                    "title": "Newton’s Laws",
                    "description": "Introduction to Newton's Laws of Motion",
                    "classroom_id": classroom_id
                }
                section_id = db.section.insert_one(section, session=session).inserted_id

                section_file = {
                    "_id": ObjectId(),
                    "file_name": "newtons_laws.pdf",
                    "file_url": "https://example.com/newtons_laws.pdf",
                    "section_id": section_id
                }
                db.sectionFile.insert_one(section_file, session=session)

                submission = {
                    "_id": ObjectId(),
                    "title": "Newton’s Laws Homework",
                    "description": "Solve the given physics problems",
                    "classroom_id": classroom_id
                }
                submission_id = db.submission.insert_one(submission, session=session).inserted_id

                test_question = {
                    "_id": ObjectId(),
                    "title": "Physics Test - Newton’s Laws",
                    "submission_id": submission_id
                }
                test_question_id = db.testQuestion.insert_one(test_question, session=session).inserted_id

                question = {
                    "_id": ObjectId(),
                    "content": "What is Newton's First Law?",
                    "testQuestion_id": test_question_id
                }
                question_id = db.question.insert_one(question, session=session).inserted_id

                answer = {
                    "_id": ObjectId(),
                    "content": "An object at rest stays at rest, and an object in motion stays in motion unless acted upon by an external force.",
                    "is_correct": True,
                    "question_id": question_id
                }
                db.answer.insert_one(answer, session=session)

                forum_post = {
                    "_id": ObjectId(),
                    "user_id": user_ids[1],
                    "title": "Understanding Newton’s First Law",
                    "content": "Can someone explain the real-world applications of Newton’s First Law?",
                    "type": "discuss"
                }
                forum_post_id = db.forumPost.insert_one(forum_post, session=session).inserted_id

                forum_comment = {
                    "_id": ObjectId(),
                    "post_id": forum_post_id,
                    "user_id": user_ids[1],
                    "text": "I think seatbelts in cars are a good example!"
                }
                db.forumComment.insert_one(forum_comment, session=session)

                participant = {
                    "_id": ObjectId(),
                    "classroom_id": classroom_id,
                    "user_id": user_ids[1], 
                    "role": "student"
                }
                db.participant.insert_one(participant, session=session)

                session.commit_transaction()
                print("✅ Transaction committed successfully!")

            except Exception as e:
                session.abort_transaction()
                print(f"❌ Transaction aborted due to error: {e}")

if __name__ == "__main__":
    run_transaction()
