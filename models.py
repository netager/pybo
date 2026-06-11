from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Table
from sqlalchemy.orm import relationship

from database import Base

# Many to Many 관계 테이블
# ManyToMany 관계를 적용하기 위해서는 sqlalchemy의 Table을 사용하여 N:N 관계를 
# 의미하는 테이블을 먼저 생성
question_voter = Table(
    'question_voter',
    Base.metadata,      # database.py 에 정의
    Column('user_id', Integer, ForeignKey('user.id'), primary_key=True),
    Column('question_id', Integer, ForeignKey('question.id'), primary_key=True)
)        

answer_voter = Table(
    'answer_voter',
    Base.metadata,      # database.py 에 정의
    Column('user_id', Integer, ForeignKey('user.id'), primary_key=True),
    Column('answer_id', Integer, ForeignKey('answer.id'), primary_key=True)
)        


class Question(Base):
    __tablename__ = "question"
    
    id = Column(Integer, primary_key=True)
    subject = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    create_date = Column(DateTime, nullable=False)
    modify_date = Column(DateTime, nullable=True)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=True)
    user = relationship("User", backref="question_users")
    sta = Column(Integer, nullable=True)
    voter = relationship('User', secondary=question_voter, backref='question_voters')

    
class Answer(Base):
    __tablename__ = "answer"

    id = Column(Integer, primary_key=True)
    content = Column(Text, nullable=False)
    create_date = Column(DateTime, nullable=False)
    modify_date = Column(DateTime, nullable=True)
    
    # question_id 속성은 답변을 질문과 연결하기 위해 추가한 속성
    # ForeignKey의 첫번째 파라미터 "question.id"는 question 테이블의 id 컬럼 의미, question 객체의 id를 의미하는 것이 아님.
    # 즉, Answer 모델의 question_id 속성은 question 테이블의 id 컬럼과 연결된다는 뜻.
    question_id = Column(Integer, ForeignKey("question.id"))
    
    # 답변 모델에서 질문 모델을 참조하기 위해 추가
    # relationship 으로 question 속성을 생성하면 답변 객체(answer)에서 연결된 질문의 
    # 제목을 answer.question.subject 처럼 참조할 수 있음
    # relationship 의 첫 번째 파라미터는 참조할 모델이고 backref 파라미터는 역참조 설정임.
    # 역참조란 질문에서 답변을 거꾸로 참조하는 것을 의미
    # 한 질문에는 여러 개의 답변이 달릴 수 있는데 역참조는 이 질문에 달린 답변들을 참조할 수 있게 한다.
    # 어떤 질문에 해당하는 객체가 a_question 이면 a_question.answers 와 같은 코드로 해당
    # 질문에 달린 답변들을 참조할 수 있음.
    question = relationship("Question", backref="answers")

    user_id = Column(Integer, ForeignKey("user.id"), nullable=True)
    user = relationship("User", backref="answer_users")
    sta = Column(Integer, nullable=True)    
    voter = relationship('User', secondary=answer_voter, backref='answer_voters')
    

class User(Base):
    __tablename__ = "user"
    
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    create_date = Column(DateTime, nullable=False)
