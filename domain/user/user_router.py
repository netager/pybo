from datetime import timedelta, datetime, timezone

from fastapi import APIRouter, Depends, HTTPException

# OAuth 관련 import
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from jose import jwt, JWTError

from sqlalchemy.orm import Session
from starlette import status
from starlette.config import Config

from database import get_db, get_db_async
from domain.user import user_schema, user_crud
from domain.user.user_crud import verify_password

config = Config('.env')

# 토큰의 유효기간(분)
ACCESS_TOKEN_EXPIRE_MINUTES = int(config('ACCESS_TOKEN_EXPIRE_MINUTES'))

# 암호화시 사용하는 64자리의 랜덤한 문자열 - 노출 되면 안됨.
SECRET_KEY = config('SECRET_KEY')


# 토큰 생성시 사용하는 알고리즘(HS256: HMAC + SHA-256)
# header.payload.signature: xxxxx.yyyyy.zzzzz
# 토큰 생성: jwt.encode(data, SECRET_KEY, algorithm="HS256")
# 토큰 검증: jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
# SECRET_KEY 매우 중요 - 노출시 토큰 생성 가능
ALGORITHM = "HS256"

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/user/login")

router = APIRouter(
    prefix="/api/user",
)

# User Create ---------------------------
@router.post("/create", status_code=status.HTTP_204_NO_CONTENT)
def user_create(_user_create: user_schema.UserCreate, db: Session = Depends(get_db)):
    # create user
    user = user_crud.get_existing_user(db, user_create=_user_create)
    if user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="이미 존재하는 사용자입니다.")
    user_crud.create_user(db=db, user_create=_user_create)

@router.post("/create_async", status_code=status.HTTP_204_NO_CONTENT)
async def user_create_async(_user_create: user_schema.UserCreate, db: AsyncSession = Depends(get_db_async)):
    # create user
    user = await user_crud.get_existing_user_async(db, user_create=_user_create)
    if user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="이미 존재하는 사용자입니다.")

    await user_crud.create_user_async(db=db, user_create=_user_create)
# End of User Create ---------------------------

# Login ---------------------------
@router.post("/login", response_model=user_schema.Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(),
                           db: Session = Depends(get_db)):
    # check user and password
    user = user_crud.get_user(db, form_data.username)
    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # make access token
    data = {
        "sub": user.username,
        "exp": datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    }
    access_token = jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "username": user.username
    }
# End of Login ---------------------------


# 헤더정보의 Token값을 읽어 사용자 객체를 가져오는 함수
def get_current_user(token: str = Depends(oauth2_scheme),
                     db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    else:
        user = user_crud.get_user(db, username=username)
        if user is None:
            raise credentials_exception
        return user
    
async def get_current_user_async(token: str = Depends(oauth2_scheme),
                     db: AsyncSession = Depends(get_db_async)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    else:
        user = await user_crud.get_user_async(db, username=username)
        if user is None:
            raise credentials_exception
        return user    
# End of - 헤더정보의 Token값을 읽어 사용자 객체를 가져오는 함수