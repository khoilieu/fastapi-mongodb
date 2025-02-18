import os
from fastapi import APIRouter, HTTPException, Query
from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId
from models import User
from dotenv import load_dotenv

# Load biến môi trường
load_dotenv()
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")

# Kết nối MongoDB
client = AsyncIOMotorClient(MONGO_URI)
db = client.education_platform

# Khởi tạo router FastAPI
router = APIRouter()

# =========================== CRUD CHO NGƯỜI DÙNG ===========================

# ✅ 1. Tạo người dùng (POST /users/)
@router.post("/users/", response_model=User)
async def create_user(user: User):
    try:
        print(f"📌 Dữ liệu nhận được: {user.dict()}")  # Debug dữ liệu input
                                                
        # Chuyển `_id` sang ObjectId
        user_dict = user.dict(by_alias=True)
        user_dict["_id"] = ObjectId()

        result = await db.user.insert_one(user_dict)

        user_dict["_id"] = str(result.inserted_id)
        return user_dict
    except Exception as e:
        print(f"❌ Lỗi khi tạo user: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ✅ 2. Lấy thông tin người dùng theo ID (GET /users/{id})
@router.get("/users/{id}", response_model=User)
async def get_user(id: str):
    user = await db.user.find_one({"_id": ObjectId(id)})
    if user:
        user["_id"] = str(user["_id"])
        return user
    raise HTTPException(status_code=404, detail="User not found")

# ✅ 3. Cập nhật thông tin người dùng (PATCH /users/{id})
@router.patch("/users/{id}")
async def update_user(id: str, user: User):
    updated_user = await db.user.find_one_and_update(
        {"_id": ObjectId(id)},
        {"$set": user.dict(exclude_unset=True)},
        return_document=True
    )
    if updated_user:
        updated_user["_id"] = str(updated_user["_id"])
        return updated_user
    raise HTTPException(status_code=404, detail="User not found")

# ✅ 4. Xóa người dùng (DELETE /users/{id})
@router.delete("/users/{id}")
async def delete_user(id: str):
    result = await db.user.delete_one({"_id": ObjectId(id)})
    if result.deleted_count:
        return {"message": "User deleted successfully"}
    raise HTTPException(status_code=404, detail="User not found")

# =========================== CRUD CHO BÀI ĐĂNG ===========================

# ✅ 5. Tạo bài đăng với bình luận nhúng (POST /posts/)
@router.post("/posts/")
async def create_post(post: dict):
    post["comments"] = []
    result = await db.post.insert_one(post)
    return {"_id": str(result.inserted_id), **post}

# ✅ 6. Lấy bài đăng theo ID (GET /posts/{id})
@router.get("/posts/{id}")
async def get_post(id: str):
    post = await db.post.find_one({"_id": ObjectId(id)})
    if post:
        post["_id"] = str(post["_id"])
        return post
    raise HTTPException(status_code=404, detail="Post not found")

# ✅ 7. Cập nhật bài đăng (PATCH /posts/{id})
@router.patch("/posts/{id}")
async def update_post(id: str, post: dict):
    updated_post = await db.post.find_one_and_update(
        {"_id": ObjectId(id)},
        {"$set": post},
        return_document=True
    )
    if updated_post:
        updated_post["_id"] = str(updated_post["_id"])
        return updated_post
    raise HTTPException(status_code=404, detail="Post not found")

# ✅ 8. Xóa bài đăng (DELETE /posts/{id})
@router.delete("/posts/{id}")
async def delete_post(id: str):
    result = await db.post.delete_one({"_id": ObjectId(id)})
    if result.deleted_count:
        return {"message": "Post deleted successfully"}
    raise HTTPException(status_code=404, detail="Post not found")

# ✅ 9. Lấy danh sách bài đăng với phân trang, lọc và sắp xếp (GET /posts/)
@router.get("/posts/")
async def get_posts(
    skip: int = Query(0, alias="offset"),
    limit: int = Query(10, alias="limit"),
    sort_by: str = Query("created_at", alias="sort_by"),
    order: int = Query(-1, alias="order")
):
    posts = await db.post.find().sort(sort_by, order).skip(skip).limit(limit).to_list(limit)
    for post in posts:
        post["_id"] = str(post["_id"])
    return posts

# =========================== TRANSACTIONS ===========================

# ✅ 10. Xóa người dùng + tất cả bài đăng của họ
@router.delete("/users/{id}/delete_with_posts")
async def delete_user_with_posts(id: str):
    async with await client.start_session() as session:
        async with session.start_transaction():
            user_deleted = await db.user.delete_one({"_id": ObjectId(id)}, session=session)
            posts_deleted = await db.post.delete_many({"user_id": id}, session=session)
            if user_deleted.deleted_count:
                return {
                    "message": "User and their posts deleted successfully",
                    "deleted_posts": posts_deleted.deleted_count
                }
            raise HTTPException(status_code=404, detail="User not found")
