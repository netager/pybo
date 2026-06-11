from datetime import datetime

from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from models import Question, Answer, User
from domain.answer.answer_schema import AnswerCreate, AnswerUpdate, AnswerDelete

# Answer Create -----------------------------------
def create_answer(db: Session, question: Question, answer_create: AnswerCreate, user: User):
    db_answer = Answer(question=question,
                       content=answer_create.content,
                       create_date=datetime.now(),
                       user=user,
                       sta=0)
    db.add(db_answer)
    db.commit()    

async def create_answer_async(db: AsyncSession, question: Question, answer_create: AnswerCreate, user: User):
    db_answer = Answer(question=question,
                       content=answer_create.content,
                       create_date=datetime.now(),
                       user=user,
                       sta=0)
    db.add(db_answer)
    await db.commit()
# End of Answer Create ----------------------------

# Get Answer --------------------------------------
def get_answer(db: Session, answer_id: int):
    return db.query(Answer).get(answer_id)

async def get_answer_async(db: AsyncSession, answer_id: int):
    result = await db.execute(
        select(Answer).where(Answer.id == answer_id)
    )
    return result.scalars().first()
# End of Get Answer -------------------------------

# Answer Update -----------------------------------
def update_answer(db: Session, db_answer: Answer, answer_update: AnswerUpdate):
    db_answer.content = answer_update.content
    db_answer.modify_date = datetime.now()
    
    db.add(db_answer)
    db.commit()

async def update_answer_async(db: AsyncSession, db_answer: Answer, answer_update: AnswerUpdate):
    db_answer.content = answer_update.content
    db_answer.modify_date = datetime.now()
    
    db.add(db_answer)
    await db.commit()
# Answer Update -----------------------------------

# Answer Delete : question.sta -> 9 -------------
def delete_answer(db: Session, db_answer: Answer):
    db_answer.sta = 9
    db_answer.modify_date = datetime.now()

    db.add(db_answer)
    db.commit()
    
async def delete_answer_async(db: AsyncSession, db_answer: Answer):
    db_answer.sta = 9
    db_answer.modify_date = datetime.now()

    db.add(db_answer)
    await db.commit()
# End of Answer Delete : question.sta -> 9 -------------

# Answer Vote Create -----------------------------------
def vote_answer(db: Session, db_answer: Answer, db_user: User):
    db_answer.voter.append(db_user)
    db.commit()

async def vote_answer_async(db: AsyncSession, db_answer: Answer, db_user: User):
    db_answer.voter.append(db_user)
    await db.commit() 
# End of Answer Vote Create ---------------------------