from sqlalchemy.orm import Session
from app.models import User

def create_user(db: Session, login: str) -> User:
    user = User(login=login)
    db.add(user)
    db.flush()
    return user

def get_user(db: Session, login: str) -> User | None:
    return db.query(User).filter(User.login == login).scalar()

def is_user_exist(db:Session, login: str) -> bool:
    pass