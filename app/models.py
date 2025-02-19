from pydantic import BaseModel, Field, EmailStr
from typing import Optional

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
