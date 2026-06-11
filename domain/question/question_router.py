from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session
from starlette import status

from database import get_db, get_db_async
from domain.question import question_schema, question_crud
from domain.user.user_router import get_current_user, get_current_user_async
from models import User


router = APIRouter(
    prefix="/api/question",
)

# question list ---------------------------
# 라우팅: FastAPI 가 요청 받은 URL을 해석하여 그에 맞는 함수를 실행하여 그 결과를 리턴하는 행위
# Depends(getdb): Depends는 매개변수로 전달받은 함수를 호출하여 그 결과를 리턴.
@router.get("/list", response_model=question_schema.QuestionList)
def question_list(db: Session = Depends(get_db), page: int=0, size: int=10, keyword: str = ''):
    total, _question_list = question_crud.get_question_list(db, skip=page*size, limit=size, keyword=keyword)
    return {
        'total': total, 
        'question_list': _question_list
    }

@router.get("/list_async", response_model=question_schema.QuestionList)
async def question_list_async(db: AsyncSession = Depends(get_db_async), page: int=0, size: int=10, keyword: str = ''):
    total, _question_list = await question_crud.get_question_list_async(db, skip=page*size, limit=size, keyword=keyword)
    return {
        'total': total, 
        'question_list': _question_list
    }
# End of question list ---------------------------

# question detail ---------------------------------------    
@router.get("/detail/{question_id}", response_model=question_schema.Question)
def question_detail(question_id: int, db: Session = Depends(get_db)):
    _question = question_crud.get_question(db, question_id=question_id)
    if not _question:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="데이터를 찾을 수 없습니다.")
    return _question

@router.get("/detail_async/{question_id}", response_model=question_schema.Question)
async def question_detail_async(question_id: int, db: AsyncSession = Depends(get_db_async)):
    result = await question_crud.get_question_async(db, question_id=question_id)
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="데이터를 찾을 수 없습니다.")
    return result
# End of question detail --------------------------------    

# question create ---------------------------
@router.post("/create", status_code=status.HTTP_204_NO_CONTENT)
def question_create(_question_create: question_schema.QuestionCreate,
                  db: Session = Depends(get_db),
                  current_user: User = Depends(get_current_user)):
    # create question    
    question_crud.create_question(db, question_create=_question_create,
                                  user=current_user)

@router.post("/create_async", status_code=status.HTTP_204_NO_CONTENT)
async def question_create_async(_question_create: question_schema.QuestionCreate,
                                db: AsyncSession = Depends(get_db_async),
                                current_user: User = Depends(get_current_user_async)):
    # create answer
    await question_crud.create_question_async(db, question_create=_question_create,
                                              user=current_user)
# End of question create ---------------------------

# Question Update ---------------------------
@router.put("/update", status_code=status.HTTP_204_NO_CONTENT)
def question_update(_question_update: question_schema.QuestionUpdate,
                  db: Session = Depends(get_db),
                  current_user: User = Depends(get_current_user)):
    # update question    
    db_question = question_crud.get_question(db, question_id=_question_update.question_id)
    if not db_question:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="데이터를 찾을 수 없습니다.")
    if current_user.id != db_question.user.id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="수정 권한이 없습니다.")
    question_crud.update_question(db=db, db_question=db_question,
                                  question_update=_question_update)                

@router.put("/update_async", status_code=status.HTTP_204_NO_CONTENT)
async def question_update(_question_update: question_schema.QuestionUpdate,
                  db: AsyncSession = Depends(get_db_async),
                  current_user: User = Depends(get_current_user_async)):
    # update question    
    db_question = await question_crud.get_question_async(db, question_id=_question_update.question_id)
    if not db_question:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="데이터를 찾을 수 없습니다.")
    if current_user.id != db_question.user.id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="수정 권한이 없습니다.")
    await question_crud.update_question_async(db=db, db_question=db_question,
                                  question_update=_question_update)                
# End of Question Update ---------------------------

# Question Delete ---------------------------
@router.delete("/delete", status_code=status.HTTP_204_NO_CONTENT)
def question_delete(_question_delete: question_schema.QuestionDelete,
                  db: Session = Depends(get_db),
                  current_user: User = Depends(get_current_user)):
    # delete question    
    db_question = question_crud.get_question(db, question_id=_question_delete.question_id)
    if not db_question:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="데이터를 찾을 수 없습니다.")
    print(f"current_user.id: {current_user.id}, db_question.user.id: {db_question.user.id}")        
    if current_user.id != db_question.user.id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="수정 권한이 없습니다.")
    question_crud.delete_question(db=db, db_question=db_question,
                                  question_delete=_question_delete)                

@router.delete("/delete_async", status_code=status.HTTP_204_NO_CONTENT)
async def question_delete_async(_question_delete: question_schema.QuestionDelete,
                  db: AsyncSession = Depends(get_db_async),
                  current_user: User = Depends(get_current_user_async)):
    # delete question    
    db_question = await question_crud.get_question(db, question_id=_question_delete.question_id)
    if not db_question:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="데이터를 찾을 수 없습니다.")
    print(f"current_user.id: {current_user.id}, db_question.user.id: {db_question.user.id}")        
    if current_user.id != db_question.user.id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="수정 권한이 없습니다.")
    await question_crud.delete_question(db=db, db_question=db_question,
                                  question_delete=_question_delete)                
# End of Question Delete ---------------------------

# Question Voter Create
@router.post("/vote", status_code=status.HTTP_204_NO_CONTENT)
def question_vote(_question_vote: question_schema.QuestionVote, db: Session = Depends(get_db),
                  current_user: User = Depends(get_current_user)):
    db_question = question_crud.get_question(db, question_id=_question_vote.question_id)
    if not db_question:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="데이터를 찾을 수 없습니다.")
    if current_user in db_question.voter:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail="이미 추천한 질문입니다.")                
    question_crud.vote_question(db, db_question=db_question, db_user=current_user)

@router.post("/vote_async", status_code=status.HTTP_204_NO_CONTENT)
async def question_vote_async(_question_vote: question_schema.QuestionVote, db: AsyncSession = Depends(get_db_async),
                  current_user: User = Depends(get_current_user_async)):
    db_question = await question_crud.get_question_async(db, question_id=_question_vote.question_id)
    if not db_question:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="데이터를 찾을 수 없습니다.")
    if current_user in db_question.voter:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail="이미 추천한 질문입니다.")                
    await question_crud.vote_question_async(db, db_question=db_question, db_user=current_user)
    