from pydantic import BaseModel, Field
from typing import Optional, List, Dict
from datetime import datetime

class User(BaseModel):
    id: Optional[str] = Field(default=None, alias="_id")
    name: str
    email: str
    password: str
    role: str  # student | teacher | admin
    enrolled_classrooms: List[str] = []

    class Config:
        populate_by_name = True

# ✅ 2. Classroom (Lớp học)
class Classroom(BaseModel):
    id: Optional[str] = Field(default=None, alias="_id")
    name: str
    subject_id: str
    teacher_id: str
    participants: List[str] = []

    class Config:
        populate_by_name = True

# ✅ 3. Subject (Môn học)
class Subject(BaseModel):
    id: Optional[str] = Field(default=None, alias="_id")
    name: str
    description: str

    class Config:
        populate_by_name = True

# ✅ 4. Section (Chương)
class Section(BaseModel):
    id: Optional[str] = Field(default=None, alias="_id")
    title: str
    classroom_id: str

    class Config:
        populate_by_name = True

# ✅ 5. SubsectionFile (Tài liệu)
class SubsectionFile(BaseModel):
    id: Optional[str] = Field(default=None, alias="_id")
    section_id: str
    file_url: str

    class Config:
        populate_by_name = True

# ✅ 6. Submission (Bài nộp)
class Submission(BaseModel):
    id: Optional[str] = Field(default=None, alias="_id")
    student_id: str
    classroom_id: str
    file_ids: List[str]

    class Config:
        populate_by_name = True

# ✅ 7. SubmissionFile (File bài nộp)
class SubmissionFile(BaseModel):
    id: Optional[str] = Field(default=None, alias="_id")
    submission_id: str
    file_url: str

    class Config:
        populate_by_name = True

# ✅ 8. Comment (Bình luận)
class Comment(BaseModel):
    id: Optional[str] = Field(default=None, alias="_id")
    user_id: str
    text: str
    context: Dict[str, str]  # {"type": "classroom", "id": ObjectId}

    class Config:
        populate_by_name = True

# ✅ 9. Participant (Thành viên lớp học)
class Participant(BaseModel):
    id: Optional[str] = Field(default=None, alias="_id")
    classroom_id: str
    user_id: str
    role: str  # student | teacher

    class Config:
        populate_by_name = True

# ✅ 10. Question (Câu hỏi)
class Question(BaseModel):
    id: Optional[str] = Field(default=None, alias="_id")
    classroom_id: str
    text: str

    class Config:
        populate_by_name = True

# ✅ 11. Answer (Đáp án)
class Answer(BaseModel):
    id: Optional[str] = Field(default=None, alias="_id")
    question_id: str
    user_id: str
    text: str

    class Config:
        populate_by_name = True

# ✅ 12. TestResult (Kết quả bài kiểm tra)
class TestResult(BaseModel):
    id: Optional[str] = Field(default=None, alias="_id")
    student_id: str
    classroom_id: str
    score: int

    class Config:
        populate_by_name = True

# ✅ 13. AnsweredQuestion (Câu hỏi đã trả lời)
class AnsweredQuestion(BaseModel):
    id: Optional[str] = Field(default=None, alias="_id")
    test_result_id: str
    question_id: str
    answer: str

    class Config:
        populate_by_name = True

# ✅ 14. ChatMessage (Tin nhắn)
class ChatMessage(BaseModel):
    id: Optional[str] = Field(default=None, alias="_id")
    sender_id: str
    receiver_id: str
    message: str
    timestamp: datetime

    class Config:
        populate_by_name = True

# ✅ 15. Favorite (Mục yêu thích)
class Favorite(BaseModel):
    id: Optional[str] = Field(default=None, alias="_id")
    user_id: str
    item_type: str  # post | classroom | subject
    item_id: str

    class Config:
        populate_by_name = True

# ✅ 16. BlockedParticipant (Danh sách chặn)
class BlockedParticipant(BaseModel):
    id: Optional[str] = Field(default=None, alias="_id")
    blocker_id: str
    blocked_id: str

    class Config:
        populate_by_name = True

# ✅ 17. ForumPost (Bài đăng trên diễn đàn)
class ForumPost(BaseModel):
    id: Optional[str] = Field(default=None, alias="_id")
    user_id: str
    title: str
    content: str
    created_at: datetime

    class Config:
        populate_by_name = True

# ✅ 18. ForumComment (Bình luận trên diễn đàn)
class ForumComment(BaseModel):
    id: Optional[str] = Field(default=None, alias="_id")
    post_id: str
    user_id: str
    text: str

    class Config:
        populate_by_name = True

# ✅ 19. ChatbotResponse (Trả lời tự động từ chatbot)
class ChatbotResponse(BaseModel):
    id: Optional[str] = Field(default=None, alias="_id")
    question: str
    answer: str

    class Config:
        populate_by_name = True

# ✅ 20. Notification (Thông báo)
class Notification(BaseModel):
    id: Optional[str] = Field(default=None, alias="_id")
    user_id: str
    message: str
    created_at: datetime

    class Config:
        populate_by_name = True
