from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session
from starlette import status

from database import get_db, get_db_async
from domain.answer import answer_schema, answer_crud
from domain.question import question_crud
from domain.user.user_router import get_current_user, get_current_user_async
from models import User

router = APIRouter(
    prefix="/api/answer",
)

# answer create ---------------------------
@router.post("/create/{question_id}", status_code=status.HTTP_204_NO_CONTENT)
def answer_create(question_id: int, 
                  _answer_create: answer_schema.AnswerCreate,
                  db: Session = Depends(get_db),
                  current_user: User = Depends(get_current_user)):
    
    # create answer
    question = question_crud.get_question(db, question_id=question_id)
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")
    
    answer_crud.create_answer(db, question=question, 
                              answer_create=_answer_create,
                              user=current_user)

@router.post("/create_async/{question_id}", status_code=status.HTTP_204_NO_CONTENT)
async def answer_create(question_id: int, 
                        _answer_create: answer_schema.AnswerCreate,
                        db: AsyncSession = Depends(get_db_async),
                        current_user: User = Depends(get_current_user_async)):
    # create answer
    question = await question_crud.get_question_async(db, question_id=question_id)
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")
    
    await answer_crud.create_answer_async(db, question=question, 
                                          answer_create=_answer_create,
                                          user=current_user)
# End of answer create ---------------------------

# get answer 
@router.get("/detail/{answer_id}", response_model=answer_schema.Answer)
def answer_detail(answer_id: int, db: Session = Depends(get_db)):
    answer = answer_crud.get_answer(db, answer_id=answer_id)
    return answer

@router.get("/detail_async/{answer_id}", response_model=answer_schema.Answer)
async def answer_detail_async(answer_id: int, db: AsyncSession = Depends(get_db_async)):
    answer = await answer_crud.get_answer_async(db, answer_id=answer_id)
    return answer
# End of get answer 


# Answer Update ---------------------------
@router.put("/update", status_code=status.HTTP_204_NO_CONTENT)
def answer_update(_answer_update: answer_schema.AnswerUpdate,
                  db: Session = Depends(get_db),
                  # store 에서 현재 로그인한 사용자 정보 조회
                  current_user: User = Depends(get_current_user)):

    db_answer = answer_crud.get_answer(db, answer_id=_answer_update.answer_id)
    if not db_answer:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="데이터를 찾을 수 없습니다.")
    if current_user.id != db_answer.user.id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="수정 권한이 없습니다.")
    answer_crud.update_answer(db, db_answer=db_answer,
                                  answer_update=_answer_update)                

@router.put("/update_async", status_code=status.HTTP_204_NO_CONTENT)
async def answer_update_async(_answer_update: answer_schema.AnswerUpdate,
                  db: AsyncSession = Depends(get_db_async),
                  # store 에서 현재 로그인한 사용자 정보 조회
                  current_user: User = Depends(get_current_user)):

    db_answer = await answer_crud.get_answer_async(db, answer_id=_answer_update.answer_id)
    if not db_answer:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="데이터를 찾을 수 없습니다.")
    if current_user.id != db_answer.user.id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="수정 권한이 없습니다.")
    await answer_crud.update_answer(db, db_answer=db_answer,
                                  answer_update=_answer_update)                
# End of Answer Update ---------------------------

# Answer Delete ---------------------------
@router.delete("/delete", status_code=status.HTTP_204_NO_CONTENT)
def answer_delete(_answer_delete: answer_schema.AnswerDelete,
                  db: Session = Depends(get_db),
                  current_user: User = Depends(get_current_user)):
    # delete answer
    db_answer = answer_crud.get_answer(db, answer_id=_answer_delete.answer_id)
    if not db_answer:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="데이터를 찾을 수 없습니다.")
    
    if current_user.id != db_answer.user_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="수정 권한이 없습니다.")
    answer_crud.delete_answer(db=db, db_answer=db_answer)

@router.delete("/delete_async", status_code=status.HTTP_204_NO_CONTENT)
async def answer_delete_async(_answer_delete: answer_schema.AnswerDelete,
                  db: AsyncSession = Depends(get_db_async),
                  current_user: User = Depends(get_current_user)):
    # delete answer
    db_answer = await answer_crud.get_answer_async(db, answer_id=_answer_delete.answer_id)
    if not db_answer:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="데이터를 찾을 수 없습니다.")
    
    if current_user.id != db_answer.user_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="수정 권한이 없습니다.")
    await answer_crud.delete_answer_async(db=db, db_answer=db_answer)

# Answer Voter Create
@router.post("/vote", status_code=status.HTTP_204_NO_CONTENT)
def answer_vote(_answer_vote: answer_schema.AnswerVote, db: Session = Depends(get_db),
                  current_user: User = Depends(get_current_user)):
    db_answer = answer_crud.get_answer(db, answer_id=_answer_vote.answer_id)
    if not db_answer:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="데이터를 찾을 수 없습니다.")
    if current_user in db_answer.voter:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail="이미 추천한 답변입니다.")                
    answer_crud.vote_answer(db, db_answer=db_answer, db_user=current_user)

@router.post("/vote_async", status_code=status.HTTP_204_NO_CONTENT)
async def answer_vote_async(_answer_vote: answer_schema.AnswerVote, db: AsyncSession = Depends(get_db_async),
                  current_user: User = Depends(get_current_user_async)):
    db_answer = await answer_crud.get_answer_async(db, answer_id=_answer_vote.answer_id)
    if not db_answer:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="데이터를 찾을 수 없습니다.")
    if current_user in db_answer.voter:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail="이미 추천한 답변입니다.")                
    await answer_crud.vote_answer_async(db, db_answer=db_answer, db_user=current_user)
    