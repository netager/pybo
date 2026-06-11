FastAPI 프로젝트 구조
앞으로 만들 파이보 프로젝트의 전체 구조는 다음과 같다. 지금은 구상하는 단계이므로 눈으로만 살펴보고 넘어가자. (현재는 main.py 파일만 만들어 놓은 상태이다.)

├── main.py
├── database.py
├── models.py
├── domain
│   ├── answer
│   ├── question
│   └── user
└── frontend
파이보 프로젝트를 설정하는 main.py 파일
main.py 파일에 생성한 app 객체는 FastAPI의 핵심 객체이다. app 객체를 통해 FastAPI의 설정을 할 수 있다. main.py는 FastAPI 프로젝트의 전체적인 환경을 설정하는 파일이다.

## database.py
- 데이터베이스 접속 대상 선택
- 데이터베이스 접속 풀 관리
데이터베이스를 설정하는 database.py 파일
database.py 파일은 데이터베이스와 관련된 설정을 하는 파일이다. 이 파일에는 데이터베이스를 사용하기 위한 변수, 함수등을 정의하고 접속할 데이터베이스의 주소와 사용자, 비밀번호등을 관리한다.

## models.py
- 테이블(모델) 관리
모델을 관리하는 models.py 파일
파이보 프로젝트는 ORM(object relational mapping)을 지원하는 파이썬 데이터베이스 도구인 SQLAlchemy를 사용한다. SQLAlchemy는 모델 기반으로 데이터베이스를 처리한다. 지금은 모델 기반으로 데이터베이스를 처리한다는 말이 이해되지 않겠지만, 이후 프로젝트를 진행하면 잘 알 수 있을 것이다. 아무튼 지금 여러분이 알아야 할 내용은 파이보 프로젝트에는 "모델 클래스들을 정의할 models.py 파일이 필요하다"는 것이다.

## domain
- 도메인별 crud - crud.py
- 도메인별 router - router.py
- 도메인별 출력 schema - schema.py 
API를 구성하는 domain 디렉터리
파이보 프로젝트는 질문과 답변을 작성하는 게시판을 만드는 것을 최종 목표로 하고 있다. 이에 "질문", "답변", "사용자" 라는 총 3개의 도메인을 두어 그 하위에 관련된 파일을 작성하고자 한다.

도메인은 "질문", "답변", "사용자" 처럼 굵직한 요구사항 또는 문제 영역을 대표하는 말이다.

질문 (question)
답변 (answer)
사용자 (user)
그리고 각 도메인은 API를 생성하기 위해서 다음과 같은 파일들이 필요하다.

라우터 파일 - URL과 API의 전체적인 동작을 관리
데이터베이스 처리 파일 - 데이터의 생성(Create), 조회(Read), 수정(Update), 삭제(Delete)를 처리 (CRUD)
입출력 관리 파일 - 입력 데이터와 출력 데이터의 스펙 정의 및 검증
예를 들어 질문(domain/question) 도메인이라면 다음의 3개 파일이 필요하다.

question_router.py - 라우터 파일
question_crud.py - 데이터베이스 처리 파일
question_schema.py - 입출력 관리 파일

## frontend 폴더
Svelte 프레임워크를 설치한 디렉터리이다. Svelte의 소스 및 빌드 파일들을 저장할 프론트엔드의 루트 디렉터리이다. 최종적으로 frontend/dist 디렉터리에 생성된 빌드 파일들을 배포시에 사용할 것이다.

## 스벨트에서 fetch로 요청이 들어오면
1.  Svelte fetch 요청
2. main.py
  - 도메인별 라우트 include
    - app.include_router(question_router.router)
3. 도메인별 라우트(domain/question/question_router.router)
  - 도메인별 URI를 활용한 route 분기
  - 출력 스키마 사용
  - question_crud.py 사용
```
  router = APIRouter(
    prefix="/api/question",
)

@router.get("/list", response_model=list[question_schema.Question])
def question_list(db: Session = Depends(get_db)):
    _question_list = question_crud.get_question_list(db)
    return _question_list
```
4. 스키마 정의
   - domain/question/question_schema.py
5. crud 정의  
   - domain/question/question_crud.py

## 트랜젝션 추가시 백엔드 절차
0. URL 정의
1. 출력 schema 정의
   - domain/question/question_schema.py 수정
2. crud 정의 
   - domain/question/question_crud.py 수정
3. router 수정
   - domain/question/question_router.py 수정
4. main.py 수정 
   - answer domain 추가시 수정
5. Svelte 요청 수정  

## 트랜젝션 추가시 프론트엔드 절차
1. / 접근 
   - App.svelte 에서 URI 를 보고 관련 페이지 Svelte로 라우팅
   - 새로운 트랜잭션 또는 화면 추가시 수정 필요

2. Svelte 수정 - routes/Detail.svelte


