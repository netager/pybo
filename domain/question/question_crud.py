from datetime import datetime

from sqlalchemy import and_, or_
from sqlalchemy.orm import Session, selectinload, with_loader_criteria
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

from domain.question.question_schema import QuestionCreate, QuestionUpdate, QuestionDelete
from models import Question, User, Answer



# Question List 조회 -----------------------------------
# def get_question_list(db: Session, skip: int=0, limit: int=10):
#     _question_list = db.query(Question).order_by(Question.create_date.desc()).all()
#     total = _question_list.count()
#     question_list = _question_list.offset(skip).limit(limit).all()
#     return total, question_list    # (전체 건수, 페이징 적용된 질문 목록)

# 개선 버전
def get_question_list(db: Session, skip: int=0, limit: int=10, keyword: str = ''):
    question_list = db.query(Question).filter(Question.sta == 0)
    if keyword:
        search = '%%{}%%'.format(keyword)
        sub_query = db.query(Answer.question_id, Answer.content, User.username)\
            .outerjoin(User, and_(Answer.user_id == User.id)).subquery()
        question_list = question_list \
            .outerjoin(User) \
            .outerjoin(sub_query, and_(sub_query.c.question_id == Question.id)) \
            .filter(Question.subject.ilike(search) |    # 질문제목
                    Question.content.ilike(search) |    # 질문내용
                    User.username.ilike(search) |       # 질문작성자
                    sub_query.c.content.ilike(search) | # 답변내용
                    sub_query.c.username.ilike(search)  # 답변작성자
                    )
    total = question_list.count()
    question_list = (
        question_list
        .order_by(Question.create_date.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )
    return total, question_list    # (전체 건수, 페이징 적용된 질문 목록)

async def get_question_list_async(db: AsyncSession, skip: int = 0, limit: int = 10, keyword: str = ''):
    question_list = select(Question).filter(Question.sta == 0)

    if keyword:
        search = '%%{}%%'.format(keyword)

        sub_query = (
            select(
                Answer.question_id,
                Answer.content,
                User.username
            )
            .outerjoin(User, Answer.user_id == User.id)
            .subquery()
        )

        question_list = (
            question_list
            .outerjoin(User, Question.user_id == User.id)
            .outerjoin(sub_query, sub_query.c.question_id == Question.id)
            .filter(
                or_(
                    Question.subject.ilike(search),
                    Question.content.ilike(search),
                    User.username.ilike(search),
                    sub_query.c.content.ilike(search),
                    sub_query.c.username.ilike(search),
                )
            )
            .distinct()
        )

    total_stmt = select(func.count()).select_from(question_list.subquery())
    total_result = await db.execute(total_stmt)
    total = total_result.scalar()

    result = await db.execute(
        question_list
        .order_by(Question.create_date.desc())
        .offset(skip)
        .limit(limit)
    )
    question_list = result.scalars().all()

    return total, question_list

# async def get_question_list_async(db: AsyncSession, skip: int = 0, limit: int = 10, keyword: str = ''):
#     total_result = await db.execute(
#         select(func.count(Question.id))
#         .where(Question.sta == 0)
#     )
#     total = total_result.scalar()

#     question_result = await db.execute(
#         select(Question)
#         .order_by(Question.create_date.desc())
#         .offset(skip)
#         .limit(limit)
#     )
#     question_list = question_result.scalars().all()

#     return total, question_list
# End of Question List 조회 ----------------------------


# Question Detail 조회 ---------------------------------
def get_question(db: Session, question_id: int):
    question = (
        db.query(Question)
        .options(
            selectinload(Question.answers),
            with_loader_criteria(Answer, Answer.sta == 0),
            selectinload(Question.voter)    # Question 조회시 Question.voter 도 조회   
        )
        .filter(
            Question.id == question_id,
            Question.sta == 0
        )
        .first()
    )
    return question    

async def get_question_async(db: AsyncSession, question_id: int):
    result = await db.execute(
        select(Question)
        .options(
            selectinload(Question.answers), # Question 조회시 Question.answers 도 조회
            with_loader_criteria(Answer, Answer.sta == 0),  
            selectinload(Question.voter)    # Question 조회시 Question.voter 도 조회   
        )
        .filter(
            Question.id == question_id,
            Question.sta == 0
        )
    )
    return result.scalars().first()
# End of Question Detail 조회 --------------------------


# Question Create ---------------------------------
def create_question(db: Session, question_create: QuestionCreate, user: User):
    db_question = Question(subject=question_create.subject,
                           content=question_create.content,
                           create_date=datetime.now(),
                           user=user,
                           sta=0)
    db.add(db_question)
    db.commit()

async def create_question_async(db: AsyncSession, question_create: QuestionCreate, user: User):
    db_answer = Question(subject=question_create.subject,
                         content=question_create.content,
                         create_date=datetime.now(),
                         user=user,
                         sta=0)
    db.add(db_answer)
    await db.commit()
# End of Question Create --------------------------

# Question Update ---------------------------------
def update_question(db: Session, db_question: Question, question_update: QuestionUpdate):
    db_question.subject = question_update.subject
    db_question.content = question_update.content
    db_question.modify_date = datetime.now()

    db.add(db_question)
    db.commit()

async def update_question_async(db: AsyncSession, db_question: Question, question_update: QuestionUpdate):
    db_question.subject = question_update.subject
    db_question.content = question_update.content
    db_question.modify_date = datetime.now()

    db.add(db_question)
    await db.commit()
# Question Update ---------------------------------    

# Question Delete : question.sta -> 9 -------------
def delete_question(db: Session, db_question: Question, question_delete: QuestionDelete):
    db_question.sta = 9
    db_question.modify_date = datetime.now()

    db.add(db_question)
    db.commit()

async def delete_question_async(db: AsyncSession, db_question: Question, question_delete: QuestionDelete):
    db_question.sta = 9
    db_question.modify_date = datetime.now()

    db.add(db_question)
    await db.commit()
# End of Question Delete : question.sta -> 9 -------------    

# Question_Vote Create
def vote_question(db: Session, db_question: Question, db_user: User):
    db_question.voter.append(db_user)
    db.commit()
    
async def vote_question_async(db: AsyncSession, db_question: Question, db_user: User):
    db_question.voter.append(db_user)
    await db.commit() 
# End of Question_Vote Create    
       