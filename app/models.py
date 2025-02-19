from pydantic import BaseModel, Field, EmailStr
from typing import Optional

# ✅ 1. User Model
class User(BaseModel):
    id: Optional[str] = Field(default=None, alias="_id")
    username: str
    email: EmailStr
    password: str
    role: str  # student | teacher | admin
    disabled: Optional[bool] = False

    class Config:
        populate_by_name = True

# ✅ 2. Classroom Model
class Classroom(BaseModel):
    id: Optional[str] = Field(default=None, alias="_id")
    name: str
    teacher_id: str  # Liên kết với giáo viên
    subject_id: str  # Liên kết với môn học

    class Config:
        populate_by_name = True

# ✅ 3. Subject Model
class Subject(BaseModel):
    id: Optional[str] = Field(default=None, alias="_id")
    name: str
    description: Optional[str] = None

    class Config:
        populate_by_name = True

# ✅ 4. Section Model
class Section(BaseModel):
    id: Optional[str] = Field(default=None, alias="_id")
    title: str
    description: str
    classroom_id: str  # Liên kết với lớp học

    class Config:
        populate_by_name = True

# ✅ 5. SectionFile Model
class SectionFile(BaseModel):
    id: Optional[str] = Field(default=None, alias="_id")
    file_name: str
    file_url: str
    section_id: str  # Liên kết với chương học

    class Config:
        populate_by_name = True

# ✅ 6. Submission Model
class Submission(BaseModel):
    id: Optional[str] = Field(default=None, alias="_id")
    title: str
    description: str
    classroom_id: str  # Liên kết với lớp học

    class Config:
        populate_by_name = True

# ✅ 7. SubmissionFile Model
class SubmissionFile(BaseModel):
    id: Optional[str] = Field(default=None, alias="_id")
    file_name: str
    file_url: str
    submission_id: str  # Liên kết với bài nộp

    class Config:
        populate_by_name = True

# ✅ 8. Participant Model
class Participant(BaseModel):
    id: Optional[str] = Field(default=None, alias="_id")
    classroom_id: str  # Liên kết với lớp học
    user_id: str  # Liên kết với người tham gia (học sinh/giáo viên)

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
