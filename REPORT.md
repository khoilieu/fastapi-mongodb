# Assignment: MongoDB and FastAPI - Advanced Data Modeling and API Development

## Part 1: Advanced Data Modeling in MongoDB
1. Choose my application: Education Platform.
2. Related entities with complex relationships:
    * User
    * Classroom
    * Subject
    * Section
    * SectionFile
    * Submission
    * SubmissionFile
    * Participant
    * TestQuestion
    * Question
    * Answer
    * ForumPost
    * ForumComment
3. Normalized Schema:
[Click here to see](https://github.com/khoilieu/fastapi-mongodb/blob/main/t1_insert_data_normalized.py)
4. Denormalized Schema
[Click here to see](https://github.com/khoilieu/fastapi-mongodb/blob/main/t1_insert_data_denormalized.py)
5. Implement indexes:
[Click here to see](https://github.com/khoilieu/fastapi-mongodb/blob/main/t1_create_indexes.py)
6. Implement MongoDB Aggregation Pipelines:
[Click here to see](https://github.com/khoilieu/fastapi-mongodb/blob/main/t1_aggregate_queries.py)
7. Use transactions:
[Click here to see](https://github.com/khoilieu/fastapi-mongodb/blob/main/t1_transaction.py)

## Part 2: Implementing API with FastAPI

### main.py:
Initializes and configures the FastAPI application, the main entry point for the API.
```markdown
app = FastAPI()

app.include_router(router)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)
```
### routes.py:
Defines the API routes, mapping URLs to specific functions.
```markdown
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
```
### models.py:
Defines data models, typically classes interacting with the database.
```markdown
class User(BaseModel):
    id: Optional[str] = Field(default=None, alias="_id")
    username: str
    email: EmailStr
    password: str
    role: str  
    disabled: Optional[bool] = False

    class Config:
        populate_by_name = True

class Classroom(BaseModel):
    id: Optional[str] = Field(default=None, alias="_id")
    name: str
    teacher_id: str 
    subject_id: str 

    class Config:
        populate_by_name = True

class Subject(BaseModel):
    id: Optional[str] = Field(default=None, alias="_id")
    name: str
    description: Optional[str] = None

    class Config:
        populate_by_name = True

class Section(BaseModel):
    id: Optional[str] = Field(default=None, alias="_id")
    title: str
    description: str
    classroom_id: str 
    class Config:
        populate_by_name = True

class SectionFile(BaseModel):
    id: Optional[str] = Field(default=None, alias="_id")
    file_name: str
    file_url: str
    section_id: str  

    class Config:
        populate_by_name = True

class Submission(BaseModel):
    id: Optional[str] = Field(default=None, alias="_id")
    title: str
    description: str
    classroom_id: str  

    class Config:
        populate_by_name = True

class SubmissionFile(BaseModel):
    id: Optional[str] = Field(default=None, alias="_id")
    file_name: str
    file_url: str
    submission_id: str 

    class Config:
        populate_by_name = True

class Participant(BaseModel):
    id: Optional[str] = Field(default=None, alias="_id")
    classroom_id: str 
    user_id: str 

    class Config:
        populate_by_name = True

class TestQuestion(BaseModel):
    id: Optional[str] = Field(default=None, alias="_id")
    title: str
    submission_id: str 

    class Config:
        populate_by_name = True

class Question(BaseModel):
    id: Optional[str] = Field(default=None, alias="_id")
    content: str
    testQuestion_id: str 

    class Config:
        populate_by_name = True

class Answer(BaseModel):
    id: Optional[str] = Field(default=None, alias="_id")
    content: str
    is_correct: bool
    question_id: str  

    class Config:
        populate_by_name = True

class ForumPost(BaseModel):
    id: Optional[str] = Field(default=None, alias="_id")
    user_id: str 
    title: str
    content: str
    type: str 

    class Config:
        populate_by_name = True

class ForumComment(BaseModel):
    id: Optional[str] = Field(default=None, alias="_id")
    content: str
    forumPost_id: str  
    user_id: str 

    class Config:
        populate_by_name = True
class ResponseMessage(BaseModel):
    message: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None
    scopes: list[str] = []
```
### auth.py:
Handles user authentication functionality, including login and registration.
```markdown
load_dotenv()
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")

client = AsyncIOMotorClient(MONGO_URI)
db = client.education_website 

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="token",
    scopes={"me": "Read information about the current user.", "items": "Read items."},
)

app = FastAPI()


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


async def get_user(db, username: str):
    user = await db.user.find_one({"username": username})
    if user:
        user["_id"] = str(user["_id"]) 
        return User(**user)


async def authenticate_user(db, username: str, password: str):
    user = await get_user(db, username)
    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    return user


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(
    security_scopes: SecurityScopes, token: Annotated[str, Depends(oauth2_scheme)]
):
    if security_scopes.scopes:
        authenticate_value = f'Bearer scope="{security_scopes.scope_str}"'
    else:
        authenticate_value = "Bearer"
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": authenticate_value},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_scopes = payload.get("scopes", [])
        print(token_scopes)
        token_data = TokenData(scopes=token_scopes, username=username)
    except (InvalidTokenError, ValidationError):
        raise credentials_exception
    user = await get_user(db, username=token_data.username)
    if user is None:
        raise credentials_exception
    for scope in security_scopes.scopes:
        if scope not in token_data.scopes:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Not enough permissions",
                headers={"WWW-Authenticate": authenticate_value},
            )
    return user


async def get_current_active_user(
    current_user: Annotated[User, Security(get_current_user, scopes=["me"])],
):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user
```
### .env:
Stores environment variables such as database configurations or other sensitive information.
```markdown
MONGO_URI="mongodb+srv://admin:<your_password>@cluster0.szq15.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
```
### DockerFile:
Defines the steps to build and configure a Docker container for the application.
```markdown
FROM python:3.10-slim

WORKDIR /code

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]
```


## MY GITHUB
[Click here to see my repository](https://github.com/khoilieu/fastapi-mongodb)