import datetime

from pydantic import BaseModel, field_validator

from domain.user.user_schema import User

class Answer(BaseModel):
    id: int
    content: str
    # question_id: int
    create_date: datetime.datetime
    modify_date: datetime.datetime | None = None
    user: User | None
    question_id: int
    voter: list[User] = []

class AnswerCreate(BaseModel):
    content: str
    
    @field_validator('content')
    def not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError('빈 값은 허용되지 않습니다.')
        return v
    
class AnswerUpdate(AnswerCreate):
    answer_id: int    

class AnswerDelete(BaseModel):
    answer_id: int    

class AnswerVote(BaseModel):
    answer_id: int    