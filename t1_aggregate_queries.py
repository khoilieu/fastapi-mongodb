import os
from pymongo import MongoClient
from bson import ObjectId
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
client = MongoClient(MONGO_URI)
db = client.education_website 

def aggregate_data():
    user_id = ObjectId("67b44d1ca56f476631a2d4d2")

    total_posts = db.forumPost.aggregate([
        { "$match": { "user_id": user_id } },
        { "$count": "total_posts" }
    ])
    print("Total posts for user:", list(total_posts))

    popular_posts = db.forumPost.aggregate([
        { "$lookup": {
            "from": "forumComment",
            "localField": "_id",
            "foreignField": "forumPost_id",
            "as": "comments"
        }},
        { "$addFields": { "comment_count": { "$size": "$comments" } } },
        { "$project": { "title": 1, "comment_count": 1 } },
        { "$sort": { "comment_count": -1 } }
    ])
    print("Popular posts by comment count:", list(popular_posts))

    avg_comments = db.forumPost.aggregate([
        { "$lookup": {
            "from": "forumComment",
            "localField": "_id",
            "foreignField": "forumPost_id",
            "as": "comments"
        }},
        { "$group": {
            "_id": None,
            "average_comments": { "$avg": { "$size": "$comments" } }
        }}
    ])
    print("Average comments per post:", list(avg_comments))

    avg_questions = db.testQuestion.aggregate([
        { "$lookup": {
            "from": "question",
            "localField": "_id",
            "foreignField": "testQuestion_id",
            "as": "questions"
        }},
        { "$group": {
            "_id": None,
            "average_questions": { "$avg": { "$size": "$questions" } }
        }}
    ])
    print("Average questions per test question:", list(avg_questions))

if __name__ == "__main__":
    aggregate_data()
