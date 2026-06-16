from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import declarative_base, sessionmaker
from starlette.config import Config

config = Config('.env')
SQLALCHEMY_DATABASE_URL = config('SQLALCHEMY_DATABASE_URL')
# ASYNC_SQLALCHEMY_DATABASE_URL = config('ASYNC_SQLALCHEMY_DATABASE_URL')

# create_engine(): 데이터베이스 커넥션 풀을 생성
# 커넥션 풀이란 데이터베이스에 접속하는 객체를 일정 갯수만큼 만들어 놓고 돌려가며 사용하는 것
# 커넥션 풀은 데이터베이스에 접속하는 세션수를 제어하고, 세션 접속에 소요되는 시간을 줄이고자흔 용도로 사용
# Async 
# -----
# engine = create_engine(
#     ASYNC_SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
# )
# Sync
# ----
# connect_args={"check_same_thread": False} 속성은 
# SQLite 데이터베이스를 사용하기 위해 적용하는 속성이다. 
# 그런데 PostgreSQL 데이터베이스를 사용할 때는 위의 속성을 사용하면 안된다. 
# 위 속성을 사용할 경우에는 데이터베이스에 접속할 수 없다는 오류가 발생한다.
if SQLALCHEMY_DATABASE_URL.startswith('sqlite'):
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
    )
else:
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL
    )

# 데이터베이스에 접속하기 위한 필요한 클래스
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 데이터베이스 모델을 구성할 때 사용되는 클래스
Base = declarative_base()

# SQLite 데이터베이스는 ORM을 사용할 때 몇 가지 문제점이 있다. 
# 이것은 SQLite 데이터베이스에만 해당하고 PostgreSQL이나 MySQL 등의 
# 다른 데이터베이스와는 상관없는 내용이다. 
# 앞으로의 진행을 원활하게 하기 위해 SQLite가 발생시킬 수 있는 오류를 먼저 해결
# MetaData 클래스를 사용하여 데이터베이스의 프라이머리 키, 유니크 키, 인덱스 키 등의 
# 이름 규칙을 새롭게 정의했다. 
# 데이터베이스에서 디폴트 값으로 명명되던 프라이머리 키, 유니크 키 등의 제약조건 이름을 
# 수동으로 설정한 것
naming_convention = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(column_0_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}
Base.metadata = MetaData(naming_convention=naming_convention)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# 비동기 방식으로 구현
# -------------------------------------------------
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

ASYNC_SQLALCHEMY_DATABASE_URL = "sqlite+aiosqlite:///./myapi.db"

async_engine = create_async_engine(ASYNC_SQLALCHEMY_DATABASE_URL)
AsyncSessionLocal = async_sessionmaker(
    autocommit=False, autoflush=False, bind=async_engine
)

async def get_db_async():
    db = AsyncSessionLocal()
    try:
        yield db
    finally:
        await db.close()
    
