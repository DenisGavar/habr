import pytest
from app.database import SessionLocal
from sqlalchemy.ext.asyncio import AsyncSession
from app.main import app
from fastapi.testclient import TestClient

@pytest.fixture(scope="module")
def db():
    """Фикстура для базы данных"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture(scope="module")
def client():
    """Фикстура для клиента FastAPI"""
    return TestClient(app)
