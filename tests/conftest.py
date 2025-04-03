# tests/conftest.py
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient
from app.database import Base, get_db
from app.api import app
from app import models  # Import models so Base.metadata knows about them
from typing import Generator

# Use an in-memory SQLite database for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Override the get_db dependency to use the testing session
def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

# Configure FastAPI to use the overridden get_db
app.dependency_overrides[get_db] = override_get_db

# Fixture for creating the test database
@pytest.fixture(scope="session", autouse=True)
def create_test_database():
    Base.metadata.create_all(bind=engine)
    yield  # Run tests
    Base.metadata.drop_all(bind=engine)

# Fixture for providing a test client
@pytest.fixture
def test_client() -> Generator:
    with TestClient(app) as client:
        yield client

# Fixture for providing a database session
@pytest.fixture
def db_session() -> Generator:
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

# Optional: Fixture for creating sample data (can be used in tests)
@pytest.fixture
def sample_device_data(db_session: TestingSessionLocal):
    data1 = models.DeviceData(device_id="test_device_1", x=1.0, y=2.0, z=3.0)
    data2 = models.DeviceData(device_id="test_device_1", x=4.0, y=5.0, z=6.0)
    data3 = models.DeviceData(device_id="test_device_2", x=7.0, y=8.0, z=9.0)
    db_session.add_all([data1, data2, data3])
    db_session.commit()
    return [data1, data2, data3]