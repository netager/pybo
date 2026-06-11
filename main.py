from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

# 프론트엔드(Svelte) 빌드(npm run build)를 통해 생성한 파일을 FastAPI에 적용 
from starlette.responses import FileResponse
from starlette.staticfiles import StaticFiles

# router 객체를 FastAPI에 등록해야 함.
from domain.question import question_router
from domain.answer import answer_router
from domain.user import user_router

app = FastAPI()

origins = [
    "http://127.0.0.1:5173",
    "http://localhost:5173",
    "http://pybo.jbbank.co.kr:8000",
    "http://141.164.40.151:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(question_router.router)
app.include_router(answer_router.router)
app.include_router(user_router.router)

# 프론트엔드(Svelte) 빌드(npm run build)를 통해 생성한 파일을 FastAPI에 적용 
app.mount("/assets", StaticFiles(directory="frontend/dist/assets"))

@app.get("/")
def index():
    return FileResponse("frontend/dist/index.html")
