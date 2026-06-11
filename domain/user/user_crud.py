from datetime import datetime

import bcrypt

from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from domain.user.user_schema import UserCreate
from models import User

def hash_password(password: str) -> str:
    password_bytes = password.encode("utf-8")
    hashed_password = bcrypt.hashpw(password_bytes, bcrypt.gensalt())
    return hashed_password.decode("utf-8")

def verify_password(password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(
        password.encode("utf-8"),
        hashed_password.encode("utf-8"),
    )

# User Create -----------------------------------
def create_user(db: Session, user_create: UserCreate):
    db_user = User(username=user_create.username,
                   password=hash_password(user_create.password1),
                   email=user_create.email,
                   create_date=datetime.now())
    print("[user_crud.py] create_user() 완료")               
    db.add(db_user)
    db.commit()    
    print("[user_crud.py] db.commit() 완료")               

async def create_user_async(db: AsyncSession, user_create: UserCreate):
    db_user = User(username=user_create.username,
                   password=hash_password(user_create.password1),
                   email=user_create.email,
                   create_date=datetime.now())
    db.add(db_user)
    await db.commit()
# End of Answer Create ----------------------------

def get_existing_user(db: Session, user_create: UserCreate):
    return db.query(User).filter(
        (User.username == user_create.username) |
        (User.email == user_create.email)
    ).first()

async def get_existing_user_async(db: AsyncSession, user_create: UserCreate):
    result = await db.execute(
        select(User).filter(
            (User.username == user_create.username) |
            (User.email == user_create.email)
        )
    )
    return result.scalars().first()

# Get User -----------------------------------
def get_user(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()

async def get_user_async(db: AsyncSession, username: str):
    result = await db.execute(select(User).filter(User.username == username))
    return result.scalars().first()
# End of Get User -----------------------------------

