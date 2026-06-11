from models import Question, Answer
from database import SessionLocal

db = SessionLocal()
result = db.query(Question).all()
print(result)