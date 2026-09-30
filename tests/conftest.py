from typing import Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from main import app
from app.dependency import get_db
from app.database import Base
from app.models import User, Wallet


TEST_DATABASE_URL = "sqlite:///./finance.db"

test_engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})

TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)

def get_test_db() -> Generator[Session, None, None]:
    db = TestSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = get_test_db



@pytest.fixture
def client():
    yield TestClient(app)

@pytest.fixture(autouse=True)
def setup_db():
    Base.metadata.create_all(bind=test_engine)
    yield
    Base.metadata.drop_all(bind=test_engine)

@pytest.fixture
def db_session() -> Generator[Session, None, None]:
    db = TestSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture
def user(db_session) -> User:
    user = User(login="test")
    db_session.add(user)
    db_session.flush()
    return user

@pytest.fixture
def wallet(db_session, user) -> Wallet:
    wallet = Wallet(name='Master', balance=200, user_id=user.id)
    db_session.add(wallet)
    db_session.commit()
    db_session.refresh(wallet)
    return wallet

@pytest.fixture
def auth_headers(user) -> dict:
    return {"Authorization": f"Bearer {user.login}"}
