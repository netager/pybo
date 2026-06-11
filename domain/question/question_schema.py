import datetime

from pydantic import BaseModel, field_validator

from domain.answer.answer_schema import Answer
from domain.user.user_schema import User

class QuestionCreate(BaseModel):
    subject: str
    content: str

    @field_validator('subject', 'content')
    def not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError('빈 값은 허용되지 않습니다.')
        return v

class Question(BaseModel):
    id: int
    subject: str
    # subject: str | None = None
    content: str
    create_date: datetime.datetime
    modify_date: datetime.datetime | None = None
    # Answer 모델은 Question 모델과 answers라는 이름으로 연결되어 있다.: models.py 참조 
    # Answer 모델에 Queston 모델을 연결할 때 backref="answers" 속성을 지정했기 때문이다. 
    # 따라서 Qestion 스키마에도 answers라는 이름의 속성을 사용해야 등록된 답변들이 정확하게 매핑된다. 만약 answers 대신 다른 이름을 사용한다면 값이 채워지지 않을 것이다.
    answers: list[Answer] = []
    user: User | None
    sta: int | None = None
    voter: list[User] = []
    
class QuestionList(BaseModel):
    total: int = 0
    question_list: list[Question] = []    

class QuestionUpdate(QuestionCreate):
    question_id: int
    
class QuestionDelete(BaseModel):
    question_id: int    

class QuestionVote(BaseModel):
    question_id: int