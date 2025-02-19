from app import auth
import os
from datetime import timedelta
from typing import Annotated, List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, Security
from fastapi.security import OAuth2PasswordRequestForm
from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId
from app.models import User, ForumPost, ResponseMessage, Token
from dotenv import load_dotenv

load_dotenv()
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")

client = AsyncIOMotorClient(MONGO_URI)
db = client.education_website 

router = APIRouter()

@router.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> Token:
    user = await auth.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    access_token_expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token(
        data={"sub": user.username, "scopes": form_data.scopes},
        expires_delta=access_token_expires,
    )
    return Token(access_token=access_token, token_type="bearer")

@router.get("/users/me/", response_model=User)
async def read_users_me(
    current_user: Annotated[User, Depends(auth.get_current_active_user)],
):
    return current_user

@router.get("/users/me/items/")
async def read_own_items(
    current_user: Annotated[User, Security(auth.get_current_active_user, scopes=["items"])],
):
    return [{"item_id": "Foo", "owner": current_user.username}]

@router.get("/status/")
async def read_system_status(current_user: Annotated[User, Depends(auth.get_current_user)]):
    return {"status": "ok"}


@router.get("/posts/", response_model=List[ForumPost])
async def fetch_posts(
    page: int = Query(1, ge=1), 
    page_size: int = Query(10, le=100),  
    title: Optional[str] = None,  
    post_type: Optional[str] = None, 
    user_id: Optional[str] = None, 
    sort_by: Optional[str] = Query("created_at", enum=["created_at", "title"]),
    order: Optional[str] = Query("desc", enum=["asc", "desc"]) 
):
    query = {}

    if title:
        query["title"] = {"$regex": title, "$options": "i"}  
    if post_type:
        query["type"] = post_type
    if user_id:
        query["user_id"] = ObjectId(user_id)

    sort_order = 1 if order == "asc" else -1
    sort_field = {sort_by: sort_order}

    posts = await db.forumPost.find(query).sort(sort_field).skip((page - 1) * page_size).limit(page_size).to_list(page_size)
    
    for post in posts:
        post["_id"] = str(post["_id"])
        post["user_id"] = str(post["user_id"])

    return posts

# ✅ Create a User (POST /users/)
@router.post("/users/", response_model=ResponseMessage)
async def create_user(user: User):
    existing_user = await db.user.find_one({"email": user.email})
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_password = auth.get_password_hash(user.password)

    user_data = user.dict(by_alias=True)
    user_data["_id"] = ObjectId()
    user_data["password"] = hashed_password 

    await db.user.insert_one(user_data)

    return {"message": "✅ User created successfully!"}

# ✅ Get a User by ID (GET /users/{id})
@router.get("/users/{id}", response_model=User)
async def get_user(id: str):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="Invalid user ID format")

    user = await db.user.find_one({"_id": ObjectId(id)})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user["_id"] = str(user["_id"])
    return user

# ✅ Update a User (PATCH /users/{id})
@router.patch("/users/{id}", response_model=ResponseMessage)
async def update_user(id: str, update_data: dict):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="Invalid user ID format")

    update_fields = {key: value for key, value in update_data.items() if value is not None}
    if not update_fields:
        raise HTTPException(status_code=400, detail="No valid fields to update")

    result = await db.user.update_one({"_id": ObjectId(id)}, {"$set": update_fields})

    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="User not found or no changes applied")

    return {"message": "✅ User updated successfully!"}

# ✅ Delete a User (DELETE /users/{id})
@router.delete("/users/{id}", response_model=ResponseMessage)
async def delete_user(id: str):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="Invalid user ID format")

    result = await db.user.delete_one({"_id": ObjectId(id)})

    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="User not found")

    return {"message": "✅ User deleted successfully!"}

# ✅ Create a Post (POST /posts/)
@router.post("/posts/", response_model=ResponseMessage)
async def create_post(post: ForumPost):
    post_data = post.dict(by_alias=True)
    post_data["_id"] = ObjectId()

    await db.forumPost.insert_one(post_data)
    return {"message": "✅ Post created successfully!"}

# ✅ Get a Post by ID (GET /posts/{id})
@router.get("/posts/{id}", response_model=ForumPost)
async def get_post(id: str):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="Invalid post ID format")

    post = await db.forumPost.find_one({"_id": ObjectId(id)})
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    post["_id"] = str(post["_id"])
    return post

# ✅ Update a Post (PATCH /posts/{id})
@router.patch("/posts/{id}", response_model=ResponseMessage)
async def update_post(id: str, update_data: dict):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="Invalid post ID format")

    update_fields = {key: value for key, value in update_data.items() if value is not None}
    if not update_fields:
        raise HTTPException(status_code=400, detail="No valid fields to update")

    result = await db.forumPost.update_one({"_id": ObjectId(id)}, {"$set": update_fields})

    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Post not found or no changes applied")

    return {"message": "✅ Post updated successfully!"}

# ✅ Delete a Post (DELETE /posts/{id})
@router.delete("/posts/{id}", response_model=ResponseMessage)
async def delete_post(id: str):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="Invalid post ID format")

    result = await db.forumPost.delete_one({"_id": ObjectId(id)})

    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Post not found")

    return {"message": "✅ Post deleted successfully!"}

@router.post("/create_user_and_post/")
async def create_user_and_post(user: User, post: ForumPost):
    session = await client.start_session() 

    async with session.start_transaction():
        user_data = user.dict(by_alias=True)
        user_data["_id"] = ObjectId()
        user_data["password"] = auth.get_password_hash(user.password)
        await db.user.insert_one(user_data, session=session)

        post_data = post.dict(by_alias=True)
        post_data["_id"] = ObjectId()
        await db.forumPost.insert_one(post_data, session=session)

    return {"message": "✅ User and Post created successfully in transaction!"}
